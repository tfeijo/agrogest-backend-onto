from flask import jsonify
from owlready2 import *
import json
from src.utils.methods import *
from src.ontology.config import increase_id, onto

r = open('./src/ontology/static_cities.json', "r")
data = json.load(r)
class CityController:
  
  def index(state_id = '*', biome_id='*'):
    if state_id != '*':
      state_id = onto.search_one(is_a=onto.State, id=state_id)
    if biome_id != '*':
      biome_id = onto.search_one(is_a=onto.Biome, id=biome_id)

    # cities_query = list(onto.search(
    #   is_a=onto.City, has_state=state_id,
    #   has_biome=biome_id)
    # ) 
    
    # cities = []
    # for query in cities_query:
    #   cities.append(query.to_json())     
    # feedback = sorted(cities, key = lambda i: (i['name']))
    
    # data = {}
  
    # data[str(state_id)] = feedback 
    
    # w = open('./src/ontology/static_cities.json', "w")
    # json.dump(data, w)

    return jsonify(data[str(state_id)])

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
    id = increase_id('City')

    city = City(
        f'{name}_{uf}',
        # id = [id],
        id = [city['id']],
        has_biome = biomes,
        fiscal_module=[city['fiscal_module']],
        has_state=[state]
      )
      
    onto.save()
    
    return jsonify(city.to_json())
