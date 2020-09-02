DELETE FROM league_season_score;
DELETE FROM league_season_division;
DELETE FROM league_season;
DELETE FROM league;

INSERT INTO league (id, technical_name, name_key, description_key) VALUES
  (1, "test_league", "name_key", "description_key"),
  (2, "second_test_league", "name_key", "description_key"),
  (3, "league_without_seasons", "name_key", "description_key");

INSERT INTO league_season (id, league_id, leaderboard_id, start_date, end_date) VALUES
  (1, 1, 1, NOW() - interval 2 year, NOW() - interval 1 year),
  (2, 1, 1, NOW() - interval 1 year, NULL),
  (3, 2, 2, NOW() - interval 2 year, NULL);

INSERT INTO league_season_division (id, league_season_id, division_index, name_key, description_key, min_rating, max_rating, highest_score) VALUES
  (1, 1, 1, "name_key", "description_key", 0, 150, 10),
  (2, 1, 2, "name_key", "description_key", 150, 3000, 10),
  (3, 2, 1, "name_key", "description_key", 0, 100, 10),
  (4, 2, 2, "name_key", "description_key", 100, 200, 10),
  (5, 2, 3, "name_key", "description_key", 200, 3000, 10),
  (6, 3, 1, "name_key", "description_key", 0, 3000, 10);

INSERT INTO league_season_score (login_id, league_season_id, division_id, score, game_count) VALUES
  (1, 1, 1, 5, 5),
  (1, 2, 4, 3, 15),
  (1, 3, 6, 1200, 120),
  (2, 1, 2, 0, 15),
  (3, 2, 5, 5, 5);

