-- CREATE DATABASE artist;
DROP TABLE IF EXISTS singer, song;
CREATE TABLE IF NOT EXISTS singer(
    id SERIAL PRIMARY KEY,
    name TEXT
);
CREATE TABLE IF NOT EXISTS song(
    id SERIAL PRIMARY KEY,
    name TEXT,
    id_singer SMALLINT REFERENCES singer ON DELETE SET NULL
);



INSERT INTO singer(name)
    VALUES
    ('Audioslave'),
    ('Mos Def'),
    ('Blackstar'),
    ('The Black Keys');




INSERT INTO song(name, id_singer)
    VALUES
    ('I am the highway', 1),
    ('Gasoline', 1),
    ('Mathematics', 2),
    ('Hip Hop', 2),
    ('Definition', 3),
    ('Gold on the Ceiling', 4),
    ('Hypnotic Girl',4);




