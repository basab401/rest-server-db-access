#!/usr/bin/env python3
'''
Flask-based REST API server which offers multiple interfaces for
Document based DB clients to
    * store or post JSON data
    * fetch or query JSON data
'''

# flake8: noqa
# noqa: E302,E501

import os
import argparse
import logging
import json
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth

from mongodb import MongoDb

####################################################################
# Globals
####################################################################

# Using an placeholder class to store module level globals
class server_conf: pass

# Logging defaults
s_logger = logging.getLogger(__name__)

# app has to be globally available
app = Flask(__name__)

# Http Basic Authentication
server_conf.auth = HTTPBasicAuth()

endpoints = {'Endpoints': [
        '/v1',
        '/v1/mongodb',
        '/v1/s3'
    ]}

def ensure_prerequisites():
    app.config['use_ssl'] = False
    if 'ssl_cert' in app.config.keys() and 'ssl_key' in app.config.keys():
        if os.path.isfile(app.config['ssl_cert']) and os.path.isfile(
                app.config['ssl_key']):
            s_logger.info('SSL certificate found')
            app.config['use_ssl'] = True
        else:
            s_logger.info('SSL certificate or key is missing, check configuration')
            os.sys.exit(1)
    else:
        s_logger.info('No SSL certificates configured, using unencrypted connection!')

def return_response(resp):
    return ({'resp': resp})

@server_conf.auth.get_password
def get_pw(username):
    if username in server_conf.users:
        return server_conf.users.get(username)
    return None

@app.route('/')
def index():
    ''' Main index page '''
    return jsonify('API to store or fetch JSON data onto/from Document based databases', 200)

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


#####################################################################
# Argument Parser
#####################################################################
def parse_arguments():
    parser = argparse.ArgumentParser(
         usage='%(prog)s [OPTIONS]',
         description='%(prog)s starts a REST API server to access DB',
         formatter_class=argparse.ArgumentDefaultsHelpFormatter,
         prefix_chars='-+')

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument(
         '--config_file',
         '-c',
         help='Path and Name for the server configuration file')
    optional.add_argument(
         '--verbose',
         '-v',
         action='store_true',
         help='Level of debug prints')
    optional.add_argument(
         '--mongodb_user',
         '-u',
         help='Mongodb cluster access userid')
    optional.add_argument(
         '--mongodb_pw',
         '-p',
         help='Mongodb cluster access password')
    return parser.parse_args()


#####################################################################
# Application Main
#####################################################################
if __name__ == '__main__':
    # Parse cli args (if any) to override config defaults
    args = parse_arguments()
    # load configuration
    app.config.from_object('config.DefaultConfig')
    ensure_prerequisites()
    # TODO: enable ssl
    # check if running with https, using None disables the SSL usage
    context = None
    if app.config['use_ssl']:
        context = (app.config['ssl_cert'], app.config['ssl_key'])
    else:
        server_conf.users = {
            app.config['DEFAULT_USERID']: app.config['DEFAULT_PW']
        }
    try:
        mongodb_userid = args.mongodb_user if args.mongodb_user else app.config['MONGODB_USER']
        mongodb_pw = args.mongodb_pw if args.mongodb_pw else app.config['MONGODB_PW']
        mongodb_url = "mongodb+srv://{}:{}@cluster0-pv6rr.mongodb.net/{}?retryWrites=true&w=majority".format(
            mongodb_userid, mongodb_pw, app.config['MONGODB_DB'])
        # Create a local mongodb cluster object (www.mongodb.com)
        server_conf.mongodb_connobj = MongoDb(
            mongodb_url, app.config['MONGODB_DB'], app.config['MONGODB_COLLECTION']
        )
        # Run the REST Server
        s_logger.info('Starting server on {}:{}.'.format(
            app.config['IP'], app.config['PORT']))
        app.run(
            host=app.config['IP'],
            port=app.config['PORT'],
            ssl_context=context)
    except KeyboardInterrupt:
        s_logger.debug('Crtl+C Pressed. Shutting down..')
    except Exception as e:
        s_logger.error('Failed to start the REST API server: {}'.format(e))
