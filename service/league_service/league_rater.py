from service.league_service.typedefs import GameOutcome, Rating

from ..decorators import with_logger
from .typedefs import League, LeagueScore


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
        rating = player_rating[0] - 3 * player_rating[1]
        player_div = cls._get_player_division(current_score.division_id, league)
        # Highest divison has lowest id
        lowest_id, highest_id = cls._get_division_id_range()

        if current_score.game_count >= 10:
            if current_score.division_id is None:
                return cls._do_placement(league, current_score, rating)

            if rating > player_div.max_rating or rating < player_div.min_rating:
                boost = 1
            # Linear interpolation of score and rating to have players in top division sorted by rating
            elif player_div.id == lowest_id and current_score.score < (player_div.highest_score - player_div.lowest_score) \
                    * (rating - player_div.min_rating) / (player_div.max_rating - player_div.min_rating):
                boost = 1

            if outcome == "VICTORY":
                current_score.score += 1 + boost
            elif outcome == "DEFEAT":
                current_score.score -= 1 + boost
            if current_score.score < 0:
                current_score.score = 0

            if current_score.score > player_div.highest_score:
                if lowest_id < current_score.division_id:
                    current_score.division_id -= 1
            elif current_score.score < player_div.lowest_score:
                if highest_id > current_score.division_id:
                    current_score.division_id += 1

        current_score.game_count += 1

        return current_score

    @classmethod
    def _get_player_division(cls, division_id, league):
        for div in league.divisions:
            if div.id == division_id:
                return div

    @classmethod
    def _get_division_id_range(cls, league):
        highest_id = league.divisions[0].id
        lowest_id = highest_id
        for div in league.divisions:
            if div.id < lowest_id:
                lowest_id = div.id
            if div.id > highest_id:
                highest_id = div.id
        return lowest_id, highest_id

    @classmethod
    def _do_placement(cls, league, current_score, rating):
        rating -= 300
        for div in league.divisions:
            if div.max_rating > rating > div.min_rating:
                current_score.division_id = div.id
                current_score.score = (div.highest_score - div.lowest_score) \
                    * (rating - div.min_rating) / (div.max_rating - div.min_rating)
                current_score.game_count += 1
                return current_score
