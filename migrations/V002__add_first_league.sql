ALTER TABLE league_season ADD COLUMN name_key VARCHAR(255) NOT NULL AFTER leaderboard_id;

INSERT INTO leaderboard (id, technical_name) VALUES
  (1, "global"),
  (2, "ladder_1v1"),
  (3, "tmm_2v2");

INSERT INTO league (id, technical_name, name_key, description_key) VALUES
  (1, "TMM2v2League", "TMM2v2League.name", "TMM2v2League.description"),
  (2, "Ladder1v1League", "Ladder1v1League.name", "Ladder1v1League.description");

INSERT INTO league_season (id, league_id, leaderboard_id, name_key, start_date, end_date) VALUES
  (1, 1, 3, "TMM2v2League.season.1", NOW(), NULL),
  (2, 2, 2, "Ladder1v1League.season.1", NOW(), NULL);

INSERT INTO league_season_division (id, league_season_id, division_index, name_key, description_key) VALUES
  (1, 1, 1, "TMM2v2League.division.1.name", "TMM2v2League.division.1.description"),
  (2, 1, 2, "TMM2v2League.division.2.name", "TMM2v2League.division.2.description"),
  (3, 1, 3, "TMM2v2League.division.3.name", "TMM2v2League.division.3.description"),
  (4, 1, 4, "TMM2v2League.division.4.name", "TMM2v2League.division.4.description"),
  (5, 1, 5, "TMM2v2League.division.5.name", "TMM2v2League.division.5.description"),
  (6, 1, 6, "TMM2v2League.division.6.name", "TMM2v2League.division.6.description"),
  (7, 2, 1, "Ladder1v1League.division.1.name", "Ladder1v1League.division.1.description"),
  (8, 2, 2, "Ladder1v1League.division.2.name", "Ladder1v1League.division.2.description"),
  (9, 2, 3, "Ladder1v1League.division.3.name", "Ladder1v1League.division.3.description"),
  (10, 2, 4, "Ladder1v1League.division.4.name", "Ladder1v1League.division.4.description"),
  (11, 2, 5, "Ladder1v1League.division.5.name", "Ladder1v1League.division.5.description"),
  (12, 2, 6, "Ladder1v1League.division.6.name", "Ladder1v1League.division.6.description");

