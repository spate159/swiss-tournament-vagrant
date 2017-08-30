-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here

create table player (id serial primary key,name text);

-- create table game (round integer, player_1 integer references player not null,  player_2 integer references player not null, winner integer references player CHECK (winner = player_1 or winner = player_2 or winner = NULL), primary key(player_1, player_2));


create table game (round integer, player_1 integer references player not null,  player_2 integer references player not null, winner integer references player not null CHECK (winner = player_1 or winner = player_2), primary key(player_1, player_2));

create unique index unique_pair
     on game (least(player_1, player_2), greatest(player_1, player_2));


CREATE VIEW standings AS
SELECT id, name, count(game.winner) AS wins, matches from
(SELECT player.id AS id, player.name AS name, count(game.winner) AS matches from player
LEFT JOIN game on player.id = game.player_1 or player.id = game.player_2 group by player.id)
AS games
LEFT JOIN game on id = game.winner group by id,name,matches order by wins desc;
