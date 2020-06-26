from flask import jsonify
from owlready2 import *
from src.models.Classes import *
from src.models.Rules import *
from src.utils.methods import *
from src.ontology.config import onto, infered, save_onto, get_id

class CityController:
  def index(state_id = '*', biome_id='*'):
    print(state_id)
    print(biome_id)
    if state_id != '*': state_id = onto.search_one(is_a = onto.State, id=state_id)
    if biome_id != '*': biome_id = onto.search_one(is_a = onto.Biome, id= biome_id)

    cities_query = list(onto.search(is_a = onto.City, state=state_id, biome=biome_id))      
    cities = []
    
    for query in cities_query:
      cities.append(query.to_json())

    return jsonify(cities)

  def show(id):

    query = onto.search_one(is_a=onto.City, id=id)      

    return jsonify(query.to_json())

  def store(city):
    
    state = onto.search_one(
      is_a = onto.State,
      id=city["state"]["id"]
    )
    
    biomes = []
    for biome in city['biomes']:
      query_biome = onto.search_one(
        is_a = onto.Biome,
        id=biome['id']
      )
      biomes.append(query_biome)
    
    name = clear_string(city['name'])
    uf = state.uf[0]
    
    city = City(
        f'{name}_{uf}',
        id = [get_id('.City')],
        # id = [city['id']],
        biome = biomes,
        fiscal_module=[city['fiscal_module']],
        state=[state]
      )
      
    onto.save()
    
    return jsonify(city.to_json())
