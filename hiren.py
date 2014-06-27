#Date : 25th June , 2014
__author__ = 'prism'

import pymongo
import datetime
from datetime import timedelta 
from functools import update_wrapper
from flask import Flask, request, jsonify, current_app, make_response

client = pymongo.MongoClient('mongodb://localhost:27017/') 
db = client['Hiren-Game']
collection = db['game']

app = Flask(__name__)

#Fix for 'Access-Control-Allow-Origin'
def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):  
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route("/",  methods=['POST', 'GET', 'OPTIONS'])
@crossdomain(origin='*')
def create():
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        duplicate = collection.find_one({'id': id})
        if not duplicate:
            data = {'name': name,
                    'id': id}
            collection.insert(data, safe=True)
            return jsonify({'status': 'created'}), 201
        else:
            return jsonify({'status': 'already exits'}), 302
    elif request.method == "GET":
        return 'Fuck off!' + " " + str(datetime.datetime.utcnow())


@app.route('/create_game', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def create_game():
    if request.method == 'POST':
        id = request.form['id']
        game = request.form['game']
        duplicate = collection.find_one({'id': id, 'game': game})
        if not duplicate:
            collection.update({'id': id},
                              {'$set': {'game': game}})
            return jsonify({'status': "created"}), 201
        elif duplicate:
            return jsonify({'status': 'already exits '}), 302


@app.route("/update_score",  methods=['POST', 'GET', 'OPTIONS'])
@crossdomain(origin='*')
def update_score():
    if request.method == 'POST':
        id = request.form['id']
        game = request.form['game']
        score = request.form['score']
        x = collection.update({'id': id, 'game': game},
                              {"$set": {'score': score}}, safe=True)
        return jsonify({'status': 'voila babe , score updated !'}), 202


@app.route("/result", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def result():
    if request.method == 'POST':
        id = request.form['id']
        game = request.form['game']
        data = collection.find_one({'id': id, 'game': game}, {'_id': False})
        if data:
            return jsonify(data), 200
        elif not data:
            return jsonify({'status': 'not found, so get lost'}), 404

#scoreboard 
@app.route("/all_result", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def result():
    if request.method == 'POST':
        game = request.form['game']
        data = collection.find({'game': game}, {'_id': False})
        if data:
            return jsonify(data), 200
        elif not data:
            return jsonify({'status': 'not found, so get lost'}), 404

#useless route ! just for dumbass heroku engine
@app.route('/favicon.ico')
def favicon():
    return "."

@app.errorhandler(404)
def page_not_found(error):
    return ":P ", 404


if __name__ == "__main__":
    app.run(debug=True)
