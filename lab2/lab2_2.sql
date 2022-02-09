PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS theater;
DROP TABLE IF EXISTS chains;
CREATE TABLE chains (
    c_name          TEXT,
    PRIMARY KEY     (c_name)
);

DROP TABLE IF EXISTS theaters;
CREATE TABLE theaters (
    t_name      TEXT,
    capacity    INT,
    PRIMARY KEY (t_name)
);

DROP TABLE IF EXISTS screenings;
CREATE TABLE screenings (
    screening_id    INTEGER,
    start_time      TIME,
    start_date      DATE,
    free_seats      INT,
    t_name          TEXT,
    m_title         TEXT,
    production_year INT,
    FOREIGN KEY     (t_name) REFERENCES theaters(t_name),
    FOREIGN KEY     (m_title, production_year) REFERENCES movies(m_title, production_year)
    PRIMARY KEY     (screening_id)
);

DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
    m_title         TEXT,
    production_year TEXT,
    duration        INT,
    imdb_key        TEXT,
    PRIMARY KEY     (m_title, production_year)
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
    c_name      TEXT,
    PRIMARY KEY (username),
    FOREIGN KEY (c_name) REFERENCES chains(c_name)
);

