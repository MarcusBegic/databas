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
        c.execute(
            """
            INSERT
            INTO       customer(username, full_name, pwd)
            VALUES     (?, ?, ?)
            RETURNING  username
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
    try:
        movie = request.json
        c = db.cursor()
        c.execute(
            """ 
            INSERT
            INTO        movies (m_title, imdb_key, production_year)
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
            performance_id, = found
            return f"/performances/{screening_id}\n"
    except:
        response.status = 400
        return "No such movie or theater"


run(host='localhost', port=7007)



