import json
from mysql.connector import connect

show_database_connection = connect(host='127.0.0.1', port=3306, use_pure=True,
                                   user='root', password='asdfghjkl228', database='films_db')

show_database_cursor = show_database_connection.cursor(dictionary=True,
                                                       buffered=True)


def save_films_to_db():
    films_info = json.load(open('new-films.json'))
    show_database_cursor.execute("DESC films_db.show")
    films_info_columns = [column_info['Field'] for column_info in show_database_cursor.fetchall()]
    index = 1
    for info_about_film in films_info:
        columns = [column for column in info_about_film.keys() if column in films_info_columns]
        values = ['"' + str(info_about_film[column]) + '"' for column in columns]
        columns_to_sql = ', '.join(columns)
        values_to_sql = ', '.join(values)
        try:
            show_database_cursor.execute("INSERT INTO films_db.show(%s) VALUES(%s)" % (columns_to_sql, values_to_sql))
        except:
            print("ERROR ADD SHOW")
            continue

        try:
            add_actors_to_db(info_about_film['cast'])
            create_relationships_show_actor(index, info_about_film['cast'])

            add_genre_to_db(info_about_film['genres'])
            create_relationships_show_genre(index, info_about_film['genres'])
        except:
            index += 1
            continue
        index += 1
        print("ADD:", info_about_film['title'])
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
            print("ERROR ADD ACTORS")
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
            print("ADD GENRE ERROR")
            continue
    show_database_connection.commit()


def create_relationships_show_genre(show_id, list_of_genres):
    genres_placeholders = ', '.join(['%s'] * len(list_of_genres))

    try:
        show_database_cursor.execute("SELECT genre_id FROM films_db.genres "
                                     "WHERE genre_name IN (%s)" % genres_placeholders,
                                     tuple(list_of_genres))
    except Exception:
        print("ERROR SHOW GENRE")
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
        print("ERROR SHOW ACTOR")
        return

    actors_ids = [actor_info['actor_id'] for actor_info in show_database_cursor.fetchall()]
    for actor_id in actors_ids:
        show_database_cursor.execute(f"INSERT INTO films_db.show_actors(show_id, actor_id) "
                                     f"VALUES ({show_id}, {actor_id})")

    show_database_connection.commit()


def count_films_for_actor():
    show_database_cursor.execute("""SELECT actor_id FROM films_db.actors ORDER BY actor_id""")
    all_actors_ids = show_database_cursor.fetchall()
    for ids in all_actors_ids:
        show_database_cursor.execute(f"SELECT COUNT(*) FROM films_db.show_actors WHERE actor_id={ids['actor_id']}")
        show_database_cursor.execute(f"UPDATE films_db.actors SET number_of_films="
                                     f"{show_database_cursor.fetchone()['COUNT(*)']} WHERE actor_id={ids['actor_id']}")


save_films_to_db()
