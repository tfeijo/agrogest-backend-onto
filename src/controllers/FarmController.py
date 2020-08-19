from flask import jsonify
from src.models.Classes import *
from src.ontology.config import onto, get_id
from src.utils.methods import *


class FarmController():
  
  def index():
    query_farm = onto.Farm.instances()
    farms = []
    for farm in query_farm:
      farms.append(farm.to_json())
    
    return jsonify(farms)

  def store(farm):
    query_city = onto.search_one(is_a=onto.City, id=farm['city_id'])
    farm_id = get_id('Farm')
    
    if farm['installation_id'] == None: 
      farm['installation_id'] = UUID()
    try:
      with onto:
        device = Device(farm['installation_id'])
        new = Farm(
          f'{get_name_to_onto(device)}_{farm_id}',
          id = [farm_id],
          has_city=[query_city],
          hectare=[float(farm['hectare'])],
          is_created_by=[device],
          licensing=[farm['licensing']],
        )
        sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
      onto.save()
      
    except:
      return jsonify({"Error": "Something went wrong"}), 400
    else:
      try:
        return jsonify(new.to_json()),200
      except:
        return jsonify({'Error':'Inserted but not queried'}),400
    finally:
      print(new)

       
    
    
  def show(id):
    farm = onto.search_one(is_a=Farm, id=id)
    if farm == None: return jsonify({ 'error': 'Not found'}), 404
    return jsonify(farm.to_json())