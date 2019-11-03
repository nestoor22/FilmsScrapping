from elasticsearch import Elasticsearch
from work_with_db import clean_json_from_incomplete_data
import json

films_info = clean_json_from_incomplete_data(json.load(open('FilmsScrapping/FilmsScrapping/films_info_in_json.json',
                                                            'r')))
es_engine = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])


def save_films_actors_genres():
    for film_id, one_film in enumerate(films_info, start=1):
        es_engine.index(index='films_db', doc_type='films', id=film_id, body=one_film)


def save_actors():
    actor_id = 0
    genre_id = 0

    all_actors = set([one_actor for one_film in films_info for one_actor in one_film['actors']])
    all_genres = set([one_genre for one_film in films_info for one_genre in one_film['actors']])

    for one_actor in all_actors:
        actor_id += 1
        es_engine.index(index='actors_db', doc_type='actors', id=actor_id, body={'name': one_actor})

    for one_genre in all_genres:
        genre_id += 1
        es_engine.index(index='genres_db', doc_type='genres', id=genre_id, body={'name': one_genre})


print(es_engine.search(index="films_db", body={"query": {"match": {'name_eng': 'Avengers'}}}))