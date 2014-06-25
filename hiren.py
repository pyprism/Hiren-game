__author__ = 'prism'
#import datamamu
import pymongo , datetime
from flask import Flask, render_template, request, jsonify

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['Hiren-Game']
collection = db['uhlala']

app = Flask(__name__)

@app.route("/",  methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        #duplicate = collection.find_one({'name': name, 'token': token})
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


@app.route("/game",  methods=['POST', 'GET'])
def game():
    if request.method == 'POST':
        id = request.form['id']
        game = request.form['game']
        score = request.form['score']
        collection.update({'id': id, 'game': game},
                          {"$set": {'score': score}}, safe=True)
        return jsonify({'status': 'voila babe , score updated !'}), 202


@app.route("/result", methods=['POST'])
def result():
    if request.method == 'POST':
        id = request.form['id']
        game = request.form['game']
        data = collection.find({'id': id, 'game': game})
        if data:
            return jsonify(data), 200
        elif not data:
            return jsonify({'status': 'not found, so get lost'}), 404



@app.errorhandler(404)
def page_not_found(error):
    return "Are You Mad? ", 404


if __name__ == "__main__":
    app.run(debug=True)