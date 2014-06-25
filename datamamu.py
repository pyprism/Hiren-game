__author__ = 'prism'
from pymongo import MongoClient
from flask import Flask ,render_template , request , jsonify

client = MongoClient('mongodb://localhost:27017/')
collection = client['Hiren-Game']


def create():
    if request.method == 'POST':
        name = request.form['name']
        token = request.form['token']
        #duplicate = collection.find_one({'name': name, 'token': token})
        duplicate = collection.find_one({'name': name})
        if not duplicate:
            data = {'name': name,
                    'token': token}
            collection.insert(data, safe=True)
            return 'done', 200
        elif duplicate['name'] == name:
