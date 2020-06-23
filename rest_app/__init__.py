#!/usr/bin/env python3
'''
Flask-based REST API application which offers multiple interfaces for
document based DB clients to
   * store or post JSON data
   * fetch or query JSON data
'''

# flake8: noqa E302,E501

import os
import logging
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from rest_app import mongodb


##########################################################################
# Globals
##########################################################################
# Class to store runtime server configurations
class server_conf: pass

# Logging defaults
s_logger = logging.getLogger(__name__)

# Http Basic Authentication
server_conf.auth = HTTPBasicAuth()

endpoints = {'Endpoints': [
        '/v1',
        '/v1/mongodb',
        '/v1/s3'
    ]}

index_msg = 'Application to access Document based databases'

def return_response(resp):
    return ({'resp': resp})

@server_conf.auth.get_password
def get_pw(username):
    if username in server_conf.users:
        return server_conf.users.get(username)
    return None


##########################################################################
# Flask application
##########################################################################
def create_app(userid=None, password=None, test_config=None):
    # app has to be globally available
    app = Flask(__name__)

    if not test_config:
        app.config.from_object('rest_app.config.DefaultConfig')
    else:
        # load the test config if passed in
        app.config.update(test_config)

    ######################################################################
    # API endpoints
    ######################################################################
    @app.route('/')
    def index():
        ''' Main index page '''
        return jsonify(index_msg, 200)

    @app.route('/v1')
    def v1():
        ''' Endpoints '''
        return jsonify(endpoints, 200)

    @app.route('/login')
    @server_conf.auth.login_required
    def login():
        ''' login to further access other APIs '''
        return jsonify('Hello, %s!' % server_conf.auth.username(), 200)

    @app.route('/v1/mongodb', methods=['GET', 'POST'])
    @server_conf.auth.login_required
    def access_mongodb():
        rc = 200
        result = {}
        data = request.get_json()
        if request.method == 'GET':
            try:
                result = server_conf.mongodb_connobj.fetch(data)
            except Exception as e:
                s_logger.error('Failed to fetch data: {}'.format(e))
                rc = 500
        elif request.method == 'POST':
            try:
                result = server_conf.mongodb_connobj.insert(data)
            except Exception as e:
                s_logger.error('Failed to update data: {}'.format(e))
                rc = 500
        return jsonify(result, rc)

    # TODO: use ssl/certs
    server_conf.users = {
        app.config['DEFAULT_USERID']: app.config['DEFAULT_PW']
    }

    # Initialize a mongodb cluster object for accessibility
    mongodb_userid = userid if userid else app.config['MONGODB_USER']
    mongodb_pw = password if password else app.config['MONGODB_PW']
    mongodb_url = "mongodb+srv://{}:{}@cluster0-pv6rr.mongodb.net/{}?retryWrites=true&w=majority".format(
        mongodb_userid, mongodb_pw, app.config['MONGODB_DB'])
    # Create a local mongodb cluster object (www.mongodb.com)
    server_conf.mongodb_connobj = mongodb.MongoDb(
        mongodb_url, app.config['MONGODB_DB'], app.config['MONGODB_COLLECTION']
    )

    return app