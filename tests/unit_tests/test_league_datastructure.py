import pytest


def test_get_division(example_league):
    assert (
            example_league.get_division(division_id=1) is example_league.divisions[0]
    )
    assert (
            example_league.get_division(division_id=2) is example_league.divisions[1]
    )
    assert (
            example_league.get_division(division_id=3) is example_league.divisions[2]
    )


def test_get_player_division_not_found(example_league):
    division_id = 999
    assert example_league.get_division(division_id) is None


def test_get_next_higher_division(example_league):
    division_id = example_league.divisions[1].id
    assert (
        example_league.get_next_higher_division(division_id)
        is example_league.divisions[2]
    )


def test_get_next_higher_division_already_highest(example_league):
    division_id = example_league.divisions[-1].id
    assert example_league.get_next_higher_division(division_id) is None


def test_get_accumulated_score(example_league):
    division_id = example_league.divisions[1].id
    score = 5

    total_score = example_league.get_accumulated_score(division_id, score)

    expected_total_score = 15
    assert total_score == expected_total_score
