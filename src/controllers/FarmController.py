from flask import jsonify
from src.models.Classes import *
from src.ontology.config import increase_id, decrease_id
from src.utils.methods import *


class FarmController():
  
  def index():
    query_farm = onto.Farm.instances()
    farms = []
    for farm in query_farm:
      farms.append(farm.to_json())
    
    return jsonify(farms)

  def store(farm):
    onto = get_ontology("./src/ontology/db.owl").load()
    query_city = onto.search_one(is_a=onto.City, id=farm['city_id'])

    if 'id' in farm:
      farm_id = farm['id']
    else:
      farm_id = increase_id('Farm')
    
    if farm['installation_id'] == None: 
      farm['installation_id'] = UUID()
    new = None
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
      onto.save(file=f'./src/ontology/temp/{farm_id}.owl')
      
    except:
      if not 'id' in farm: decrease_id('Farm')
      return jsonify({"Error": "Something went wrong in inserting"}), 400
    else:
      try:
        print(new.to_json())
        return jsonify(new.to_json()),200
      except:
        
        return jsonify({'Error':'Inserted but not queried'}),400

  def show(id):
    farm = onto.search_one(is_a=Farm, id=id)
    if farm == None: return jsonify({ 'error': 'Not found'}), 404
    return jsonify(farm.to_json())