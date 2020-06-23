# To be run like this:
#   python3 -m pytest -s tests -v

###############################################################################
# Disable linting warnings: 'line too long' and 'may be undefined'
# flake8: noqa E302, E305

import os
import sys
import json
from bson import json_util
from base64 import b64encode
import mongomock
import pytest
from pytest_mock import mocker


#module_path = os.path.dirname(os.path.abspath(__file__))
#sys.path.insert(0, module_path + '/../')

from rest_app import create_app, mongodb, endpoints, index_msg

dummy_get_objects = [{'dummy_mult_field0': 0, 'dummy_mult_field100': 100}]
dummy_get_object = {'dummy_field0': 0}
dummy_post_objects = {'dummy_post_mult_field0': 1000, 'dummy_post_mult_field100': 1000}
dummy_post_object = {'dummy_post_field0': 0}

credentials = b64encode(b"test:test").decode('utf-8')


###############################################################################
# Fixtures and monkeypatches
###############################################################################

@pytest.fixture(autouse=True)
def mock_mongodb(monkeypatch):
    ''' Monkeypatching mongodb connection '''
    class MockMongoDb(object):
        def __init__(self):
            self.client = mongomock.MongoClient()
            self.db = self.client.db
            self.collection = self.db.collection
            self.collection.insert(dummy_get_objects)
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def fetch(self, data=None):
            record = {}
            if not data:
                record = self.collection.find()
            else:
                record = self.collection.find_one(data)
            return json.loads(json_util.dumps(record))
        def insert(self, data):
            self.collection.insert_one(data)
            return json.loads(json_util.dumps('mock_insert'))

    def _mock_mongodb(*arg, **kwargs):
        return MockMongoDb()
    monkeypatch.setattr(mongodb, 'MongoDb', _mock_mongodb)


@pytest.fixture(scope='module')
def app():
    ''' Create and configure a new app instance for each of the tests '''
    # create the app with common test config
    app = create_app()
    yield app
    # close and remove the temporary database


@pytest.fixture(scope='module')
def client(app):
    ''' A test client for the app '''
    return app.test_client()


###############################################################################
# Test functions for rest application
###############################################################################

def test_client_get(client):
    ''' Test rest application get method '''
    response = client.get('/')
    assert json.loads(response.data)[0] == index_msg
    assert response.status_code == 200

    response = client.get('/v1')
    assert json.loads(response.data)[0] == endpoints
    assert response.status_code == 200

    response = client.get('/v1/mongodb',
            headers={'Authorization': f'Basic {credentials}'})
    print(json.loads(response.data)[0])
    assert json.loads(response.data)[0][0]['dummy_mult_field100'] == 100
    assert response.status_code == 200


def test_client_post(client):
    ''' Test rest application post method '''
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Basic {credentials}'
    }
    response = client.post('/v1/mongodb',
            data=json.dumps(dummy_post_objects),
            headers=headers)
    print(response)
    assert response.content_type == mimetype
    assert response.status_code == 200
    assert json.loads(response.data)[0] == 'mock_insert'


def test_client_unauthorized(client):
    # Test unathorized access
    response = client.post('/v1/mongodb',
        data=json.dumps(dummy_post_objects))
    assert response.status_code == 401
