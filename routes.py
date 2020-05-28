import markdown, os
from flask import jsonify, request
from app import app
from controllers.CityController import *
from controllers.StateController import *
from controllers.BiomeController import *
from controllers.FarmController import *


@app.route('/', methods=['GET']) 
def readme():
  with open(os.path.dirname(app.root_path) + '\
/backend-onto/README.md', 'r') as readme_file:
    content = readme_file.read()
    return markdown.markdown(content), 200

@app.route('/cities', methods=['GET']) 
def city_index(): return CityController.index()

@app.route('/cities/<int:id>', methods=['GET']) 
def city_show(id): return CityController.show(id)

@app.route('/cities/state/<int:id>', methods=['GET']) 
def city_index_by_state(id): return CityController.index_by_state(id)

@app.route('/cities/biome/<int:id>', methods=['GET']) 
def city_index_by_biome(id): return CityController.index_by_biome(id)

@app.route('/states', methods=['GET']) 
def state_index(): return StateController.index()

@app.route('/states/<int:id>', methods=['GET']) 
def state_show(id): return StateController.show(id)

@app.route('/biomes', methods=['GET']) 
def biome_index(): return BiomeController.index()

@app.route('/biomes/<int:id>', methods=['GET']) 
def biome_show(id): return BiomeController.show(id)

@app.route('/lands', methods=['GET']) 
def farm_index(): return FarmController.index()

@app.route('/lands', methods=['POST']) 
def farm_store(): 
  content = request.json
  return FarmController.store(content)

@app.route('/lands/<int:id>', methods=['GET']) 
def farm_show(id): return FarmController.show(id)
