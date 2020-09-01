import pytest

from service import config
from service.league_service.league_rater import LeagueRater
from service.league_service.typedefs import (GameOutcome, League,
                                             LeagueDivision, LeagueScore)


@pytest.fixture
def unplaced_player_score():
    return LeagueScore(division_id=None, score=None, game_count=config.PLACEMENT_GAMES - 1)


def test_new_score_victory_no_boost(example_league):
    current_score = LeagueScore(division_id=2, score=5, game_count=30)
    player_rating = (180.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.VICTORY,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score + config.SCORE_GAIN

    player_rating = (10.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.VICTORY,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score + config.SCORE_GAIN


def test_new_score_victory_boost(example_league):
    current_score = LeagueScore(division_id=2, score=5, game_count=30)
    player_rating = (1800.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.VICTORY,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score + config.SCORE_GAIN + config.POSITIVE_BOOST


def test_new_score_defeat_no_boost(example_league):
    current_score = LeagueScore(division_id=2, score=5, game_count=30)
    player_rating = (180.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.DEFEAT,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score - config.SCORE_GAIN

    player_rating = (1800.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.DEFEAT,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score - config.SCORE_GAIN


def test_new_score_defeat_boost(example_league):
    current_score = LeagueScore(division_id=2, score=5, game_count=30)
    player_rating = (60.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.DEFEAT,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score - config.SCORE_GAIN - config.NEGATIVE_BOOST


def test_new_score_victory_highest_division_no_boost(example_league):
    current_score = LeagueScore(division_id=3, score=5, game_count=30)
    player_rating = (240.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.VICTORY,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score + config.SCORE_GAIN


def test_new_score_victory_highest_division_boost(example_league):
    current_score = LeagueScore(division_id=3, score=5, game_count=30)
    player_rating = (380.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.VICTORY,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score + config.SCORE_GAIN + config.HIGHEST_DIVISION_BOOST


def test_placement_after_enough_games(example_league, unplaced_player_score):
    # Neutralize the offset in the placement function so we can test the score independently of the config settings
    rating = (150.0 - config.RATING_MODIFIER_FOR_PLACEMENT, 0.0)

    new_score = LeagueRater.rate(example_league, unplaced_player_score, GameOutcome.DRAW, rating)

    assert new_score.division_id == example_league.divisions[1].id
    assert new_score.game_count == unplaced_player_score.game_count + 1
    assert new_score.score == 5


def test_replacement_at_invalid_player_division(example_league):
    current_score = LeagueScore(division_id=999, score=4, game_count=config.PLACEMENT_GAMES)
    rating = (150.0 - config.RATING_MODIFIER_FOR_PLACEMENT, 0.0)

    new_score = LeagueRater.rate(example_league, current_score, None, rating)

    assert new_score.division_id == example_league.divisions[1].id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == 5


def test_placement(example_league, unplaced_player_score):
    # Neutralize the offset in the placement function so we can test the score independently of the config settings
    rating = 150 - config.RATING_MODIFIER_FOR_PLACEMENT

    new_score = LeagueRater._do_placement(example_league, unplaced_player_score, rating)

    assert new_score.division_id == example_league.divisions[1].id
    assert new_score.game_count == unplaced_player_score.game_count + 1
    assert new_score.score == 5


def test_placement_high_rating(example_league, unplaced_player_score):
    rating = 1500 - config.RATING_MODIFIER_FOR_PLACEMENT

    new_score = LeagueRater._do_placement(example_league, unplaced_player_score, rating)

    assert new_score.division_id == example_league.divisions[-1].id
    assert new_score.game_count == unplaced_player_score.game_count + 1
    assert new_score.score == 10


def test_placement_low_rating(example_league, unplaced_player_score):
    rating = -500 - config.RATING_MODIFIER_FOR_PLACEMENT

    new_score = LeagueRater._do_placement(example_league, unplaced_player_score, rating)

    assert new_score.division_id == example_league.divisions[0].id
    assert new_score.game_count == unplaced_player_score.game_count + 1
    assert new_score.score == 0


def test_new_player(example_league):
    current_score = LeagueScore(division_id=None, score=None, game_count=0)
    player_rating = (380.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.VICTORY,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == 1
    assert new_score.score == current_score.score


def test_placement_games(example_league):
    current_score = LeagueScore(division_id=None, score=None, game_count=5)
    player_rating = (380.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.VICTORY,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == 6
    assert new_score.score == current_score.score


def test_promote(example_league):
    current_score = LeagueScore(division_id=2, score=10, game_count=30)
    player_rating = (380.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.VICTORY,
        player_rating,
    )

    assert new_score.division_id == 3
    assert new_score.game_count == 31
    assert new_score.score == config.POINT_BUFFER_AFTER_DIVISION_CHANGE


def test_demote(example_league):
    current_score = LeagueScore(division_id=2, score=0, game_count=30)
    player_rating = (380.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.DEFEAT,
        player_rating,
    )

    assert new_score.division_id == 1
    assert new_score.game_count == 31
    assert new_score.score == 10 - config.POINT_BUFFER_AFTER_DIVISION_CHANGE


def test_promote_in_highest_division(example_league):
    current_score = LeagueScore(division_id=3, score=10, game_count=30)
    player_rating = (380.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.VICTORY,
        player_rating,
    )

    assert new_score.division_id == 3
    assert new_score.game_count == 31
    assert new_score.score == 10


def test_demote_in_lowest_division(example_league):
    current_score = LeagueScore(division_id=1, score=0, game_count=30)
    player_rating = (380.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.DEFEAT,
        player_rating,
    )

    assert new_score.division_id == 1
    assert new_score.game_count == 31
    assert new_score.score == 0


def test_score_too_high(example_league):
    current_score = LeagueScore(division_id=2, score=14, game_count=30)
    player_rating = (380.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.VICTORY,
        player_rating,
    )

    assert new_score.division_id == 3
    assert new_score.game_count == 31
    assert new_score.score == config.POINT_BUFFER_AFTER_DIVISION_CHANGE


def test_score_too_low(example_league):
    current_score = LeagueScore(division_id=2, score=-14, game_count=30)
    player_rating = (380.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.VICTORY,
        player_rating,
    )

    assert new_score.division_id == 1
    assert new_score.game_count == 31
    assert new_score.score == 10 - config.POINT_BUFFER_AFTER_DIVISION_CHANGE


def test_other_game_outcomes(example_league):
    current_score = LeagueScore(division_id=2, score=4, game_count=30)
    player_rating = (180.0, 0.0)

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.DRAW,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.MUTUAL_DRAW,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.UNKNOWN,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score

    new_score = LeagueRater.rate(
        example_league,
        current_score,
        GameOutcome.CONFLICTING,
        player_rating,
    )

    assert new_score.division_id == current_score.division_id
    assert new_score.game_count == current_score.game_count + 1
    assert new_score.score == current_score.score
