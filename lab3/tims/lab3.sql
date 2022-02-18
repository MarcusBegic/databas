PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS theater;
DROP TABLE IF EXISTS performance;
DROP TABLE IF EXISTS movie;
DROP TABLE IF EXISTS ticket;
DROP TABLE IF EXISTS customer;

PRAGMA foreign_keys=ON;

CREATE TABLE theater (
    t_name TEXT,
    capacity INT,
    PRIMARY KEY  (t_name)
);

CREATE TABLE movie (
    imdb_key TEXT,
    running_time INT,
    m_name TEXT,
    production_year DATE,
    PRIMARY KEY (imdb_key)
);

CREATE TABLE performance (
    performance_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    imdb_key TEXT,
    t_name TEXT,
    performance_date DATE,
    start_time TIME,
    FOREIGN KEY  (imdb_key) REFERENCES movie(imdb_key),
    FOREIGN KEY  (t_name) REFERENCES theater(t_name),
    PRIMARY KEY (performance_id)
);

CREATE TABLE ticket (
  ticket_id         TEXT DEFAULT (lower(hex(randomblob(16)))),
  performance_id    INT,
  c_user_name       TEXT,
  FOREIGN KEY  (performance_id) REFERENCES performance(performance_id),
  FOREIGN KEY  (c_user_name) REFERENCES customer(c_user_name)
  PRIMARY KEY  (ticket_id)
);


CREATE TABLE customer (
    c_user_name TEXT,
    full_name TEXT,
    c_password TEXT,
    PRIMARY KEY  (c_user_name)
);

INSERT
INTO    theater (t_name, capacity)
VALUES  ("SF_Lund", 500),
        ("SF_Malmö", 650),
        ("Kino_Lund", 350),
        ("Kino_Malmö", 550),
        ("FransFilm", 3);

INSERT
INTO    movie (imdb_key, running_time, m_name, production_year)
VALUES  ("tt0111161", 160, "The Shawshank Redemption", 1994),
        ("tt0068646", 180, "The Godfather", 1972),
        ("tt0071562", 210, "The Godfather: Part II", 1974),
        ("tt0468569", 105, "Pulp Fiction", 1994),
        ("tt0110912", 117, "Il buono, il brutto, il cattivo", 1966),
        ("tt0133093", 144, "Inception", 2010),
        ("tt0047478", 99, "12 Angry Men", 2000);

INSERT
INTO    performance (performance_date, imdb_key, start_time, t_name)
VALUES  ("2022-01-31", "tt0111161", "04:30", "SF_Lund"),
        ("2022-01-31", "tt0111161", "14:30", "SF_Malmö"),
        ("2022-01-31", "tt0111161", "18:30", "FransFilm"),
        ("2022-01-31", "tt0068646", "05:20", "Kino_Malmö"),
        ("2022-01-31", "tt0468569", "19:30", "Kino_Lund"),
        ("2022-02-03", "tt0468569", "19:30", "FransFilm"),
        ("2022-02-03", "tt0468569", "19:30", "Kino_Malmö"),
        ("2022-02-03", "tt0468569", "21:55", "Kino_Lund"),
        ("2022-01-17", "tt0110912", "15:30", "FransFilm"),
        ("2022-01-18", "tt0133093", "18:00", "SF_Lund"),
        ("2022-01-12", "tt0133093", "19:40", "Kino_Lund"),
        ("2022-01-01", "tt0068646", "19:20", "FransFilm"),
        ("2022-01-07", "tt0068646", "19:30", "Kino_Malmö"),
        ("2022-01-14", "tt0047478", "19:40", "Kino_Lund");

INSERT
INTO    customer (c_user_name, full_name, c_password)
VALUES  ("daniel123", "Daneil Andersson", "hej1234"),
        ("aleko1234", "Aleko Lilius", "halo1234"),
        ("tim1234", "Tim Jangenfeldt", "nihao1234"),
        ("alice", "Alice Lidell", "ecila"),
        ("bob", "Bob Hund", "bob"),
        ("carol", "Carol Christmas", "lorac"),
        ("frans1234", "Frans Sjöström", "hola1234");