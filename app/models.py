from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    super_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', backref='hero', lazy=True)

    def to_dict(self, include_powers=True):
        hero_dict = {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
        }

        if include_powers:
            hero_dict['powers'] = [hero_power.power.to_dict(include_heroes=False) for hero_power in self.hero_powers]

        return hero_dict
        

    def __repr__(self):
        return f'<Hero {self.name}, {self.super_name}>'
    
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', backref='power', lazy=True)

    @validates('name')
    def validate_name(self, key, name):
        if len(name) < 2:
            raise ValueError('Name must be at least 20 characters long')
        return name
    
    def to_dict(self, include_heroes=True):
        power_dict = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

        if include_heroes:
            power_dict['heroes'] = [hero_power.hero.to_dict(include_powers=False) for hero_power in self.hero_powers]

        return power_dict

    def __repr__(self):
        return f'<Power {self.name}, {self.description}>'
    

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError('Strength must be one of "Strong", "Weak", or "Average"')
        return strength

    def __repr__(self):
        return f'<HeroPower {self.hero_id}, {self.power_id}>'
 

