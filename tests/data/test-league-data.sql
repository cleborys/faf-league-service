DELETE FROM league_season_score;
DELETE FROM league_season_division_subdivision;
DELETE FROM league_season_division;
DELETE FROM league_season;
DELETE FROM league;

INSERT INTO league (id, technical_name, name_key, description_key) VALUES
  (1, "test_league", "L1", "description_key"),
  (2, "second_test_league", "L2", "description_key"),
  (3, "league_without_seasons", "L3", "description_key");

INSERT INTO league_season (id, league_id, leaderboard_id, start_date, end_date) VALUES
  (1, 1, 1, NOW() - interval 2 year, NOW() - interval 1 year),
  (2, 1, 1, NOW() - interval 1 year, NULL),
  (3, 2, 2, NOW() - interval 2 year, NULL);

INSERT INTO league_season_division (id, league_season_id, division_index, name_key, description_key) VALUES
  (1, 1, 1, "L1D1", "description_key"),
  (2, 1, 2, "L1D2", "description_key"),
  (3, 2, 1, "L2D1", "description_key"),
  (4, 2, 2, "L2D2", "description_key"),
  (5, 2, 3, "L2D3", "description_key"),
  (6, 3, 1, "L3D1", "description_key");

INSERT INTO league_season_division_subdivision (id, league_season_division_id, subdivision_index, name_key, description_key, min_rating, max_rating, highest_score) VALUES
  (1, 1, 1, "L1D1S1", "description_key", 0, 150, 10),
  (2, 2, 1, "L1D2S1", "description_key", 150, 3000, 10),
  (3, 3, 1, "L2D1S1", "description_key", 0, 100, 10),
  (4, 3, 2, "L2D1S2", "description_key", 100, 200, 10),
  (5, 4, 1, "L2D2S1", "description_key", 200, 300, 10),
  (6, 4, 2, "L2D2S2", "description_key", 300, 400, 10),
  (7, 5, 1, "L2D3S1", "description_key", 400, 500, 10),
  (8, 5, 2, "L2D3S2", "description_key", 500, 600, 100),
  (9, 6, 1, "L3D1S1", "description_key", 0, 3000, 10);

INSERT INTO league_season_score (login_id, league_season_id, subdivision_id, score, game_count) VALUES
  (1, 1, 1, 5, 5),
  (1, 2, 5, 3, 15),
  (1, 3, 9, 1200, 120),
  (2, 1, 2, 0, 15),
  (3, 2, 8, 5, 5);
