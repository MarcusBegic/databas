from bottle import get, post, run, request, response
import sqlite3
from urllib.parse import unquote
import hashlib

db = sqlite3.connect('movies.sqlite')



@get('/ping')
def get_pong():
    response.status = 200
    return 'pong\n'



def hash(msg):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

@post('/reset')
def post_reset():
    c = db.cursor()
    
    c.execute(
        """DELETE FROM theaters"""
    )  
    
    c.execute(
        """DELETE FROM screenings"""
    )    
    
    c.execute(
        """DELETE FROM movies"""
    )   
     
    c.execute(
        """DELETE FROM tickets"""
    )

    c.execute(
        """DELETE FROM customers"""
    )   
    
    
    c.execute(
        """
        INSERT
        INTO    theaters (t_name, capacity)
        VALUES  ("Kino", 10),
                ("Regal", 16),
                ("Skandia", 100);
        """
    )   
    
    response.status = 200
    return request.json

@post('/users')
def post_users():
    try:
        user = request.json
        c = db.cursor()
        print("here2")
        c.execute(
            """
            INSERT
            INTO       customers(username, full_name, pwd)
            VALUES     (?, ?, ?)
            RETURNING  username
            """,
            [user['username'], user['fullName'], hash(user['pwd'])]
        )
        print("here1")
        found = c.fetchone()
        print("here3")
        if not found:
            response.status = 400
            return "Illegal..."
        else:
            response.status = 201
            user_name, = found
            return f"/users/{user_name}\n"
    except:
        response.status = 400
        return ""


@post('/movies')
def post_movies():
    try:
        movie = request.json
        c = db.cursor()
        c.execute(
            """ 
            INSERT
            INTO        movies(m_title, imdb_key, production_year)
            VALUES      (?, ?, ?)
            RETURNING   imdb_key
            """,
            [movie['title'], movie['imdbKey'], movie['year']]
        )
        found = c.fetchone()
        if not found:
            response.status = 400
            return "Illegal..."
        else:
            response.status = 201
            imdb_key, = found
            return f"/movies/{imdb_key}\n"
    except:
        response.status = 400
        return ""
            
 

    
@post('/performances')
def post_performances():
    # -d '{"imdbKey": "tt5580390", "theater": "Kino", "date": "2021-02-22", "time": "19:00"}' -H "Content-Type: application/json"
    try:
        performance = request.json
        c = db.cursor()
        c.execute(
            """ 
            INSERT
            INTO        screenings (imdb_key, t_name, start_date, start_time)
            VALUES      (?, ?, ?, ?)
            RETURNING   screening_id
            """,
            [performance['imdbKey'], performance['theater'], performance['date'], performance['time']]
        )
        found = c.fetchone()
        if not found:
            response.status = 400
            return "Illegal..."
        else:
            response.status = 201
            screening_id, = found
            return f"/performances/{screening_id}\n"
    except:
        response.status = 400
        return "No such movie or theater"


@get('/movies')
def get_movies():
    # -d '{"imdbKey": "tt0111161", "title": "The Shawshank Redemption", "year": "1994"}' -H "Content-Type: application/json"
    query = """
            SELECT   imdb_key, m_title, production_year
            FROM     movies
            WHERE    1=1
            """
    
    params = []
    if request.query.title:
        query += " AND m_title = ?"
        params.append(unquote(request.query.title))
    if request.query.year:
        query += " AND production_year = ?"
        params.append(request.query.year)
        
    c = db.cursor()
    c.execute(query, params)
    found = [{"imdbKey": imdb_key, "title": m_title, "year": production_year}
            for imdb_key, m_title, production_year in c]
    response.status = 200
    return {"data": found}


@get('/movies/<imdb_key>')
def get_specific_movie(imdb_key):
    c = db.cursor()
    c.execute(
        """
        SELECT   imdb_key, m_title, production_year
        FROM     movies
        WHERE    imdb_key = ?
        """,
        [imdb_key]
    )
    found = [{"imdbKey": imdb_key, "title": m_title, "year": production_year}
             for imdb_key, m_title, production_year in c]
    response.status = 200
    return {"data": found}


@get('/performances')
def performances():
    c = db.cursor()
    c.execute(
        """
        WITH taken_seats AS (
            SELECT t_name, count(ticket_id) AS tickets_bought
            FROM screenings
            LEFT OUTER JOIN tickets
            USING (screening_id)
            GROUP BY screening_id
        )

        SELECT   DISTINCT screening_id, start_date, start_time, m_title, production_year, t_name, (capacity - tickets_bought) AS available_seats
        FROM     screenings
        JOIN     movies
        USING    (imdb_key)
        JOIN     taken_seats
        USING    (t_name)
        JOIN     theaters
        USING    (t_name)
        """
    )
    found = [{"performanceId": screening_id, "date": start_date, "startTime": start_time, "title": m_title, "year": production_year, "theater": t_name, "remainingSeats": available_seats}
            for screening_id, start_date, start_time, m_title, production_year, t_name, available_seats in c]
    response.status = 200
    return {"data": found}


@post('/tickets')
def post_tickets():
    # -d '{"username": "daniel123", "pwd": "hej1234", "performanceId": 1}' -H "Content-Type: application/json"
    try:
        c = db.cursor()
        
        ticket = request.json
        c.execute(
            """
            SELECT  username, pwd
            FROM    customers
            WHERE   username = ? AND pwd = ?
            """,
            [ticket['username'], hash(ticket['pwd'])]
        )
        found = c.fetchone()
        if not found:
            response.status = 401
            return "Wrong user credentials"
        
        c.execute(
            """
            WITH remaining_seats AS (
                SELECT t_name, count(ticket_id) AS tickets_bought
                FROM screenings
                LEFT OUTER JOIN tickets
                USING (screening_id)
                GROUP BY screening_id
            )

            SELECT  screening_id, (capacity - tickets_bought) AS available_seats
            FROM    screenings
            JOIN    remaining_seats
            USING   (t_name)
            JOIN    theaters
            USING   (t_name)
            WHERE   screening_id = ?
            """,
            [ticket['performanceId']]
        )
        remaining_seats = c.fetchone()[1]
        if remaining_seats == 0:
            response.status = 400
            return "No tickets left"
            
        c.execute(
            """     
            INSERT
            INTO        tickets (screening_id, username)
            VALUES      (?, ?)
            RETURNING   ticket_id
            """,
            [ticket['performanceId'], ticket['username']]
        )
        found = c.fetchone()
        if not found:
            response.status = 400
            return "Error"
        else:
            response.status = 201
            ticket_id = found
            return f"/tickets/{ticket_id}\n"
    except:
        response.status = 400
        return "Error"






run(host='localhost', port=7007)



