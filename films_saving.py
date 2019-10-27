import json
from mysql.connector import connect

film_database_connection = connect(host='127.0.0.1', port=3306, use_pure=True,
                                   user='root', password='asdfghjkl228', database='films_db')

film_database_cursor = film_database_connection.cursor(buffered=True,
                                                       dictionary=True)


def save_films_to_db():
    films_info = json.load(open('FilmsScrapping/FilmsScrapping/films_info_in_json.json', 'r'))
    pass


def add_actors_to_db(actors_list):
    for actor_name in actors_list:
        actor_exists_flag = film_database_cursor.execute(f"SELECT 1 FROM films_db.actors WHERE name={actor_name}")
        if not actor_exists_flag:
            film_database_cursor.execute(f"INSERT INTO films_db.actors(name) VALUES ('{actor_name}')")
    film_database_connection.commit()


def add_genre_to_db(genre_list):
    for genre_name in genre_list:
        genre_exists_flag = film_database_cursor.execute(f"SELECT 1 FROM films_db.genres WHERE genre_name={genre_name}")
        if not genre_exists_flag:
            film_database_cursor.execute(f"INSERT INTO films_db.genres(genre_name) VALUES ('{genre_name}')")
    film_database_connection.commit()