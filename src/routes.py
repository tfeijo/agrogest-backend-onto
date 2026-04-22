import os

import markdown
from flask import request

from app import app
from src.controllers.AttributeController import AttributeController
from src.controllers.BiomeController import BiomeController
from src.controllers.CityController import CityController
from src.controllers.FarmController import FarmController
from src.controllers.FullontoController import FullontoController
from src.controllers.ParameterController import ParameterController
from src.controllers.ProductionController import ProductionController
from src.controllers.QuestionController import QuestionController
from src.controllers.StateController import StateController
from src.controllers.SustainabilityController import SustainabilityController


@app.route('/', methods=['GET'])
def readme():
  # README.md lives alongside app.py, so app.root_path is the correct base.
  readme_path = os.path.join(app.root_path, 'README.md')
  with open(readme_path, 'r') as readme_file:
    content = readme_file.read()
  return markdown.markdown(content), 200


# --- Cities ---
@app.route('/cities', methods=['GET'])
def city_index():
  return CityController.index()


@app.route('/cities/<int:id>', methods=['GET'])
def city_show(id):
  return CityController.show(id)


@app.route('/states/<int:state_id>/cities', methods=['GET'])
def city_index_by_state(state_id):
  return CityController.index(state_id, '*')


@app.route('/biomes/<int:biome_id>/cities', methods=['GET'])
def city_index_by_biome(biome_id):
  return CityController.index('*', biome_id)


# --- States ---
@app.route('/states', methods=['GET'])
def state_index():
  return StateController.index()


@app.route('/states/<int:id>', methods=['GET'])
def state_show(id):
  return StateController.show(id)


# --- Biomes ---
@app.route('/biomes', methods=['GET'])
def biome_index():
  return BiomeController.index()


@app.route('/biomes/<int:id>', methods=['GET'])
def biome_show(id):
  return BiomeController.show(id)


# --- Farms ---
@app.route('/farms', methods=['GET'])
def farm_index():
  return FarmController.index()


@app.route('/farms', methods=['POST'])
def farm_store():
  return FarmController.store(request.json)


@app.route('/farms/<int:id>', methods=['GET'])
def farm_show(id):
  return FarmController.show(id)


# --- Parameters ---
@app.route('/parameters', methods=['POST'])
def parameter_store():
  return ParameterController.store(request.json)


@app.route('/parameters', methods=['GET'])
def parameters_index():
  return ParameterController.index()


# --- Productions ---
@app.route('/productions', methods=['POST'])
def production_store():
  return ProductionController.store(request.json)


@app.route('/productions', methods=['GET'])
def productions_index():
  return ProductionController.index()


@app.route('/farms/<int:farm_id>/productions/<int:id>', methods=['DELETE'])
def productions_delete(farm_id, id):
  return ProductionController.delete(farm_id, id)


# --- Questions ---
@app.route('/questions', methods=['POST'])
def question_store():
  return QuestionController.store(request.json)


# --- Attributes ---
@app.route('/attributes', methods=['POST'])
def attribute_store():
  return AttributeController.store(request.json)


# --- Fullontology ---
@app.route('/fullontology', methods=['GET'])
def fullontology_index():
  production_type = request.args.get('production_type')
  return FullontoController.index(production_type)


@app.route('/fullontology/<int:id>', methods=['GET'])
def fullontology_index_id(id):
  return FullontoController.index_id(id)


# --- Sustainability / Graphics ---
@app.route('/graphics', methods=['GET'])
def sustainability_index():
  production_type = request.args.get('production_type')
  return SustainabilityController.index(production_type)
