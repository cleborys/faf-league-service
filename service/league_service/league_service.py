import asyncio
from collections import defaultdict
from typing import Dict

from aio_pika import IncomingMessage

import aiocron
from service import config
from service.db import FAFDatabase
from service.db.models import (leaderboard, league, league_season,
                               league_season_division, league_season_score)
from service.decorators import with_logger
from service.message_queue_service import MessageQueueService, message_to_dict
from service.metrics import league_service_backlog
from sqlalchemy import and_, select
from sqlalchemy.dialects.mysql import insert

from .league_rater import LeagueRater
from .typedefs import (InvalidScoreError, League, LeagueDivision,
                       LeagueRatingRequest, LeagueScore, ServiceNotReadyError)


@with_logger
class LeagueService:
    def __init__(self, database: FAFDatabase, mq_service: MessageQueueService):
        self._db = database
        self._mq_service = mq_service
        self._accept_input = False
        self._queue = asyncio.Queue()
        self._task = None
        self._leagues_by_rating_type = None

    async def initialize(self) -> None:
        if self._task is not None:
            self._logger.error("Service already runnning or not properly shut down.")
            return

        await self.update_data()
        self._update_cron = aiocron.crontab("*/10 * * * *", func=self.update_data)
        self._accept_input = True
        self._logger.debug("LeagueService starting...")
        self._task = asyncio.create_task(self._handle_queue())

        # Listen for league events
        await self._mq_service.listen(
            config.EXCHANGE_NAME, config.LEAGUE_REQUEST_ROUTING_KEY, self.handle_message
        )

    async def update_data(self):
        async with self._db.acquire() as conn:
            sql = (
                select(
                    [league_season, league, league_season_division, leaderboard],
                    use_labels=True,
                )
                .select_from(
                    league_season_division.outerjoin(league_season)
                    .outerjoin(league)
                    .outerjoin(leaderboard)
                )
                .where(league_season.c.end_date == None)
            )
            result = await conn.execute(sql)
            division_rows = await result.fetchall()

        divisions_by_league = defaultdict(list)
        for row in division_rows:
            divisions_by_league[row[league.c.technical_name]].append(row)

        self._leagues_by_rating_type = defaultdict(list)
        for league_name, division_list in divisions_by_league.items():
            rating_type = division_list[0][leaderboard.c.technical_name]
            division_list.sort(
                key=lambda row: (
                    row[league_season_division.c.division_index],
                    row[league_season_division.c.id],
                )
            )
            self._leagues_by_rating_type[rating_type].append(
                League(
                    league_name,
                    [
                        LeagueDivision(
                            row[league_season_division.c.id],
                            row[league_season_division.c.min_rating],
                            row[league_season_division.c.max_rating],
                            row[league_season_division.c.highest_score],
                        )
                        for row in division_list
                    ],
                    division_list[0][league_season.c.id],
                    rating_type,
                )
            )

    async def _handle_queue(self) -> None:
        self._logger.info("LeagueService started!")
        while self._accept_input or not self._queue.empty():
            request = await self._queue.get()

            try:
                await self._rate_request(request)
            except Exception:  # pragma: no cover
                self._logger.exception("Failed handling request %s", request)
            else:
                self._logger.debug("Done handling request.")

            self._queue.task_done()
            if request.callback is not None:
                request.callback()
            league_service_backlog.set(self._queue.qsize())

        self._logger.info("LeagueService stopped.")

    async def _rate_request(self, request: LeagueRatingRequest) -> None:
        for league_object in self._leagues_by_rating_type[request.rating_type]:
            await self._rate_single_league(league_object, request)

    async def _rate_single_league(self, league: League, request: LeagueRatingRequest):
        current_score = await self._load_score(
            request.player_id, league.current_season_id
        )
        new_score = LeagueRater.rate(
            league, current_score, request.outcome, request.rating
        )
        await self._persist_score(
            request.player_id, league.current_season_id, new_score
        )
        await self._broadcast_score_change(request.player_id, league, new_score)

    async def _load_score(self, player_id, league_season_id):
        async with self._db.acquire() as conn:
            sql = select([league_season_score]).where(
                and_(
                    league_season_score.c.login_id == player_id,
                    league_season_score.c.league_season_id == league_season_id,
                )
            )
            result = await conn.execute(sql)
            row = await result.fetchone()
        if row is None:
            return LeagueScore(None, None, 0)

        return LeagueScore(
            row[league_season_score.c.division_id],
            row[league_season_score.c.score],
            row[league_season_score.c.game_count],
        )

    async def _persist_score(
        self, player_id: int, season_id: int, new_score: LeagueScore
    ):
        async with self._db.acquire() as conn:
            # TODO this asserts that the passed season_id matches the
            # division_id of new_score. It would be better to enforce this
            # relationship in the database
            # Note that new_score.division_id may be NULL,
            # while season_id must not be

            if new_score.division_id is not None:
                if new_score.score is None:
                    raise InvalidScoreError("Missing score for non-null division.")

                select_season_id = select(
                    [league_season_division.c.league_season_id]
                ).where(league_season_division.c.id == new_score.division_id)
                result = await conn.execute(select_season_id)
                row = await result.fetchone()
                season_id_of_division = row.get("league_season_id")
                if season_id != season_id_of_division:
                    raise InvalidScoreError("Division id did not match season id.")

            upsert_sql = (
                insert(league_season_score)
                .values(
                    login_id=player_id,
                    league_season_id=season_id,
                    division_id=new_score.division_id,
                    score=new_score.score,
                    game_count=new_score.game_count,
                )
                .on_duplicate_key_update(
                    division_id=new_score.division_id,
                    score=new_score.score,
                    game_count=new_score.game_count,
                )
            )
            await conn.execute(upsert_sql)

    async def _broadcast_score_change(
        self, player_id, league: League, new_score: LeagueScore
    ):
        pass

    def handle_message(self, message: IncomingMessage):
        """
        Parses a message from RabbitMQ to python dict with callback and queues it up.
        Needs to be synchronous to be used as a callback.
        """
        try:
            parsed_dict = message_to_dict(message)
        except Exception as e:
            self._logger.warning(
                "Failed to parse message with body %s\n Raised exception %s",
                message.body,
                e,
            )
            message.reject()
        else:
            asyncio.create_task(self.enqueue(parsed_dict))

    async def enqueue(self, rating_change_message: Dict) -> None:
        if not self._accept_input:
            self._logger.warning("Dropped league request %s", rating_change_message)
            raise ServiceNotReadyError(
                "LeagueService not yet initialized or shutting down."
            )

        try:
            request = LeagueRatingRequest.from_rating_change_dict(rating_change_message)
        except Exception as e:
            self._logger.warning(
                "Failed to parse info from message id %s: %s",
                rating_change_message.get("_id"),
                str(e),
            )
            if rating_change_message.get("_ack") is not None:
                rating_change_message["_ack"]()
            return
        await self._queue.put(request)
        league_service_backlog.set(self._queue.qsize())

    async def _join_queue(self) -> None:
        """
        Offers a call that is blocking until the queue has been emptied.
        Mostly for testing purposes.
        """
        await self._queue.join()

    async def shutdown(self) -> None:
        """
        Finish handling all remaining requests, then exit.
        """
        self._accept_input = False
        self._logger.debug(
            "Shutdown initiated. Waiting on current queue: %s", self._queue
        )
        await self._queue.join()
        self._task = None
        self._logger.debug("Queue emptied: %s", self._queue)

    def kill(self) -> None:
        """
        Exit without waiting for the queue to join.
        """
        self._accept_input = False
        if self._task is not None:
            self._task.cancel()
            self._task = None
