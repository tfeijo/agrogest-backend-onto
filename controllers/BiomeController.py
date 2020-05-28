from flask import jsonify
from models.Biome import Biome

class BiomeController:


  def index():
    biome1 = Biome('Bioma1')
    biome2 = Biome('Bioma2')
    biomes = [biome1.toJSON(),biome2.toJSON()]

    return jsonify(biomes)
  
  def show(id):
    biome1 = Biome('Bioma1', id)
    
    return jsonify(biome1.toJSON())
