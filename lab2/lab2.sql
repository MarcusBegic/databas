
CREATE TABLE customer (
    full_name TEXT,
    user_name TEXT, 
    password TEXT
    PRIMARY KEY (user_name)
);

CREATE TABLE movie (
    movie_title TEXT,
    production_year INT,
    running_time INT,
    imdb_key TEXT,
    PRIMARY KEY (movie_title, production_year)    
);

CREATE TABLE screening (
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    screen_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    movie_title TEXT,
    production_year INT,
    seats INT,
    PRIMARY KEY (screen_id)
    FOREIGN KEY (movie_title) REFERENCES movie(movie_title),
    FOREIGN KEY (production_year) REFERENCES movie(production_year)
);

CREATE TABLE ticket (
    ticket_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    user_name TEXT,
    screen_id TEXT,
    FOREIGN KEY (user_name) REFERENCES customer(user_name),
    FOREIGN KEY (screen_id) REFERENCES screening(screen_id),
    PRIMARY KEY (ticket_id, user_name)
);

CREATE TABLE theater_chain (
    chain_name TEXT,    

    PRIMARY KEY(chain_name)    
);

CREATE TABLE theater (
    theater_name TEXT,
    capacity INT,
    chain_name TEXT,
    PRIMARY KEY(theater_name),
    FOREIGN KEY(chain_name) REFERENCES theater_chain(chain_name)
);