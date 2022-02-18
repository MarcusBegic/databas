PRAGMA foreign_keys=OFF;
--
-- DROP TABLE IF EXISTS chains;
-- CREATE TABLE chains (
--     c_name          TEXT,
--     PRIMARY KEY     (c_name)
-- );
--

DROP TABLE IF EXISTS theaters;
CREATE TABLE theaters (
    t_name      TEXT,
    capacity    INT,
    PRIMARY KEY (t_name)
);

DROP TABLE IF EXISTS screenings;
CREATE TABLE screenings (
    screening_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    start_time      TIME,
    start_date      DATE,
    t_name          TEXT,
    imdb_key        TEXT,
    FOREIGN KEY     (t_name) REFERENCES theaters(t_name),
    FOREIGN KEY     (imdb_key) REFERENCES movies(imdb_key),
    PRIMARY KEY     (screening_id)
);

DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
    m_title         TEXT,
    production_year TEXT,
    imdb_key        TEXT,
    PRIMARY KEY     (imdb_key)
);

DROP TABLE IF EXISTS tickets;
CREATE TABLE tickets (
    ticket_id       TEXT DEFAULT (lower(hex(randomblob(16)))),
    screening_id    INT,
    username        TEXT,
    PRIMARY KEY     (ticket_id),
    FOREIGN KEY     (screening_id) REFERENCES screenings(screening_id),
    FOREIGN KEY     (username) REFERENCES customers(username)
);

DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    username    TEXT,
    full_name   TEXT,
    pwd         TEXT,
    PRIMARY KEY (username)
);

