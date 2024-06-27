# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)


@app.route('/pets/<int:id>')
def get_pet(id):
    pet = Pet.query.get_or_404(id)
    return make_response(pet.to_dict(), 200)

@app.route('/species/<string:species>')
def get_pets_by_species(species):
    pets = Pet.query.filter_by(species=species).all()
    body = {
        'pets': [pet.to_dict() for pet in pets],
        'count': len(pets)
    }
    return make_response(body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
