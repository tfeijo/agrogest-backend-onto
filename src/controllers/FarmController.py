from flask import jsonify
from src.models.Classes import *
from src.ontology.config import onto
from src.utils.methods import *

class FarmController():
  def index():
    farm1 = Farm(123.23, 2343, True, 1, 'asdjkfasdkjhfius')
    farm2 = Farm(321.23, 123, False, 2, 'aljsdfdlf')
    farms = [farm1.toJSON(), farm2.toJSON()]
    return jsonify(farms)

  def store(farm):
    query_city = onto.search_one(is_a=onto.City, id=farm['city_id'])
    
    farm_id = 4 #Get_id
    
    if farm['installation_id'] == None: 
      farm['installation_id'] = UUID()

    device = Device(farm['installation_id'])
    

    new = Farm(
      f'{get_name_to_onto(device)}_{farm_id}',
      id = [farm_id],
      city=[query_city],
      hectare=[farm['hectare']],
      device=[device],
      licensing=[farm['licensing']],
    )
    onto.save()
    
    return jsonify(new.store_json())
    
  def show(id):
    farm1 = Farm(123.23, 2343, True, id, 'asdjkfasdkjhfius')
    return jsonify(farm1.toJSON())