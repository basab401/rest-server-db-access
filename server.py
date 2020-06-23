#!/usr/bin/env python3

# flake8: noqa E302,E501

import os
import argparse
from rest_app import create_app, s_logger


####################################################################
# Helper functions
####################################################################
def check_ssl(app):
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


###############################################################################
# Execution functions
###############################################################################
def get_context(args, app):
    ''' Load application configurations '''
    check_ssl(app)
    # TODO: enable ssl
    # check if running with https, using None disables the SSL usage
    context = None
    if app.config['use_ssl']:
        context = (app.config['ssl_cert'], app.config['ssl_key'])
    return context

def run_rest_server(app, context):
    ''' Run the REST Server '''
    s_logger.info('Starting server on {}:{}.'.format(
        app.config['IP'], app.config['PORT']))
    app.run(
        host=app.config['IP'],
        port=app.config['PORT'],
        ssl_context=context)


###############################################################################
# Application Main
###############################################################################
if __name__ == '__main__':
    # Parse cli args (if any) to override config defaults
    args = parse_arguments()
    try:
        # Create application instance
        app = create_app(userid=args.mongodb_user, password=args.mongodb_pw)
        context = get_context(app, args)
        # Run the server
        run_rest_server(app, context)
    except KeyboardInterrupt:
        s_logger.debug('Crtl+C Pressed. Shutting down..')
    except Exception as e:
        s_logger.error('Failed to start the REST API server: {}'.format(e))
