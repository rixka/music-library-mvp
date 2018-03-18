from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import make_response, abort

JSON_MIME_TYPE = 'application/json'


def json_response(data='', status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE

    return make_response(dumps(data), status, headers)

def validate_object_id(_id):
    if ObjectId.is_valid(_id):
        return ObjectId(_id)
    else:
        abort(400)

