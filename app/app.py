#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
import os
from flask_restful import Api, Resource
from sqlalchemy.orm import joinedload

from models import db, Hero, Power, HeroPower

file_path = os.path.abspath(os.getcwd()) + '/db/app.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        heroes_dict = [
            {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            } for hero in heroes
        ]
        
        return make_response(jsonify(heroes_dict), 200)
        

api.add_resource(Heroes, '/heroes')

if __name__ == '__main__':
    app.run(port=5556)
