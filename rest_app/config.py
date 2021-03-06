#!/usr/bin/env python3

class DefaultConfig:
    ALLOWED_EXTENSIONS = ['json', 'txt']

    # Default Userid and Password
    DEFAULT_USERID = 'test'
    DEFAULT_PW = 'test'

    # TODO: SSL certificate and key to allow https connections:
    #  must be provided when deployed
    #SSL_CERT =
    #SSL_KEY =

    # default IP to listen at.
    # settings this to 0.0.0.0 will be globally accessible, this is
    #  the most likely the case for deployment
    IP = '127.0.0.1'

    # default port to run
    # for deployment this should be most likely set to 443
    PORT = 10443

    # MONGODB Cluster access details
    MONGODB_USER = 'basab'
    MONGODB_PW = 'xxxxxxxx'
    MONGODB_DB = 'test_db'
    MONGODB_COLLECTION = 'test_collection'
    MONGODB_URL = 'mongodb+srv://%(MONGODB_USER)s:%(MONGODB_PW)s@cluster0-pv6rr.mongodb.net/%(MONGODB_DB)s?retryWrites=true&w=majority'

    # S3 Object store access details
    S3_BUCKET = 'basab-test-bucket-1'
    S3_REMOTE_UPLOAD_FOLDER = 'test-uploads-folder'
    S3_LOCAL_UPLOAD_FOLDER = '/tmp/uploads'
    S3_LOCAL_DOWNLOAD_FOLDER = '/tmp/downloads'
