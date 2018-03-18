import pytest

from flask import url_for
from jsonschema import validate
from bson.json_util import dumps
from bson.objectid import ObjectId

from app.utils import JSON_MIME_TYPE
from common import MongoSystemTest, build_query

"""
These tests required MongoDB to be running locally.

    To setup MongoDB:     `make docker-up`
    To setup Virtual Env: `make venv`
    To run the tests:     `make test`

"""


class TestMisc(object):
    def test_health(self, client):
        res = client.get(url_for('api.health'))

        assert res.status_code == 200
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'status': 'ok' }

    def test_not_found(self, client):
        res = client.get('/')

        assert res.status_code == 404
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Not Found' }


class TestSongsAPI(MongoSystemTest):

    @classmethod
    def setup_class_custom(cls):
        cls.api = 'api.songs_list'

        cls.last_id = str(cls.song_ids[-1]['_id'])

        cls.schema = {
          'type': 'array',
          'items': {
            'type': 'object',
            'properties': {
              'artist': { 'type': 'string' },
              'title': { 'type': 'string' },
              'difficulty': { 'type': 'number' },
              'level': { 'type': 'integer' },
              'released': { 'type': 'string' }
            },
            'required': [ 'artist', 'title', 'released' ]
          }
        }

    def test_list(self, client):
        res = client.get(url_for(self.api))

        assert res.status_code == 200
        assert res.mimetype == JSON_MIME_TYPE
        assert validate(res.json['data'], self.schema) is None
        assert len(res.json['data']) == 5

    def test_list_paginate(self, client):
        res_orig = client.get(url_for(self.api))
        last_id = res_orig.json['data'][-1]['_id']['$oid']

        res = client.get(
            build_query(self.api, [ '?last-id=', last_id ])
        )

        assert res.status_code == 200
        assert res.mimetype == JSON_MIME_TYPE
        assert validate(res.json['data'], self.schema) is None
        assert res_orig.json != res.json

    def test_list_bad_id(self, client):
        res = client.get(
            build_query(self.api, [ '?last-id=123' ])
        )

        assert res.status_code == 400
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Bad Request' }

    def test_list_id_not_found(self, client):
        res = client.get(
            build_query(self.api, [ '?last-id=5abd9fbcd48b40737d3c14db' ])
        )

        assert res.status_code == 200
        assert res.mimetype == JSON_MIME_TYPE

        # When an `_id` cannot be found or is the last `_id` in the collection
        # and empty array will be returned
        assert res.json['data'] == []


class TestDifficultyAPI(object):

    @classmethod
    def setup_class(cls):
        cls.api = 'api.songs_avg_difficulty'
        cls.schema = {
          'type': 'array',
          'items': {
            'type': 'object',
            'properties': {
              '_id': { 'type': 'object' },
              'artist': { 'type': 'string' },
              'title': { 'type': 'string' },
              'difficulty': { 'type': 'number' },
            },
            'required': [ 'artist', 'title', 'difficulty' ],
            'additionalProperties': False
          }
        }

    def test_avg_difficulty_level_query(self, client):
        res = client.get(
            build_query(self.api, [ '?level=6' ])
        )

        assert res.status_code == 200
        assert res.mimetype == JSON_MIME_TYPE
        assert validate(res.json['data'], self.schema) is None
        assert len(res.json['data']) == 2

    def test_avg_difficulty_level_not_found(self, client):
        res = client.get(
            build_query(self.api, [ '?level=10000' ])
        )

        assert res.status_code == 404
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Not Found' }

    def test_avg_difficulty(self, client):
        res = client.get(url_for(self.api))

        assert res.status_code == 200
        assert res.mimetype == JSON_MIME_TYPE
        assert validate(res.json['data'], self.schema) is None


class TestSongsSearchAPI(object):

    @classmethod
    def setup_class(cls):
        cls.api = 'api.songs_search'
        cls.schema = {
          'type': 'array',
          'items': {
            'type': 'object',
            'properties': {
              'artist': { 'type': 'string' },
              'title': { 'type': 'string' },
              'difficulty': { 'type': 'number' },
              'level': { 'type': 'integer' },
              'released': { 'type': 'string' }
            },
            'required': [ 'artist', 'title', 'released' ]
          }
        }

    def test_search(self, client):
        res = client.get(
            build_query(self.api, [ '?message=fastfinger' ])
        )

        assert res.status_code == 200
        assert res.mimetype == JSON_MIME_TYPE
        assert validate(res.json['data'], self.schema) is None

    def test_search_no_message(self, client):
        res = client.get(url_for(self.api))

        assert res.status_code == 200
        assert res.mimetype == JSON_MIME_TYPE
        assert validate(res.json['data'], self.schema) is None

    def test_search_not_found(self, client):
        res = client.get(
            build_query(self.api, [ '?message=foobar' ])
        )

        assert res.status_code == 404
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Not Found' }


