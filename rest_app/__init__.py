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
from flask import Flask, request, jsonify, redirect
from flask_httpauth import HTTPBasicAuth
from rest_app import mongodb, s3_access


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
        '/v1/mongodb/fetch',
        '/v1/mongodb/insert',
        '/v1/s3',
        '/v1/s3/upload',
        '/v1/s3/download/{file_name}'
    ]}

index_msg = 'Application to access Document based databases'

def return_response(resp):
    return ({'resp': resp})

@server_conf.auth.get_password
def get_pw(username):
    if username in server_conf.users:
        return server_conf.users.get(username)
    return None

def allowed_file(filename, allowed_ext=[]):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in allowed_ext

def ensure_dir_exists(dir_path):
    ''' Create a direcotry path if it does not yet exist '''
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

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


    # Mongodb routes
    @app.route('/v1/mongodb')
    @server_conf.auth.login_required
    def mongodb_find_all():
        rc = 200
        result = None
        if request.method == 'GET':
            try:
                result = server_conf.mongodb_connobj.fetch()
            except Exception as e:
                s_logger.error('Failed to fetch data: {}'.format(e))
                rc = 500
        return jsonify(result, rc)

    @app.route('/v1/mongodb/fetch')
    @server_conf.auth.login_required
    def mongodb_find_one_or_all():
        rc = 200
        result = None
        data = request.get_json() if request.get_json() else None
        if request.method == 'GET':
            try:
                result = server_conf.mongodb_connobj.fetch(data)
            except Exception as e:
                s_logger.error('Failed to fetch data: {}'.format(e))
                rc = 500
        return jsonify(result, rc)

    @app.route('/v1/mongodb/insert', methods=['POST'])
    @server_conf.auth.login_required
    def mongodb_insert_doc():
        rc = 200
        result = None
        data = request.get_json()
        if request.method == 'POST':
            try:
                result = server_conf.mongodb_connobj.insert(data)
            except Exception as e:
                s_logger.error('Failed to update data: {}'.format(e))
                rc = 500
        return jsonify(result, rc)


    # S3 routes
    @app.route('/v1/s3')
    def s3_list_items():
        try:
            contents = server_conf.s3_obj.list_files()
            rc = 200
        except Exception as e:
            s_logger.error('Failed to list bucket contents: {}'.format(e))
            rc = 500
        return jsonify(contents, rc)

    @app.route('/v1/s3/upload', methods=['POST'])
    def s3_upload():
        if request.method == 'POST':
            try:
                print(request.files)
                f = request.files['File']
                print(f.filename)
                if not allowed_file(f.filename, app.config['ALLOWED_EXTENSIONS']):
                    return jsonify('file type not supported', 400)
                #f.save(os.path.join(server_conf.s3_remote_upload_folder, f.filename))
                server_conf.s3_obj.upload_file(
                    f'{server_conf.s3_local_upload_folder}/{f.filename}')
            except Exception as e:
                s_logger.error('failed to upload file: {}'.format(e))
                return jsonify('failed to upload file', 500)
            return redirect("/v1/s3")

    @app.route("/v1/s3/download/<file_name>", methods=['GET'])
    def download(file_name):
        if request.method == 'GET':
            try:
                ensure_dir_exists(server_conf.s3_local_download_folder)
                output = server_conf.s3_obj.download_file(
                    file_name, server_conf.s3_local_download_folder)
                rc = 200
            except Exception as e:
                s_logger.error('Failed to list bucket contents: {}'.format(e))
                rc = 500
            return jsonify(output, rc)


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

    # Initialize s3 access object
    server_conf.s3_remote_upload_folder = app.config['S3_REMOTE_UPLOAD_FOLDER']
    server_conf.s3_local_download_folder = app.config['S3_LOCAL_DOWNLOAD_FOLDER']
    server_conf.s3_local_upload_folder = app.config['S3_LOCAL_UPLOAD_FOLDER']
    server_conf.s3_obj = s3_access.S3Access(app.config['S3_BUCKET'])

    return app
