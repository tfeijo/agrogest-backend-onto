from flask import jsonify
from owlready2 import World, OwlReadyError, sync_reasoner_pellet
from src.models.Classes import farm_to_json
from src.ontology.config import increase_id, decrease_id
from src.utils.methods import *
import glob, json

class FarmController():
  def index():
    r = open('./src/ontology/static_farms.json', "r")
    data = json.load(r)
    
    farms = data["farms"]
    last_id = data["last_id"]
    
    for file in glob.iglob('./src/ontology/temp/*.owl', recursive = True):
      file = file[:-4]
      id = int(file[20:])
      
      if (id > last_id ):
        last_id = id

        default_world = World(filename = f'{file}.sqlite3', exclusive=False)
        onto = default_world.get_ontology(f'{file}.owl').load()
        try:
          farms.append(farm_to_json(onto.search_one(is_a=onto.Farm, id=id)))
          
        except OwlReadyError as e:
          print(f'Something went wrong in query: {e}')
          return jsonify({"Error": "Something went wrong in query"}), 400
          
        finally:
          onto.destroy()
          default_world.close()
        
    w = open('./src/ontology/static_farms.json', "w")
    json.dump({
      "last_id": last_id,
      "farms": farms
    }, w)
    
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
    
    file = f'./src/ontology/temp/{id}'
    
    try:
      default_world = World(filename = f'{file}.sqlite3', exclusive=False)
      onto = default_world.get_ontology(f'{file}.owl').load()
      farm = farm_to_json(onto.search_one(is_a=onto.Farm, id=id))
      
    except OwlReadyError as e:
      print(f'Something went wrong in query: {e}')
      return jsonify({"Error": "Something went wrong in query"}), 400
      
    finally:
      onto.destroy()
      default_world.close()
    
    return jsonify(farm)