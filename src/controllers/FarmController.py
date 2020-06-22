from flask import jsonify
from src.models.Classes import *
from src.ontology.config import onto

class FarmController():
  def index():
    farm1 = Farm(123.23, 2343, True, 1, 'asdjkfasdkjhfius')
    farm2 = Farm(321.23, 123, False, 2, 'aljsdfdlf')
    farms = [farm1.toJSON(), farm2.toJSON()]
    return jsonify(farms)

  def store(content):
    farm1 = Farm(
      content['hectare'],
      content['city_id'],
      content['licensing'],
    )
    return jsonify(farm1.toJSON())
  
  def show(id):
    farm1 = Farm(123.23, 2343, True, id, 'asdjkfasdkjhfius')
    return jsonify(farm1.toJSON())