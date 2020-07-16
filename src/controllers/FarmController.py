from flask import jsonify
from src.models.Classes import *
from src.ontology.config import onto, get_id, inferred
from src.utils.methods import *

class FarmController():
  def index():
    with onto: sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
    query_farm = onto.Farm.instances()
    farms = []
    for farm in query_farm:
      farms.append(farm.show_json())
    
    return jsonify(farms)

  def store(farm):
    query_city = onto.search_one(is_a=onto.City, id=farm['city_id'])
    farm_id = get_id('Farm')
    
    if farm['installation_id'] == None: 
      farm['installation_id'] = UUID()

    device = Device(farm['installation_id'])

    new = Farm(
      f'{get_name_to_onto(device)}_{farm_id}',
      id = [farm_id],
      city=[query_city],
      hectare=[float(farm['hectare'])],
      device=[device],
      licensing=[farm['licensing']],
    )
    onto.save()
    with onto: sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
    onto.save(file = "./src/ontology/inferred.owl")
    return jsonify(new.store_json())
    
  def show(id):
    with inferred: sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
    farm = inferred.search_one(is_a=Farm, id=id)
    if farm == None: return jsonify({ 'error': 'Not found'}), 404
    return jsonify(farm.show_json())
    