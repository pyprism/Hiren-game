#Date : 25th June , 2014
__author__ = 'prism'

import pymongo
import datetime
from flask import Flask, request, jsonify
#change the URI and db name plz  :/
client = pymongo.MongoClient('mongodb://localhost:27017/') 
db = client['Hiren-Game']
collection = db['game']

app = Flask(__name__)

@app.route("/",  methods=['POST', 'GET'])
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


@app.route('/create_game', methods=['POST'])
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


@app.route("/update_score",  methods=['POST', 'GET'])
def update_score():
    if request.method == 'POST':
        id = request.form['id']
        game = request.form['game']
        score = request.form['score']
        x = collection.update({'id': id, 'game': game},
                              {"$set": {'score': score}}, safe=True)
        return jsonify({'status': 'voila babe , score updated !'}), 202


@app.route("/result", methods=['POST'])
def result():
    if request.method == 'POST':
        id = request.form['id']
        game = request.form['game']
        data = collection.find_one({'id': id, 'game': game}, {'_id': False})
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
