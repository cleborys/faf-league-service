import pytest

from service.league_service.league_rater import LeagueRater
from service.league_service.typedefs import (
    GameOutcome,
    League,
    LeagueDivision,
    LeagueScore,
)


@pytest.fixture
def unplaced_player_score():
    return LeagueScore(division_id=None, score=None, game_count=10)


def test_new_score_victory_no_boost(example_league):
    current_score = LeagueScore(division_id=2, score=5, game_count=30)
    player_rating = 150

    new_score = LeagueRater._calculate_new_score(
        example_league,
        current_score,
        GameOutcome.VICTORY,
        player_rating,
        example_league.divisions[1],
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score + 1


def test_new_score_victory_boost(example_league):
    current_score = LeagueScore(division_id=2, score=5, game_count=30)
    player_rating = 1500

    new_score = LeagueRater._calculate_new_score(
        example_league,
        current_score,
        GameOutcome.VICTORY,
        player_rating,
        example_league.divisions[1],
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score + 2


def test_placement(example_league, unplaced_player_score):
    rating = 150

    new_score = LeagueRater._do_placement(example_league, unplaced_player_score, rating)

    assert new_score.division_id == example_league.divisions[1].id
    assert new_score.score == 5  # TODO: or whatever you expect here


def test_placement_high_rating(example_league, unplaced_player_score):
    rating = 1500

    new_score = LeagueRater._do_placement(example_league, unplaced_player_score, rating)

    assert new_score.division_id == example_league.divisions[-1].id
    assert new_score.score > 100  # TODO: or whatever you expect here


def test_placement_low_rating(example_league, unplaced_player_score):
    rating = -500

    new_score = LeagueRater._do_placement(example_league, unplaced_player_score, rating)

    assert new_score.division_id == example_league.divisions[0].id
    assert new_score.score == 0  # TODO: or whatever you expect here
