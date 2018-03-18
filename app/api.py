import ast
from flask import Blueprint, abort

from pymongo import MongoClient
from utils import (
    json_response, validate_object_id, parse_query
)

api = Blueprint('api', __name__)
db = MongoClient('localhost', 27017).development
# TODO: ^^ fix


@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def catch_all(path):
    abort(404)

@api.route('/health')
def health():
    return json_response({'status': 'ok'}, 200)

@api.route('/songs')
def songs_list():
    last_id =  parse_query('last-id')
    query = { '_id': { '$gt': validate_object_id(last_id) } } if last_id else {}

    songs = db.songs.find(query).sort('_id').limit(5)
    return json_response({
        'data': songs
    })

@api.route('/songs/avg/difficulty')
def songs_avg_difficulty():
    level = parse_query('level')
    query = { 'level': level } if level else {}
    fields = { 'artist': 1, 'title': 1, 'difficulty': 1 }

    songs = list(db.songs.find(query, fields))

    if songs == []:
        abort(404)

    return json_response({
        'data': songs
    })

@api.route('/songs/search')
def songs_search():
    abort(501)

@api.route('/songs/avg/rating/<song_id>')
def songs_avg_rating(song_id):
    abort(501)


# === HANDLERS === #

@api.errorhandler(400)
def not_found(error):
    return json_response({'error': 'Bad Request'}, 400)

@api.errorhandler(404)
def not_found(error):
    return json_response({'error': 'Not Found'}, 404)

@api.errorhandler(500)
def internal_error(error):
    return json_response({'error': 'Internal Server Error'}, 500)

@api.errorhandler(501)
def not_implemented(error):
    return json_response({'error': 'Not Implemented'}, 501)

