PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE voting_user (
    user_id integer primary key autoincrement,
    user_name text unique not null,
    pass_word text not null
);
INSERT INTO voting_user VALUES(1,'aldo','aldo');
INSERT INTO voting_user VALUES(2,'beppe','beppe');
INSERT INTO voting_user VALUES(3,'carlo','carlo');
INSERT INTO voting_user VALUES(4,'dario','dario');
INSERT INTO voting_user VALUES(5,'ernesto','ernesto');
INSERT INTO voting_user VALUES(6,'fabio','fabio');
CREATE TABLE votation
(
    votation_id integer primary key autoincrement,
    promoter_user_id integer not null,
    votation_description text unique not null,
    begin_date datetime not null,
    end_date datetime not null,
    votation_type text not null,
    votation_status integer not null
);
INSERT INTO votation VALUES(1,5,'Scelta del tè','2018-12-10 12:00','2018-12-17 12:00','maj_jud',1);
INSERT INTO votation VALUES(2,5,'Scelta vino','2018-12-10 12:00','2018-12-17 12:00','maj_jud',1);
CREATE TABLE guarantor
(
    votation_id integer,
    user_id integer,
    passphrase_ok integer not null,
    hash_ok integer not null,
    order_n integer,
    primary key (votation_id, user_id)
);
CREATE TABLE voting_option
(
    option_id integer PRIMARY KEY autoincrement,
    votation_id integer,
    option_name text,
    description text,
    unique  (votation_id, option_name)
);
INSERT INTO voting_option VALUES(1,1,'Oolong','');
INSERT INTO voting_option VALUES(2,1,'BOP','');
INSERT INTO voting_option VALUES(3,1,'Lapsang sounchong','');
INSERT INTO voting_option VALUES(4,1,'English breakfast','');
INSERT INTO voting_option VALUES(5,2,'Bianco','');
INSERT INTO voting_option VALUES(6,2,'Rosso','');
INSERT INTO voting_option VALUES(7,2,'Rosato','');
INSERT INTO voting_option VALUES(8,2,'Prosecco','');
CREATE TABLE voting_judgement
(
    votation_id integer,
    jud_value integer,
    jud_name text,
    description text,
    primary key (votation_id, jud_value)
);
CREATE TABLE vote
(
    vote_key text,
    votation_id integer,
    option_id integer ,
    jud_value integer,
    primary key (vote_key,votation_id, option_id)
);
INSERT INTO vote VALUES('b653ed506b996b812c2f5b010e20bd981f988c9de21b5b6523006e1cbe378cec',2,5,1);
INSERT INTO vote VALUES('b653ed506b996b812c2f5b010e20bd981f988c9de21b5b6523006e1cbe378cec',2,6,2);
INSERT INTO vote VALUES('b653ed506b996b812c2f5b010e20bd981f988c9de21b5b6523006e1cbe378cec',2,7,4);
INSERT INTO vote VALUES('b653ed506b996b812c2f5b010e20bd981f988c9de21b5b6523006e1cbe378cec',2,8,0);
INSERT INTO vote VALUES('530004a8303a0ed6c1155e81967e88b83df1f58f9e45b6f6fe1fff4c5fe73de9',2,5,3);
INSERT INTO vote VALUES('530004a8303a0ed6c1155e81967e88b83df1f58f9e45b6f6fe1fff4c5fe73de9',2,6,0);
INSERT INTO vote VALUES('530004a8303a0ed6c1155e81967e88b83df1f58f9e45b6f6fe1fff4c5fe73de9',2,7,5);
INSERT INTO vote VALUES('530004a8303a0ed6c1155e81967e88b83df1f58f9e45b6f6fe1fff4c5fe73de9',2,8,0);
INSERT INTO vote VALUES('8f0a3f2dfbee51fc3b5d597561eb2b6cf36c868d8b9aba5bb56e24444d08502d',2,5,5);
INSERT INTO vote VALUES('8f0a3f2dfbee51fc3b5d597561eb2b6cf36c868d8b9aba5bb56e24444d08502d',2,6,4);
INSERT INTO vote VALUES('8f0a3f2dfbee51fc3b5d597561eb2b6cf36c868d8b9aba5bb56e24444d08502d',2,7,3);
INSERT INTO vote VALUES('8f0a3f2dfbee51fc3b5d597561eb2b6cf36c868d8b9aba5bb56e24444d08502d',2,8,0);
INSERT INTO vote VALUES('ae739ced3994625d137ce2aff5b8126685f4f207b41bee63b165c10a7bdf6f4f',2,5,0);
INSERT INTO vote VALUES('ae739ced3994625d137ce2aff5b8126685f4f207b41bee63b165c10a7bdf6f4f',2,6,3);
INSERT INTO vote VALUES('ae739ced3994625d137ce2aff5b8126685f4f207b41bee63b165c10a7bdf6f4f',2,7,4);
INSERT INTO vote VALUES('ae739ced3994625d137ce2aff5b8126685f4f207b41bee63b165c10a7bdf6f4f',2,8,0);
INSERT INTO vote VALUES('b3199536d33a84c8277809e7aff84f4b85d5d50bd3b953e354659543e83ed4b0',2,5,3);
INSERT INTO vote VALUES('b3199536d33a84c8277809e7aff84f4b85d5d50bd3b953e354659543e83ed4b0',2,6,3);
INSERT INTO vote VALUES('b3199536d33a84c8277809e7aff84f4b85d5d50bd3b953e354659543e83ed4b0',2,7,3);
INSERT INTO vote VALUES('b3199536d33a84c8277809e7aff84f4b85d5d50bd3b953e354659543e83ed4b0',2,8,3);
INSERT INTO vote VALUES('6f419176f77807e6ebe24283f62d008c24da1cf8b1b8b38f2a0ebda2d9213ec3',2,5,3);
INSERT INTO vote VALUES('6f419176f77807e6ebe24283f62d008c24da1cf8b1b8b38f2a0ebda2d9213ec3',2,6,2);
INSERT INTO vote VALUES('6f419176f77807e6ebe24283f62d008c24da1cf8b1b8b38f2a0ebda2d9213ec3',2,7,5);
INSERT INTO vote VALUES('6f419176f77807e6ebe24283f62d008c24da1cf8b1b8b38f2a0ebda2d9213ec3',2,8,3);
CREATE TABLE voter
(
    user_id integer,
    votation_id integer,
    primary key (user_id,votation_id)
);
INSERT INTO voter VALUES(1,2);
INSERT INTO voter VALUES(2,2);
INSERT INTO voter VALUES(3,2);
INSERT INTO voter VALUES(4,2);
INSERT INTO voter VALUES(5,2);
INSERT INTO voter VALUES(6,2);

DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('voting_user',6);
INSERT INTO sqlite_sequence VALUES('votation',2);
INSERT INTO sqlite_sequence VALUES('voting_option',8);
COMMIT;
