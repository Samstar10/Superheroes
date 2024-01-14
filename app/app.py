#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
import os
from flask_restful import Api, Resource

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
    

class HeroesById(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()

        if hero:
            hero_dict = hero.to_dict()

            return make_response(jsonify(hero_dict), 200)
        
        else:
            return make_response(jsonify({"error": "Hero not found"}), 404)

class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        powers_dict = [
            {
                "id": power.id,
                "name": power.name,
                "description": power.description
            } for power in powers
        ]
        
        return make_response(jsonify(powers_dict), 200)
    
class PowersById(Resource):
    def get(self, id):
        power = Power.query.filter_by(id=id).first()

        if power:
            power_dict = power.to_dict()

            return make_response(jsonify(power_dict), 200)
        
        else:
            return make_response(jsonify({"error": "Power not found"}), 404)
        
    def patch(self, id):
        power = Power.query.filter_by(id=id).first()

        if power:
            for attr in request.form:
                setattr(power, attr, request.form[attr])

            db.session.commit(power)

            response_dict = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }

            return make_response(jsonify(response_dict), 200)
        
        else:
            return make_response(jsonify({"error": "Power not found"}), 404)
        

class HeroPowers(Resource):
    def post(self):
        data = request.get_json()

        new_hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )

        try:
            db.session.add(new_hero_power)
            db.session.commit()
            new_hero_power_dict = new_hero_power.hero.to_dict()
            return make_response(jsonify(new_hero_power_dict.to_dict()), 201)
        except:
            return make_response(jsonify({"error": ["validation errors"]}), 500)

api.add_resource(Heroes, '/heroes')
api.add_resource(HeroesById, '/heroes/<int:id>')
api.add_resource(Powers, '/powers')
api.add_resource(PowersById, '/powers/<int:id>')
api.add_resource(HeroPowers, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5556)
