from enum import Enum
from typing import Callable, Dict, List, NamedTuple, Optional, Tuple
from ..decorators import with_logger


class LeagueServiceError(Exception):
    pass


class ServiceNotReadyError(LeagueServiceError):
    pass


PlayerID = int
RatingType = str  # e.g. "ladder_1v1"
Rating = Tuple[float, float]


class GameOutcome(Enum):
    VICTORY = "VICTORY"
    DEFEAT = "DEFEAT"
    DRAW = "DRAW"
    MUTUAL_DRAW = "MUTUAL_DRAW"
    UNKNOWN = "UNKNOWN"
    CONFLICTING = "CONFLICTING"


class LeagueDivision(NamedTuple):
    id: int
    min_rating: float
    max_rating: float
    lowest_score: int
    highest_score: int


@with_logger
class League(NamedTuple):
    name: str
    divisions: List[LeagueDivision]
    current_season_id: int
    rating_type: str

    @classmethod
    def get_player_division(cls, division_id):
        for div in cls.divisions:
            if div.id == division_id:
                return div
        cls._logger.error("Could not find a division with id %s", division_id)
        return None

    @classmethod
    def get_next_lower_division(cls, division_id):
        i = 0
        for div in cls.divisions:
            if div.id == division_id:
                if i == 0:
                    return None
                else:
                    return cls.divisions[i - 1]
            i += 1

    @classmethod
    def get_next_higher_division(cls, division_id):
        i = 0
        for div in cls.divisions:
            if div.id == division_id:
                if i == len(cls.divisions) - 1:
                    return None
                else:
                    return cls.divisions[i + 1]
            i += 1

    @classmethod
    def get_accumulated_score(cls, division_id, score):
        div = cls.get_next_lower_division(division_id)
        while div is not None:
            score += div.highest_score
            div = cls.get_next_lower_division(div.id)
        return score


class LeagueScore(NamedTuple):
    division_id: int
    score: int
    game_count: int


class LeagueRatingRequest(NamedTuple):
    """
    Minimal information to recalculate league score after a finished game.
    Includes a callback to acknowledge processing.
    """

    player_id: PlayerID
    rating_type: RatingType
    rating: Rating
    outcome: GameOutcome
    callback: Optional[Callable]

    @classmethod
    def from_rating_change_dict(cls, message: Dict):
        return cls(
            message["player_id"],
            message["rating_type"],
            (message["new_rating_mean"], message["new_rating_deviation"]),
            getattr(GameOutcome, message["outcome"]),
            message.get("_ack"),
        )
