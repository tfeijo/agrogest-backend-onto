import markdown, os
from flask import jsonify, request
from app import app
from src.controllers.CityController import *
from src.controllers.StateController import *
from src.controllers.BiomeController import *
from src.controllers.FarmController import *

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

@app.route('/states/<int:state_id>/cities', methods=['GET']) 
def city_index_by_state(state_id): return CityController.index(state_id, '*')

@app.route('/biomes/<int:biome_id>/cities', methods=['GET']) 
def city_index_by_biome(biome_id): return CityController.index('*', biome_id)

@app.route('/states', methods=['GET']) 
def state_index(): return StateController.index()

@app.route('/states/<int:id>', methods=['GET']) 
def state_show(id): return StateController.show(id)

@app.route('/biomes', methods=['GET']) 
def biome_index(): return BiomeController.index()

@app.route('/biomes/<int:id>', methods=['GET']) 
def biome_show(id): return BiomeController.show(id)

################# CORRIGIR

@app.route('/farms', methods=['GET']) 
def farm_index(): return FarmController.index()

@app.route('/farms', methods=['POST']) 
def farm_store():
  farm = request.json
  return FarmController.store(farm)

@app.route('/farms/<int:id>', methods=['GET']) 
def farm_show(id): return FarmController.show(id)


####################
# Methods POST (store) not essencial

@app.route('/biomes', methods=['POST']) 
def biome_store(): return BiomeController.store(request.json)

@app.route('/cities', methods=['POST']) 
def city_store():
  content = request.json
  return CityController.store(content)

@app.route('/states', methods=['POST']) 
def state_store(): 
  state = request.json
  return StateController.store(state)