class TestCreateSongsRatingsAPI(MongoSystemTest):

    @classmethod
    def setup_class_custom(cls):
        cls.api = 'api.create_songs_rating'
        cls.song_id = cls.song_ids[0]['_id']
        cls.headers = {
            'Content-Type': JSON_MIME_TYPE,
            'Accept': JSON_MIME_TYPE
        }

    def test_post_rating(self, client):
        data = { 'songId': str(self.song_id), 'rating': 3 }
        res = client.post(url_for(self.api), data=dumps(data), headers=self.headers)

        assert res.status_code == 201
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'message': 'The item was created successfully' }
        assert res.headers.get('Location') is not None

        rating_id = res.headers.get('Location').split('/')[-1]
        db_res = self.db.ratings.find({ '_id': ObjectId(rating_id) }).limit(1)
        assert list(db_res) != []

    def test_post_rating_bad_rating(self, client):
        data = { 'songId': str(self.song_id), 'rating': 10 }
        res = client.post(url_for(self.api), data=dumps(data), headers=self.headers)

        assert res.status_code == 400
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Bad Request' }

    def test_post_rating_no_id(self, client):
        res = client.post(url_for(self.api), headers=self.headers)

        assert res.status_code == 400
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Bad Request' }

    def test_post_rating_bad_id(self, client):
        data = { 'songId': 'xyz', 'rating': 3 }
        res = client.post(url_for(self.api), data=dumps(data), headers=self.headers)

        assert res.status_code == 400
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Bad Request' }

    def test_post_rating_not_found(self, client):
        data = { 'songId': '5abd9fbcd48b40737d3c14db', 'rating': 3 }
        res = client.post(url_for(self.api), data=dumps(data), headers=self.headers)

        assert res.status_code == 404
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Not Found' }


class TestSongsRatingsAPI(MongoSystemTest):

    @classmethod
    def setup_class_custom(cls):
        cls.api = 'api.songs_rating'
        cls.seed_ratings()
        cls.rating_id = str(cls.rating_ids[0]['_id'])

        cls.schema = {
          'type': 'object',
          'properties': {
            'songId': { 'type': 'object' },
            'rating': { 'type': 'integer' },
          },
          'required': [ 'songId', 'rating' ]
        }

    def test_rating(self, client):
        res = client.get(url_for(self.api, rating_id=self.rating_id))

        assert res.status_code == 200
        assert res.mimetype == JSON_MIME_TYPE
        assert validate(res.json['data'], self.schema) is None
        assert res.json['data']['_id']['$oid'] == self.rating_id

    def test_rating_no_id(self, client):
        res = client.get(url_for(self.api, rating_id=''))

        assert res.status_code == 404
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Not Found' }

    def test_rating_bad_id(self, client):
        res = client.get(url_for(self.api, rating_id='123'))

        assert res.status_code == 400
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Bad Request' }

    def test_rating_not_found(self, client):
        res = client.get(url_for(self.api, rating_id='5abd9fbcd48b40737d3c14db'))

        assert res.status_code == 404
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Not Found' }


class TestSongsAvgRatingsAPI(MongoSystemTest):

    @classmethod
    def setup_class_custom(cls):
        cls.api = 'api.songs_avg_rating'
        cls.song_id = str(cls.song_ids[0]['_id'])
        cls.seed_ratings()

        cls.schema = {
          'type': 'array',
          'items': {
            'type': 'object',
            'properties': {
              'avgRating': { 'type': 'number' },
              'minRating': { 'type': 'integer' },
              'maxRating': { 'type': 'integer' }
            },
            'required': [ 'avgRating', 'minRating', 'maxRating' ]
          }
        }

    def test_avg_rating(self, client):
        res = client.get(url_for(self.api, song_id=self.song_id))

        assert res.status_code == 200
        assert res.mimetype == JSON_MIME_TYPE
        assert validate(res.json['data'], self.schema) is None
        assert res.json['data'][0]['_id']['$oid'] == self.song_id

    def test_avg_rating_no_id(self, client):
        res = client.get(url_for(self.api, song_id=''))

        assert res.status_code == 404
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Not Found' }

    def test_avg_rating_bad_id(self, client):
        res = client.get(url_for(self.api, song_id='123'))

        assert res.status_code == 400
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Bad Request' }

    def test_avg_rating_not_found(self, client):
        res = client.get(url_for(self.api, song_id='5abd9fbcd48b40737d3c14db'))

        assert res.status_code == 404
        assert res.mimetype == JSON_MIME_TYPE
        assert res.json == { 'error': 'Not Found' }

