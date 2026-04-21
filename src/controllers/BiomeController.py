from flask import jsonify
from src.models.Classes import Biome
from src.ontology.config import onto, increase_id
from src.utils.methods import clear_string


class BiomeController:
  @staticmethod
  def index():
    biomes = [query.to_json() for query in onto.Biome.instances()]
    return jsonify(biomes)

  @staticmethod
  def show(id):
    biome = onto.search_one(is_a=onto.Biome, id=id)
    if biome is None:
      return jsonify({'error': 'Biome not found'}), 404
    return jsonify(biome.to_json())

  @staticmethod
  def store(biome):
    new = Biome(
      clear_string(biome['name']),
      id=[biome['id']],
    )
    onto.save()
    return jsonify(new.to_json())
