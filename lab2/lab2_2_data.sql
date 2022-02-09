INSERT
INTO   chains(c_name)
VALUES ('Filmstaden');

INSERT
INTO    theaters(t_name, capacity)
VALUES  ('Filmstaden Lund', 100),
        ('Storgatan', 300),
        ('Royal', 500),
        ('Entre', 500);

INSERT
INTO    movies(m_title, production_year, duration, imdb_key)
VALUES  ('The Lord of the Rings: The Fellowship of the Ring', 2001, 178, 'tt0120737'),
        ('Snatch', 2000, 102, 'tt0208092'),
        ('Batman Begins', 2005, 140, 'tt0372784'),
        ('Demon Slayer: Mugen Train', 2020, 117, 'tt11032374'),
        ('Monty Python and the Holy Grail', 1975, 91, 'tt0071853');

INSERT
INTO    screenings(start_date, start_time, t_name, free_seats, m_title, production_year)
VALUES  ('2022-02-01', '19:30', 'Filmstaden Lund', 100, 'Demon Slayer: Mugen Train', 2020),
        ('2022-02-01', '20:30', 'Royal', 500, 'Snatch', 2000),
        ('2022-02-01', '20:30', 'Storgatan', 300, 'Monty Python and the Holy Grail', 1975),
        ('2022-02-01', '20:30', 'Entre', 500, 'Batman Begins', 2005);

INSERT
INTO    tickets(screening_id, username)
VALUES  (1, 'marcusoft'),
        (1, 'axley'),
        (2, 'marcusoft'),
        (2, 'stifi'),
        (3, 'Greven'),
        (3, 'axley'),
        (3, 'sollerito'),
        (3, 'MrFiskpinnar'),
        (4, 'marcusoft'),
        (4, 'Sollerito');

INSERT
INTO    customers(username, full_name, pwd, c_name)
VALUES  ('marcusoft', 'marcusbegic','kingen123', 'Filmstaden'),
        ('stifi', 'dylanfrost','somethingstrange','Filmstaden'),
        ('axley', 'axelbengtsson','mari6969','Filmstaden'),
        ('Greven', 'FredrikHornDannertAfAminne','pleb','Filmstaden'),
        ('Sollerito', 'MaxSoller','bayern','Filmstaden'),
        ('MrFiskpinnar', 'HenkeRasmusson','obiOneknobe','Filmstaden');