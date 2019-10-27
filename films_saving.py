import json
from mysql.connector import connect

film_database_connection = connect(host='127.0.0.1', port=3306, use_pure=True,
                                   user='root', password='asdfghjkl228', database='films_db')

film_database_cursor = film_database_connection.cursor(dictionary=True,
                                                       buffered=True)


def save_films_to_db():

    films_info = json.load(open('FilmsScrapping/FilmsScrapping/films_info_in_json.json', 'r'))
    film_database_cursor.execute("DESC films_db.films")
    films_info_columns = [column_info['Field'] for column_info in film_database_cursor.fetchall()]

    index = 1
    for info_about_film in films_info:

        columns = [column for column in info_about_film.keys() if column in films_info_columns]
        values = ["'" + str(info_about_film[column]) + "'" for column in columns]
        columns_to_sql = ', '.join(columns)
        values_to_sql = ', '.join(values)
        try:
            film_database_cursor.execute("INSERT INTO films_db.films(%s) VALUES(%s)" % (columns_to_sql, values_to_sql))
        except Exception:
            index += 1
            continue

        try:
            add_actors_to_db(info_about_film['actors'])
            add_genre_to_db(info_about_film['genre'])
            add_country_to_db(info_about_film['country'])
            create_relationships_film_actor(index, info_about_film['actors'])
            create_relationships_film_genre(index, info_about_film['genre'])
            create_relationships_film_country(index, info_about_film['country'])
        except Exception:
            index += 1
            continue

        index += 1


def add_actors_to_db(actors_list):
    if not actors_list:
        return

    for actor_name in actors_list:
        try:
            film_database_cursor.execute(f"SELECT 1 FROM films_db.actors WHERE name='{actor_name}'")
            if not film_database_cursor.fetchall():
                film_database_cursor.execute(f"INSERT INTO films_db.actors(name) VALUES ('{actor_name}')")
        except Exception:
            continue

    film_database_connection.commit()


def add_genre_to_db(genre_list):
    if not genre_list:
        return

    for genre_name in genre_list:
        try:
            film_database_cursor.execute(f"SELECT 1 FROM films_db.genres WHERE genre_name='{genre_name}'")
            if not film_database_cursor.fetchall():
                film_database_cursor.execute(f"INSERT INTO films_db.genres(genre_name) VALUES ('{genre_name}')")
        except Exception:
            continue
    film_database_connection.commit()


def add_country_to_db(country_list):

    if not country_list:
        return

    for country in country_list:
        try:
            film_database_cursor.execute(f"SELECT 1 FROM films_db.countries WHERE name='{country}'")

            if not film_database_cursor.fetchall():
                film_database_cursor.execute(f"INSERT INTO films_db.countries(name) VALUES ('{country}')")
        except Exception:
            continue

    film_database_connection.commit()


def create_relationships_film_country(film_id, list_of_countries):
    countries_placeholders = ', '.join(['%s'] * len(list_of_countries))

    try:
        film_database_cursor.execute("SELECT country_id FROM films_db.countries "
                                     "WHERE name IN (%s)" % countries_placeholders,
                                     tuple(list_of_countries))
    except Exception:
        return

    countries_ids = [country_info['country_id'] for country_info in film_database_cursor.fetchall()]
    for country_id in countries_ids:
        film_database_cursor.execute(f"INSERT INTO films_db.film_country(film_id, country_id) "
                                     f"VALUES ({film_id}, {country_id})")
    film_database_connection.commit()


def create_relationships_film_genre(film_id, list_of_genres):
    genres_placeholders = ', '.join(['%s'] * len(list_of_genres))

    try:
        film_database_cursor.execute("SELECT genre_id FROM films_db.genres "
                                     "WHERE genre_name IN (%s)" % genres_placeholders,
                                     tuple(list_of_genres))
    except Exception:
        return

    genres_ids = [genre_info['genre_id'] for genre_info in film_database_cursor.fetchall()]
    for genre_id in genres_ids:
        film_database_cursor.execute(f"INSERT INTO films_db.film_genre(film_id, genre_id) "
                                     f"VALUES ({film_id}, {genre_id})")
    film_database_connection.commit()


def create_relationships_film_actor(film_id, list_of_actors):
    actor_placeholders = ', '.join(['%s'] * len(list_of_actors))

    try:
        film_database_cursor.execute("SELECT actor_id FROM films_db.actors "
                                     "WHERE name IN (%s)" % actor_placeholders,
                                     tuple(list_of_actors))
    except Exception:
        return

    actors_ids = [actor_info['actor_id'] for actor_info in film_database_cursor.fetchall()]
    for actor_id in actors_ids:
        film_database_cursor.execute(f"INSERT INTO films_db.film_actors(film_id, actor_id) "
                                     f"VALUES ({film_id}, {actor_id})")

    film_database_connection.commit()

save_films_to_db()
