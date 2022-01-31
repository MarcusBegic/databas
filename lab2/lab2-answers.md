## lab 2 answers

### 4
#### a) 
Which relations have natural keys?
theater: primary(theater_name)
theater_chain: primary(chain_name)
ticket: primary(id)
screening: primary(id)
movie: primary(movie_title), composite(movie_title, production_year)
customer: primary(user_name)

foreign key is required for customer <-> ticket, theater<->screening, 

#### b) Is there a risk that any of the natural keys will ever change?
All natural keys for the movie will remain stagnant, same goes for the screening and ticket. The customer might change his name at some point, the theater_chain might change their name and same goes for the theater. 

#### c) Are there any weak entity sets?
The weak entity set we have is the movie being displayed for each screening. Since we only have the movie_title we cannot deduce which exact movie it is. We have uniqueness on title for each calendar year but there are many years. 

Ticket and Screening

#### d) In which relations do you want to use an invented key. Why?
We want to use a foreign key in screening, the movie_id attribute, as defined in the movie table. This is due to the uniqueness problem we bump into with non-unique movie titles. 

Otherwise we would like to create an invented key for the ticket ID. This is so competitors cannot deduce how many ticket we are selling at a given theater.

Might have to invent a key for the screening and theater relation

### 6

theater_chain(_chain_name_)
theater(/_chain_name_/, _theater_name_, capacity)
screening(end_time, start_time, ,_screen_id_, /_movie_name_/, /_production_year_/)
ticket(_ticket_id, /_screen_id_/, /_user_name_/)
customer(full_name, _user_name_, password)
movie(_movie_title_, _production_year_, running_time, imdb_key, _movie_id_)

### 7
For keeping track of the number of seats available could be:

##### 1)
Keeping track of one integer which is decremented when a new ticket is bought.

##### 2)
Keeping track of a sort of transaction list. I.e. we could have a log containing a ticket purchase by customer with user_name and ticket_id. This procedure is cleaner than keeping track of one int, since it gives us more information. 


