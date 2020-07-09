from service.league_service.typedefs import GameOutcome, Rating

from ..decorators import with_logger
from .typedefs import League, LeagueScore
from ..config import *


class LeagueRatingError(Exception):
    pass


@with_logger
class LeagueRater:
    @classmethod
    def rate(
        cls,
        league: League,
        current_score: LeagueScore,
        outcome: GameOutcome,
        player_rating: Rating,
    ):
        boost = 0
        reduction = 0
        rating = player_rating[0] - 3 * player_rating[1]
        player_div = cls._get_player_division(current_score.division_id, league)
        # Highest divison has lowest id
        lowest_id, highest_id = cls._get_division_id_range()

        if current_score.game_count < PLACEMENT_GAMES:
            return LeagueScore(
                current_score.division_id,
                current_score.score,
                current_score.game_count + 1
            )

        if current_score.division_id is None:
            return cls._do_placement(league, current_score, rating)

        if rating > player_div.max_rating:
            boost = POSITIVE_BOOST
        elif rating < player_div.min_rating:
            reduction = NEGATIVE_BOOST
        # Linear interpolation of score and rating to have players in top division sorted by rating
        elif player_div.id == lowest_id and current_score.score < (player_div.highest_score - player_div.lowest_score) \
                * (rating - player_div.min_rating) / (player_div.max_rating - player_div.min_rating):
            boost = HIGHEST_DIVISION_BOOST

        new_score = current_score.score
        if outcome is GameOutcome.VICTORY:
            new_score += SCORE_GAIN + boost
        elif outcome is GameOutcome.DEFEAT:
            new_score -= SCORE_GAIN + reduction
        if new_score < 0:
            new_score = 0

        new_division_id = current_score.division_id
        if new_score > player_div.highest_score:
            if lowest_id < new_division_id:
                new_division_id -= 1
        elif new_score < player_div.lowest_score:
            if highest_id > new_division_id:
                new_division_id += 1

        return LeagueScore(
            new_division_id,
            new_score,
            current_score.game_count + 1
        )

    @classmethod
    def _get_player_division(cls, division_id, league):
        for div in league.divisions:
            if div.id == division_id:
                return div
            # Todo: fallback

    @classmethod
    def _get_division_id_range(cls, league):
        return (
            max(div.id for div in league.divisions),
            min(div.id for div in league.divisions)
        )

    @classmethod
    def _do_placement(cls, league, current_score, rating):
        rating += RATING_MODIFIER_FOR_PLACEMENT
        for div in league.divisions:
            if div.max_rating > rating > div.min_rating:
                new_score = (div.highest_score - div.lowest_score) \
                    * (rating - div.min_rating) / (div.max_rating - div.min_rating)
                return LeagueScore(
                    div.id,
                    new_score,
                    current_score.game_count + 1
                )
            # Todo: fallback
