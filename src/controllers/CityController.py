from flask import jsonify
from src.models.Classes import *
from src.ontology.config import onto

class CityController:
  def index():
    city1 = City('Cidade1')
    city2 = City('Cidade2')
    cities= [city1.toJSON(),city2.toJSON()]
    return jsonify(cities)

  def show(id):
    city1 = City('Cidade1', id)
    return jsonify(city1.toJSON())
  
  def index_by_state(state_id):
    city1 = City('Cidade1')
    city2 = City('Cidade2')
    cities= [city1.toJSON(),city2.toJSON()]
    return jsonify(cities)

  def index_by_biome(biome_id):
    city1 = City('Cidade1')
    city2 = City('Cidade2')
    cities= [city1.toJSON(),city2.toJSON()]
    return jsonify(cities)