INSERT INTO league_season_division_subdivision (league_season_division_id, subdivision_index, name_key, description_key, min_rating, max_rating, highest_score) VALUES
  (1, 1, "TMM2v2League.subdivision.1.1.name", "TMM2v2League.subdivision.1.1.description", -1000, -600, 10),
  (1, 2, "TMM2v2League.subdivision.1.2.name", "TMM2v2League.subdivision.1.2.description", -600, -500, 10),
  (1, 3, "TMM2v2League.subdivision.1.3.name", "TMM2v2League.subdivision.1.3.description", -500, -400, 10),
  (1, 4, "TMM2v2League.subdivision.1.4.name", "TMM2v2League.subdivision.1.4.description", -400, -300, 10),
  (1, 5, "TMM2v2League.subdivision.1.5.name", "TMM2v2League.subdivision.1.5.description", -300, -200, 10),
  (2, 1, "TMM2v2League.subdivision.2.1.name", "TMM2v2League.subdivision.2.1.description", -200, -100, 10),
  (2, 2, "TMM2v2League.subdivision.2.2.name", "TMM2v2League.subdivision.2.2.description", -100, -0, 10),
  (2, 3, "TMM2v2League.subdivision.2.3.name", "TMM2v2League.subdivision.2.3.description", 0, 100, 10),
  (2, 4, "TMM2v2League.subdivision.2.4.name", "TMM2v2League.subdivision.2.4.description", 100, 200, 10),
  (2, 5, "TMM2v2League.subdivision.2.5.name", "TMM2v2League.subdivision.2.5.description", 200, 300, 10),
  (3, 1, "TMM2v2League.subdivision.3.1.name", "TMM2v2League.subdivision.3.1.description", 300, 400, 10),
  (3, 2, "TMM2v2League.subdivision.3.2.name", "TMM2v2League.subdivision.3.2.description", 400, 500, 10),
  (3, 3, "TMM2v2League.subdivision.3.3.name", "TMM2v2League.subdivision.3.3.description", 500, 600, 10),
  (3, 4, "TMM2v2League.subdivision.3.4.name", "TMM2v2League.subdivision.3.4.description", 600, 700, 10),
  (3, 5, "TMM2v2League.subdivision.3.5.name", "TMM2v2League.subdivision.3.5.description", 700, 800, 10),
  (4, 1, "TMM2v2League.subdivision.4.1.name", "TMM2v2League.subdivision.4.1.description", 800, 900, 10),
  (4, 2, "TMM2v2League.subdivision.4.2.name", "TMM2v2League.subdivision.4.2.description", 900, 1000, 10),
  (4, 3, "TMM2v2League.subdivision.4.3.name", "TMM2v2League.subdivision.4.3.description", 1000, 1100, 10),
  (4, 4, "TMM2v2League.subdivision.4.4.name", "TMM2v2League.subdivision.4.4.description", 1100, 1200, 10),
  (4, 5, "TMM2v2League.subdivision.4.5.name", "TMM2v2League.subdivision.4.5.description", 1200, 1300, 10),
  (5, 1, "TMM2v2League.subdivision.5.1.name", "TMM2v2League.subdivision.5.1.description", 1300, 1400, 10),
  (5, 2, "TMM2v2League.subdivision.5.2.name", "TMM2v2League.subdivision.5.2.description", 1400, 1500, 10),
  (5, 3, "TMM2v2League.subdivision.5.3.name", "TMM2v2League.subdivision.5.3.description", 1500, 1600, 10),
  (5, 4, "TMM2v2League.subdivision.5.4.name", "TMM2v2League.subdivision.5.4.description", 1600, 1700, 10),
  (5, 5, "TMM2v2League.subdivision.5.5.name", "TMM2v2League.subdivision.5.5.description", 1700, 1800, 10),
  (6, 1, "TMM2v2League.subdivision.6.1.name", "TMM2v2League.subdivision.6.1.description", 1800, 3000, 100),
  (7, 1, "Ladder1v1League.subdivision.1.1.name", "Ladder1v1League.subdivision.1.1.description", -1000, -600, 10),
  (7, 2, "Ladder1v1League.subdivision.1.2.name", "Ladder1v1League.subdivision.1.2.description", -600, -500, 10),
  (7, 3, "Ladder1v1League.subdivision.1.3.name", "Ladder1v1League.subdivision.1.3.description", -500, -400, 10),
  (7, 4, "Ladder1v1League.subdivision.1.4.name", "Ladder1v1League.subdivision.1.4.description", -400, -300, 10),
  (7, 5, "Ladder1v1League.subdivision.1.5.name", "Ladder1v1League.subdivision.1.5.description", -300, -200, 10),
  (8, 1, "Ladder1v1League.subdivision.2.1.name", "Ladder1v1League.subdivision.2.1.description", -200, -100, 10),
  (8, 2, "Ladder1v1League.subdivision.2.2.name", "Ladder1v1League.subdivision.2.2.description", -100, -0, 10),
  (8, 3, "Ladder1v1League.subdivision.2.3.name", "Ladder1v1League.subdivision.2.3.description", 0, 100, 10),
  (8, 4, "Ladder1v1League.subdivision.2.4.name", "Ladder1v1League.subdivision.2.4.description", 100, 200, 10),
  (8, 5, "Ladder1v1League.subdivision.2.5.name", "Ladder1v1League.subdivision.2.5.description", 200, 300, 10),
  (9, 1, "Ladder1v1League.subdivision.3.1.name", "Ladder1v1League.subdivision.3.1.description", 300, 400, 10),
  (9, 2, "Ladder1v1League.subdivision.3.2.name", "Ladder1v1League.subdivision.3.2.description", 400, 500, 10),
  (9, 3, "Ladder1v1League.subdivision.3.3.name", "Ladder1v1League.subdivision.3.3.description", 500, 600, 10),
  (9, 4, "Ladder1v1League.subdivision.3.4.name", "Ladder1v1League.subdivision.3.4.description", 600, 700, 10),
  (9, 5, "Ladder1v1League.subdivision.3.5.name", "Ladder1v1League.subdivision.3.5.description", 700, 800, 10),
  (10, 1, "Ladder1v1League.subdivision.4.1.name", "Ladder1v1League.subdivision.4.1.description", 800, 900, 10),
  (10, 2, "Ladder1v1League.subdivision.4.2.name", "Ladder1v1League.subdivision.4.2.description", 900, 1000, 10),
  (10, 3, "Ladder1v1League.subdivision.4.3.name", "Ladder1v1League.subdivision.4.3.description", 1000, 1100, 10),
  (10, 4, "Ladder1v1League.subdivision.4.4.name", "Ladder1v1League.subdivision.4.4.description", 1100, 1200, 10),
  (10, 5, "Ladder1v1League.subdivision.4.5.name", "Ladder1v1League.subdivision.4.5.description", 1200, 1300, 10),
  (11, 1, "Ladder1v1League.subdivision.5.1.name", "Ladder1v1League.subdivision.5.1.description", 1300, 1400, 10),
  (11, 2, "Ladder1v1League.subdivision.5.2.name", "Ladder1v1League.subdivision.5.2.description", 1400, 1500, 10),
  (11, 3, "Ladder1v1League.subdivision.5.3.name", "Ladder1v1League.subdivision.5.3.description", 1500, 1600, 10),
  (11, 4, "Ladder1v1League.subdivision.5.4.name", "Ladder1v1League.subdivision.5.4.description", 1600, 1700, 10),
  (11, 5, "Ladder1v1League.subdivision.5.5.name", "Ladder1v1League.subdivision.5.5.description", 1700, 1800, 10),
  (12, 1, "Ladder1v1League.subdivision.6.1.name", "Ladder1v1League.subdivision.6.1.description", 1800, 3000, 100);
