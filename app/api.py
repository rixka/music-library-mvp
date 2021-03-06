from os import environ
from flask import Blueprint, request, abort
from pymongo import MongoClient

from utils import (
    json_response, validate_object_id,
    parse_query, validate_rating
)

MONGO_HOST = environ.get('MONGO_HOST') or 'localhost'
MONGO_DB = environ.get('MONGO_DB') or 'development'

api = Blueprint('api', __name__)
db = MongoClient(MONGO_HOST, 27017)[MONGO_DB]


@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def catch_all(path):
    abort(404)

@api.route('/health', methods=['GET'])
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

@api.route('/songs/avg/difficulty', methods=['GET'])
def songs_avg_difficulty():
    level = parse_query('level')
    query = { 'level': int(level) } if level else {}

    songs = list(
        db.songs.aggregate([
            {
                '$match': query
            },
            {
                '$group': {
                    '_id': 'null',
                    'avgDifficulty': { '$avg': '$difficulty' }
                }
            }
        ])
    )
    check_not_empty(songs)

    return json_response({
        'data': songs[0]
    })

@api.route('/songs/search', methods=['GET'])
def songs_search():
    message = parse_query('message')

    if not message:
        return songs_list()

    query = { '$text': { '$search': message } }
    songs = list(db.songs.find(query))
    check_not_empty(songs)

    return json_response({
        'data': songs
    })

@api.route('/songs/rating', methods=['POST'])
def create_songs_rating():
    data = request.json
    data['songId'] = validate_object_id(data['songId'])

    validate_rating(data['rating'])
    validate_song_exists(data['songId'])

    rating_id = db.ratings.insert(data)
    headers = { 'Location': str.join('/', [ '/songs/rating', str(rating_id) ]) }
    return json_response({ 'message': 'The item was created successfully' }, 201, headers)

@api.route('/songs/rating/<rating_id>', methods=['GET'])
def songs_rating(rating_id):
    rating_id = validate_object_id(rating_id)
    rating = list(db.ratings.find({ '_id': rating_id }).limit(1))
    check_not_empty(rating)

    return json_response({
        'data': rating[0]
    })

@api.route('/songs/avg/rating/<song_id>', methods=['GET'])
def songs_avg_rating(song_id):
    song_id = validate_object_id(song_id)
    validate_song_exists(song_id)

    rating = db.ratings.aggregate([
        {
            '$match': { 'songId': song_id }
        },
        {
            '$group': {
                '_id': '$songId',
                'minRating': { '$min': '$rating' },
                'avgRating': { '$avg': '$rating' },
                'maxRating': { '$max': '$rating' }
            }
        }
    ])

    return json_response({
        'data': rating
    })

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


# TODO: Move into a database module
def validate_song_exists(song_id):
    check_not_empty(
        list(
            db.songs.find({ '_id': song_id }, { '_id': 1 }).limit(1)
        )
    )

def check_not_empty(r):
    if r == []: abort(404)

