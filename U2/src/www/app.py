from bottle import get, debug, run, template

debug(True)

@get('/')
def index():
    return template('index')

run(host='localhost', port=8080)