from enum import Enum
from typing import Callable, Dict, List, NamedTuple, Optional, Tuple

from ..decorators import with_logger


class LeagueServiceError(Exception):
    pass


class ServiceNotReadyError(LeagueServiceError):
    pass


class DivisionDoesNotExistError(Exception):
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
    highest_score: int


@with_logger
class League(NamedTuple):
    name: str
    divisions: List[LeagueDivision]
    current_season_id: int
    rating_type: str

    def get_division(self, division_id):
        for div in self.divisions:
            if div.id == division_id:
                return div
        self._logger.warning("Could not find a division with id %s", division_id)
        return None

    def _get_division_index(self, division_id):
        return next((i for (i, div) in enumerate(self.divisions) if div.id == division_id), [None])

    def get_next_lower_division(self, division_id: int) -> Optional[int]:
        i = self._get_division_index(division_id)
        if i == 0:
            return None
        else:
            return self.divisions[i - 1]

    def get_next_higher_division(self, division_id: int) -> Optional[int]:
        i = self._get_division_index(division_id)
        if i == len(self.divisions) - 1:
            return None
        else:
            return self.divisions[i + 1]

    def get_accumulated_score(self, division_id, score):
        my_division_index = self._get_division_index(division_id)
        return score + sum(div.highest_score for div in self.divisions[:my_division_index])

    def get_highest_division(self):
        return self.divisions[-1]

    def get_lowest_division(self):
        return self.divisions[0]


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
