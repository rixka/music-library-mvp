import pytest

from flask import url_for
from app import utils


def test_health(accept_json, client):
    res = client.get(url_for('api.health'), headers=accept_json)

    assert res.status_code == 200
    assert res.mimetype == utils.JSON_MIME_TYPE
    assert res.json == {'status': 'ok'}

