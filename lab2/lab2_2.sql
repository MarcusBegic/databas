DROP TABLE IF EXISTS chains;
CREATE TABLE chains (
    c_name          TEXT,
    PRIMARY KEY     (c_name)
);

DROP TABLE IF EXISTS theater;
CREATE TABLE theater (
    t_name      TEXT,
    capacity    INT,
    PRIMARY KEY (t_name)
);

DROP TABLE IF EXISTS screenings;
CREATE TABLE screenings (
    screening_id    TEXT DEFAULT (lower(hex(randomblob(16)))),
    start_time      TIMESTAMP,
    t_name          TEXT,
    m_title         TEXT,
    production_year INT, 
    FOREIGN KEY     (t_name) REFERENCES theater(t_name),
    FOREIGN KEY     (m_title, production_year) REFERENCES movies(m_title, production_year)
    PRIMARY KEY     (start_time, t_name, m_title)
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
    screening_id    TEXT,
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
    PRIMARY KEY (username)
    FOREIGN KEY (c_name) REFERENCES chains(c_name)
);