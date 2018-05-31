from gevent import monkey
monkey.patch_all()

import os
import sys
from bottle import run, get, template, abort, static_file, debug, redirect
from db import init_db
from appconfig import config


# Name of config File

"""
Configured Sites

Routes for the html Pages are set up automatically.

SITE'S keys represent an url path as well as the name of 
the used template for rendering the page.

E.g. 'print' corresponds to server_url/path and uses the template
'views/print.tpl'.

The static pages try to get the data, passed to the processData function via the
api url: '/api' + key (E.g. '/api/print'). These routes need to be filled with life!

"""

SITES = {
    'print': 'Print Data'
}


def mount_routes(db):
    @get('/')
    def index():
        # Redirect to first elements of SITES
        redirect('/' + list(SITES.keys())[0])

    @get('/static/<filename>')
    def server_static(filename):
        return static_file(filename, root='./static')

    @get('/api/print')
    def just_print():
        return {
            'testkey': 'testvalue'
        }

    @get('/<path:path>')
    def main_route(path):
        try:
            config = {
                'api_url': os.path.join('/api/', path),
                'cur_url': path,
                'title': SITES[path],
                'menu': SITES
            }
            return template(path, config=config)
        except (OSError, KeyError):
            abort(404)


if __name__ == '__main__':
    try:
        # Set up database connection
        db = init_db(config['database'])
    except KeyError:
        sys.exit("No database section in config file")

    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    else:
        port = config['main']['port']

    # Create routes
    mount_routes(db)

    # Do not cache css/js/html files
    debug(True)

    # Run server at given ports
    try:
        run(host=config['main']['host'], port=port, server='gevent')
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down server.")
        db.close()
