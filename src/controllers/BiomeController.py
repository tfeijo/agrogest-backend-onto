from flask import jsonify
from src.models.Classes import *
from src.ontology.config import onto, increase_id

class BiomeController:
  def index():
    biomes_query = onto.Biome.instances()
    biomes = []
    for query in biomes_query: biomes.append(query.to_json())
    return jsonify(biomes)
  
  def show(id):
    biome = onto.search_one(is_a=Biome, id=id) 
    return jsonify(biome.to_json())
  
  def store(biome):
    id = increase_id('Biome')
    new = Biome(
      clear_string(biome['name']),
      id = [biome['id']],
      # id = [id]
    )
    onto.save()
    
    return jsonify(new.to_json())
