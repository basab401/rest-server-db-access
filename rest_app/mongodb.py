#!/usr/bin/env python3

# flake8: noqa
# noqa: E302,E501

import json
from bson import json_util
from pymongo import MongoClient


class MongoDb(object):
    ''' Class to abstract away mongodb cluster operations '''
    def __init__(self, connection_url, db, collection):
        self.client = MongoClient(connection_url)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def fetch(self, data=None):
        ''' Fetch records (documents) based on data pattern '''
        if not data:
            record = self.collection.find()
        else:
            record = self.collection.find_one(data)
        # Requires extra encoding to work around Binary JSON (ObjectID)
        return json.loads(json_util.dumps(record))

    def insert(self, data):
        ''' Insert records (documents) into the collection '''
        result = None
        if data:
            result = self.collection.insert_one(data).inserted_id
        # Requires extra encoding to work around Binary JSON (ObjectID)
        return json.loads(json_util.dumps(result))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def __del__(self):
        self.client.close()
