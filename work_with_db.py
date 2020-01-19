import json
from mysql.connector import connect

show_database_connection = connect(host='127.0.0.1', port=3306, use_pure=True,
                                   user='root', password='asdfghjkl228', database='films_db')

show_database_cursor = show_database_connection.cursor(dictionary=True,
                                                       buffered=True)

show_database_cursor.execute("""SELECT name_rus FROM films_db.show""")
films_list = [name['name_rus'] for name in show_database_cursor.fetchall()]


def clean_json_from_incomplete_data(json_info):
    all_columns_in_json = ['poster_url', 'name_rus', 'name_eng', 'imdb_rating',
                           'release_date', 'country', 'genre', 'plot',
                           'actors_eng', 'actors_rus', 'showtype']

    for one_json in json_info:
        if not all([column in one_json.keys() for column in all_columns_in_json]):
            json_info.remove(one_json)

    return json_info


def save_films_to_db():

    films_info = clean_json_from_incomplete_data(json.load(open('films_info_in_json.json')))
    show_database_cursor.execute("DESC films_db.show")
    films_info_columns = [column_info['Field'] for column_info in show_database_cursor.fetchall()]

    index = 1
    for info_about_film in films_info:
        print(info_about_film)
        columns = [column for column in info_about_film.keys() if column in films_info_columns]
        values = ["'" + str(info_about_film[column]) + "'" for column in columns]
        columns_to_sql = ', '.join(columns)
        values_to_sql = ', '.join(values)

        try:
            show_database_cursor.execute("INSERT INTO films_db.show(%s) VALUES(%s)" % (columns_to_sql, values_to_sql))
        except Exception:
            print('ERROR')
            continue
        try:
            add_actors_to_db(info_about_film['actors_eng'])
            create_relationships_show_actor(index, info_about_film['actors_eng'])

            add_genre_to_db(info_about_film['genre'])
            create_relationships_show_genre(index, info_about_film['genre'])

            add_country_to_db(info_about_film['country_eng'])
            create_relationships_show_country(index, info_about_film['country_eng'])
        except:
            index += 1
            continue
        index += 1

    count_films_for_actor()
    show_database_connection.commit()


def add_actors_to_db(actors_list):
    if not actors_list:
        return

    for actor_name in actors_list:
        try:
            show_database_cursor.execute(f"SELECT 1 FROM films_db.actors WHERE name='{actor_name}'")
            if not show_database_cursor.fetchall():
                show_database_cursor.execute(f"INSERT INTO films_db.actors(name) VALUES ('{actor_name}')")
        except Exception:
            continue

    show_database_connection.commit()


def add_genre_to_db(genre_list):
    if not genre_list:
        return

    for genre_name in genre_list:
        try:
            show_database_cursor.execute(f"SELECT 1 FROM films_db.genres WHERE genre_name='{genre_name}'")
            if not show_database_cursor.fetchall():
                show_database_cursor.execute(f"INSERT INTO films_db.genres(genre_name) VALUES ('{genre_name}')")
        except Exception:
            continue
    show_database_connection.commit()


def add_country_to_db(country_list):

    if not country_list:
        return

    for country in country_list:
        try:
            show_database_cursor.execute(f"SELECT 1 FROM films_db.countries WHERE name='{country}'")

            if not show_database_cursor.fetchall():
                show_database_cursor.execute(f"INSERT INTO films_db.countries(name) VALUES ('{country}')")
        except Exception:
            continue

    show_database_connection.commit()


def create_relationships_show_country(show_id, list_of_countries):
    countries_placeholders = ', '.join(['%s'] * len(list_of_countries))

    try:
        show_database_cursor.execute("SELECT country_id FROM films_db.countries "
                                     "WHERE name IN (%s)" % countries_placeholders,
                                     tuple(list_of_countries))
    except Exception:
        return

    countries_ids = [country_info['country_id'] for country_info in show_database_cursor.fetchall()]
    for country_id in countries_ids:
        show_database_cursor.execute(f"INSERT INTO films_db.show_country(show_id, country_id) "
                                     f"VALUES ({show_id}, {country_id})")
    show_database_connection.commit()


def create_relationships_show_genre(show_id, list_of_genres):
    genres_placeholders = ', '.join(['%s'] * len(list_of_genres))

    try:
        show_database_cursor.execute("SELECT genre_id FROM films_db.genres "
                                     "WHERE genre_name IN (%s)" % genres_placeholders,
                                     tuple(list_of_genres))
    except Exception:
        return

    genres_ids = [genre_info['genre_id'] for genre_info in show_database_cursor.fetchall()]
    for genre_id in genres_ids:
        show_database_cursor.execute(f"INSERT INTO films_db.show_genre(show_id, genre_id) "
                                     f"VALUES ({show_id}, {genre_id})")
    show_database_connection.commit()


