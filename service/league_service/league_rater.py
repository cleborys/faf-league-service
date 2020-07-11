from service.league_service.typedefs import GameOutcome, Rating, League, LeagueScore

from service import config
from ..decorators import with_logger


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
        rating = player_rating[0] - 3 * player_rating[1]
        player_div = league.get_player_division(current_score.division_id)

        if current_score.game_count is None:
            return LeagueScore(
                current_score.division_id,
                current_score.score,
                1
            )
        if current_score.game_count < config.PLACEMENT_GAMES - 1:  # This check is before we increase game_count
            return LeagueScore(
                current_score.division_id,
                current_score.score,
                current_score.game_count + 1
            )
        if current_score.division_id is None or player_div is None:
            if player_div is None:
                cls._logger.warning("Doing placement again, because a division for id %s could not be found",
                                    current_score.division_id)
            return cls._do_placement(league, current_score, rating)

        score = cls._calculate_new_score(league, current_score, outcome, rating, player_div)
        new_score, new_division_id = cls._calculate_division_change(league, score, current_score.division_id, player_div)
        return LeagueScore(
            new_division_id,
            new_score,
            current_score.game_count + 1
        )

    @classmethod
    def _do_placement(cls, league, current_score, rating):
        rating += config.RATING_MODIFIER_FOR_PLACEMENT
        for div in league.divisions:
            if div.max_rating >= rating >= div.min_rating:
                new_score = div.highest_score * (rating - div.min_rating) / (div.max_rating - div.min_rating)
                return LeagueScore(
                    div.id,
                    new_score,
                    current_score.game_count + 1
                )

        highest_div = league.get_highest_division()
        if rating > highest_div.max_rating:
            return LeagueScore(
                highest_div.id,
                highest_div.highest_score,
                current_score.game_count + 1
            )

        lowest_div = league.get_lowest_division()
        if rating < lowest_div.min_rating:
            return LeagueScore(
                lowest_div.id,
                0,
                current_score.game_count + 1
            )

        cls._logger.error("Could not find a suitable division in league %s for placement for rating %s", league, rating)
        return LeagueScore(
            current_score.division_id,
            current_score.score,
            current_score.game_count + 1
        )

    @classmethod
    def _calculate_new_score(cls, league, current_score, outcome, rating, player_div):
        boost = 0
        reduction = 0
        higher_div = league.get_next_higher_division(player_div.id)

        if rating > player_div.max_rating:
            boost = config.POSITIVE_BOOST
        elif rating < player_div.min_rating:
            reduction = config.NEGATIVE_BOOST
        # Boost for high rated players with low score to have players in top division sorted by rating
        elif higher_div is None and current_score.score < player_div.highest_score \
                * (rating - player_div.min_rating) / (player_div.max_rating - player_div.min_rating):
            boost = config.HIGHEST_DIVISION_BOOST

        new_score = current_score.score
        if outcome is GameOutcome.VICTORY:
            new_score += config.SCORE_GAIN + boost
        elif outcome is GameOutcome.DEFEAT:
            new_score -= config.SCORE_GAIN + reduction

        return new_score

    @classmethod
    def _calculate_division_change(cls, league, score, division_id, player_div):
        if score > player_div.highest_score:
            higher_div = league.get_next_higher_division(player_div.id)
            if higher_div is not None:
                division_id = higher_div.id
                score = config.POINT_BUFFER_AFTER_DIVISION_CHANGE
            else:
                score = player_div.highest_score
        elif score < 0:
            lower_div = league.get_next_lower_division(player_div.id)
            if lower_div is not None:
                division_id = lower_div.id
                score = lower_div.highest_score - config.POINT_BUFFER_AFTER_DIVISION_CHANGE
            else:
                score = 0
        return score, division_id
