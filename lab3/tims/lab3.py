from bottle import get, post, run, request, response
import sqlite3
from urllib.parse import unquote
import hashlib

# moviechain, theater, performance, movie, ticket, customer
db = sqlite3.connect('movies.sqlite')


def hash(msg):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()


@get('/ping')
def get_pong():
    response.status = 200
    return 'pong\n'

@post('/reset')
def post_reset():
    c = db.cursor()
    
    c.execute(
        """DELETE FROM theater"""
    )  
    
    c.execute(
        """DELETE FROM performance"""
    )    
    
    c.execute(
        """DELETE FROM movie"""
    )   
     
    c.execute(
        """DELETE FROM ticket"""
    )

    c.execute(
        """DELETE FROM customer"""
    )   
    
    
    c.execute(
        """
        INSERT
        INTO    theater (t_name, capacity)
        VALUES  ("Kino", 10),
                ("Regal", 16),
                ("Skandia", 100);
        """
    )   
    
    response.status = 200
    return request.json

@post('/users')
def post_users():
    # -d '{"username": "alice", "fullName": "Alice Lidell", "pwd": "aliceswaytoosimplepassword"}' -H "Content-Type: application/json"
    try:
        user = request.json
        c = db.cursor()
        c.execute(
            """
            INSERT
            INTO       customer(c_user_name, full_name, c_password)
            VALUES     (?, ?, ?)
            RETURNING  c_user_name
            """,
            [user['username'], user['fullName'], hash(user['pwd'])]
        )
        found = c.fetchone()
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
    # -d '{"imdbKey": "tt4975722", "title": "Moonlight", "year": 2016}' -H "Content-Type: application/json"
    try:
        movie = request.json
        c = db.cursor()
        c.execute(
            """ 
            INSERT
            INTO        movie (imdb_key, m_name, production_year)
            VALUES      (?, ?, ?)
            RETURNING   imdb_key
            """,
            [movie['imdbKey'], movie['title'], movie['year']]
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
            INTO        performance (imdb_key, t_name, performance_date, start_time)
            VALUES      (?, ?, ?, ?)
            RETURNING   performance_id
            """,
            [performance['imdbKey'], performance['theater'], performance['date'], performance['time']]
        )
        found = c.fetchone()
        if not found:
            response.status = 400
            return "Illegal..."
        else:
            response.status = 201
            performance_id, = found
            return f"/performances/{performance_id}\n"
    except:
        response.status = 400
        return "No such movie or theater"

@get('/movies')
def get_movies():
    # -d '{"imdbKey": "tt0111161", "title": "The Shawshank Redemption", "year": "1994"}' -H "Content-Type: application/json"
    query = """
            SELECT   imdb_key, m_name, production_year
            FROM     movie
            WHERE    1 = 1
            """
    
    params = []
    if request.query.title:
        query += " AND m_name = ?"
        params.append(unquote(request.query.title))
    if request.query.year:
        query += " AND production_year = ?"
        params.append(request.query.year)
        
    c = db.cursor()
    c.execute(query, params)
    found = [{"imdbKey": imdb_key, "title": m_name, "year": production_year}
            for imdb_key, m_name, production_year in c]
    response.status = 200
    return {"data": found}

@get('/movies/<imdb_key>')
def get_specific_movie(imdb_key):
    c = db.cursor()
    c.execute(
        """
        SELECT   imdb_key, m_name, production_year
        FROM     movie
        WHERE    imdb_key = ?
        """,
        [imdb_key]
    )
    found = [{"imdbKey": imdb_key, "title": m_name, "year": production_year}
             for imdb_key, m_name, production_year in c]
    response.status = 200
    return {"data": found}

@get('/performances')
def performances():
    c = db.cursor()
    c.execute(
        """
        WITH taken_seats AS (
            SELECT t_name, count(ticket_id) AS tickets_bought
            FROM performance
            LEFT OUTER JOIN ticket
            USING (performance_id)
            GROUP BY performance_id
        )

        SELECT   DISTINCT performance_id, performance_date, start_time, m_name, production_year, t_name, (capacity - tickets_bought) AS available_seats
        FROM     performance
        JOIN     movie
        USING    (imdb_key)
        JOIN     taken_seats
        USING    (t_name)
        JOIN     theater
        USING    (t_name)
        """
    )
    found = [{"performanceId": performance_id, "date": performance_date, "startTime": start_time, "title": m_name, "year": production_year, "theater": t_name, "remainingSeats": available_seats}
            for performance_id, performance_date, start_time, m_name, production_year, t_name, available_seats in c]
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
            SELECT  c_user_name, c_password
            FROM    customer
            WHERE   c_user_name = ? AND c_password = ?
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
                FROM performance
                LEFT OUTER JOIN ticket
                USING (performance_id)
                GROUP BY performance_id
            )

            SELECT  performance_id, (capacity - tickets_bought) AS available_seats
            FROM    performance
            JOIN    remaining_seats
            USING   (t_name)
            JOIN    theater
            USING   (t_name)
            WHERE   performance_id = ?
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
            INTO        ticket (performance_id, c_user_name)
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
    
@get('/users/<username>/tickets')
def get_username_tickets(username):
    c = db.cursor()
    c.execute(
        """
        SELECT   performance_date, start_time, t_name, m_name, production_year, count(ticket_id) AS tickets_bought
        FROM     performance
        JOIN     movie
        USING    (imdb_key)
        LEFT     OUTER JOIN ticket
        USING    (performance_id)
        WHERE    c_user_name = ?
        GROUP BY performance_id
        """,
        [username]
    )
    found = [{"date": performance_date, "startTime": start_time, "theater": t_name, "title": m_name, "year": production_year, "nbrOfTickets": tickets_bought}
             for performance_date, start_time, t_name, m_name, production_year, tickets_bought in c]
    response.status = 200
    return {"data": found}
    


run(host='localhost', port=7007)