import pytest

from service.league_service.typedefs import League, LeagueDivision


@pytest.fixture
def example_league():
    return League(
        name="example_league",
        divisions=[
            LeagueDivision(
                id=1, min_rating=None, max_rating=100, lowest_score=0, highest_score=10
            ),
            LeagueDivision(
                id=2, min_rating=100, max_rating=200, lowest_score=0, highest_score=10
            ),
            LeagueDivision(
                id=3, min_rating=200, max_rating=None, lowest_score=0, highest_score=10
            ),
        ],
        current_season_id=0,
        rating_type="global",
    )
