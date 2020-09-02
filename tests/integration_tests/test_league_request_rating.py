import pytest

from service.league_service import LeagueService
from service.league_service.typedefs import LeagueScore


@pytest.fixture
async def league_service(database, message_queue_service):
    service = LeagueService(database, message_queue_service)
    await service.initialize()
    yield service
    service.kill()


pytestmark = pytest.mark.asyncio


async def test_rate_new_player(league_service):
    new_player_id = 50
    rating_type = "global"
    rating_change_message = {
        "player_id": new_player_id,
        "rating_type": rating_type,
        "new_rating_mean": 1200,
        "new_rating_deviation": 200,
        "game_id": 1,
        "outcome": "VICTORY",
    }

    await league_service.enqueue(rating_change_message)
    await league_service._join_queue()

    league_season_id = league_service._leagues_by_rating_type[rating_type][
        0
    ].current_season_id
    saved_score = await league_service._load_score(new_player_id, league_season_id)
    assert saved_score == LeagueScore(None, None, 1)


async def test_rate_new_player_twice(league_service):
    new_player_id = 50
    rating_type = "global"

    for game_nbr in range(2):
        rating_change_message = {
            "player_id": new_player_id,
            "rating_type": rating_type,
            "new_rating_mean": 1200,
            "new_rating_deviation": 200,
            "game_id": game_nbr,
            "outcome": "VICTORY",
        }
        await league_service.enqueue(rating_change_message)
    await league_service._join_queue()

    league_season_id = league_service._leagues_by_rating_type[rating_type][
        0
    ].current_season_id
    saved_score = await league_service._load_score(new_player_id, league_season_id)
    assert saved_score == LeagueScore(None, None, 2)


async def test_rate_new_player_until_placement(league_service):
    new_player_id = 50
    rating_type = "global"

    for game_nbr in range(10):
        rating_change_message = {
            "player_id": new_player_id,
            "rating_type": rating_type,
            "new_rating_mean": 1200,
            "new_rating_deviation": 200,
            "game_id": game_nbr,
            "outcome": "VICTORY",
        }
        await league_service.enqueue(rating_change_message)
    await league_service._join_queue()

    league_season_id = league_service._leagues_by_rating_type[rating_type][
        0
    ].current_season_id
    saved_score = await league_service._load_score(new_player_id, league_season_id)
    assert saved_score.game_count == 10
    assert saved_score.division_id is not None
    assert saved_score.score is not None
