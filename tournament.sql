-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS players CASCADE;
DROP tABLE IF EXISTS matches CASCAD;

CREATE TABLE players(id SERIAL primary key, name TEXT);

CREATE TABLE matches(id SERIAL primary key,
                   winner INTEGER REFERENCES players(id),
                   loser INTEGER REFERENCES players(id));

CREATE VIEW standings AS
SELECT p.id as player_id, p.name as player_name,
(SELECT count(*) FROM matches WHERE matches.winner = p.id) as won,
(SELECT count(*) FROM matches WHERE p.id in (winner, loser)) as played
FROM players p
GROUP BY p.id
ORDER BY won DESC;
