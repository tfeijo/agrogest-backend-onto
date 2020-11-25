from flask import jsonify
from owlready2 import World, OwlReadyError, sync_reasoner_pellet
from src.models.Classes import farm_to_json
from src.ontology.config import increase_id, decrease_id
from src.utils.methods import *


class FarmController():
  
  def index():
    default_world = World(filename = "./src/ontology/db.sqlite3", exclusive=False)
    onto = default_world.get_ontology("./src/ontology/db.owl").load()
    
    query_farm = onto.Farm.instances()
    farms = []
    for farm in query_farm:
      farms.append(farm_to_json(farm))
    
    return jsonify(farms)

  def store(farm):
    if 'id' in farm:
      farm_id = farm['id']
    else:
      farm_id = increase_id('Farm')
    
    default_world = World(filename = f'./src/ontology/temp/{farm_id}.sqlite3', exclusive=False)
    onto = default_world.get_ontology("./src/ontology/db.owl").load()
    
    query_city = onto.search_one(is_a=onto.City, id=farm['city_id'])

    if farm['installation_id'] == None: 
      farm['installation_id'] = UUID()
    
    new = None
    
    try:
      with onto:
        device = onto.Device(farm['installation_id'])
        new = onto.Farm(
          f'{get_name_to_onto(device)}_{farm_id}',
          id = [farm_id],
          has_city=[query_city],
          hectare=[float(farm['hectare'])],
          is_created_by=[device],
          licensing=[farm['licensing']],
        )
        sync_reasoner_pellet(default_world, infer_property_values = True, infer_data_property_values = True)
      default_world.save(file=f'./src/ontology/temp/{farm_id}.owl')
      
    except OwlReadyError as e:
      print(f'Something went wrong in inserting: {e}')
      if not 'id' in farm: decrease_id('Farm')
      return jsonify({"Error": "Something went wrong in inserting"}), 400
    else:
      try:
        json = farm_to_json(new)
        return jsonify(json),200
      except OwlReadyError as e:
        print(f'Inserted but not queried: {e}')
        return jsonify({'Error':'Inserted but not queried'}),400
    finally:
      onto.destroy()
      default_world.save()
      default_world.close()
      

  def show(id):
    farm = onto.search_one(is_a=Farm, id=id)
    if farm == None: return jsonify({ 'error': 'Not found'}), 404
    json = farm.to_json()
    return jsonify(json)