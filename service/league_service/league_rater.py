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
        return current_score