def create_relationships_show_actor(show_id, list_of_actors):
    actor_placeholders = ', '.join(['%s'] * len(list_of_actors))

    try:
        show_database_cursor.execute("SELECT actor_id FROM films_db.actors "
                                     "WHERE name IN (%s)" % actor_placeholders,
                                     tuple(list_of_actors))
    except Exception:
        return

    actors_ids = [actor_info['actor_id'] for actor_info in show_database_cursor.fetchall()]
    for actor_id in actors_ids:
        show_database_cursor.execute(f"INSERT INTO films_db.show_actors(show_id, actor_id) "
                                     f"VALUES ({show_id}, {actor_id})")

    show_database_connection.commit()


def get_actors_for_film(show_name):
    show_database_cursor.execute(f"SELECT name from films_db.actors "
                                 f"JOIN films_db.show_actors ON actors.actor_id = show_actors.actor_id "
                                 f"JOIN films_db.show ON films_db.show.show_id=show_actors.show_id"
                                 f" WHERE show.name_rus='{show_name}'")

    list_of_actors = [actor_dict['name'] for actor_dict in show_database_cursor.fetchall()]
    return list_of_actors


def get_genres_for_film(show_name):
    show_database_cursor.execute(f"SELECT genre_name from films_db.genres "
                                 f"JOIN films_db.show_genre ON genres.genre_id = show_genre.genre_id "
                                 f"JOIN films_db.show ON films_db.show.show_id=show_genre.show_id"
                                 f" WHERE show.name_rus='{show_name}'")
    list_of_genres = [genre_dict['genre_name'] for genre_dict in show_database_cursor.fetchall()]
    return list_of_genres


def get_countries_for_film(show_name):
    show_database_cursor.execute(f"SELECT name from films_db.countries "
                                 f"JOIN films_db.show_country ON countries.country_id = show_country.country_id "
                                 f"JOIN films_db.show ON films_db.show.show_id=show_country.show_id"
                                 f" WHERE show.name_rus='{show_name}'")
    list_of_countries = [country_dict['name'] for country_dict in show_database_cursor.fetchall()]

    return list_of_countries


def get_best_rated_films_with_parameters(limit=5, **kwargs):
    sql_query = f"SELECT * from films_db.show "

    for column, value in kwargs.items():
        if column == 'actors':
            actor_placeholders = ', '.join(['%s'] * len(kwargs['actors']))

            sql_query += f"JOIN show_actors ON show_actors.show_id = show.show_id " \
                         f"JOIN actors ON actors.actor_id = show_actors.actor_id " \
                         f"AND actors.name IN (%s) " % actor_placeholders
            sql_query %= ','.join("'" + str(value) + "'" for value in kwargs['actors'])

        elif column == 'genres':
            genres_placeholders = ', '.join(['%s'] * len(kwargs['genres']))

            sql_query += f"JOIN show_genre ON show_genre.show_id = show.show_id " \
                         f"JOIN genres ON genres.genre_id = show_genre.genre_id " \
                         f"AND genres.genre_name IN (%s) " % genres_placeholders
            sql_query %= ','.join("'" + str(value) + "'" for value in kwargs['genres'])

        elif column == 'countries':
            countries_placeholders = ', '.join(['%s'] * len(kwargs['countries']))
            sql_query += f"JOIN show_country ON show_country.show_id = show.show_id " \
                         f"JOIN countries ON countries.country_id =show_country.country_id " \
                         f"AND countries.name IN (%s) " % countries_placeholders

            sql_query %= ','.join("'" + str(value) + "'" for value in kwargs['countries'])

    sql_query += f"ORDER BY imdb_rating DESC LIMIT {limit}"

    return show_database_cursor.execute(sql_query)


def count_films_for_actor():
    show_database_cursor.execute("""SELECT actor_id FROM films_db.actors ORDER BY actor_id""")
    all_actors_ids = show_database_cursor.fetchall()
    for ids in all_actors_ids:
        show_database_cursor.execute(f"SELECT COUNT(*) FROM films_db.show_actors WHERE actor_id={ids['actor_id']}")
        show_database_cursor.execute(f"UPDATE films_db.actors SET number_of_films="
                                     f"{show_database_cursor.fetchone()['COUNT(*)']} WHERE actor_id={ids['actor_id']}")


save_films_to_db()
