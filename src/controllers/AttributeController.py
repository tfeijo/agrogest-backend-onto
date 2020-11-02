from flask import jsonify
from owlready2 import *
from src.models.Classes import *
from src.models.Rules import *
from src.utils.methods import *
from src.ontology.config import onto, increase_id

class AttributeController:
  def store(attributes):
    # farm = onto.search_one(is_a=Farm, id=attributesc['farm_id'])
    print(f'ID: {attributes[farm_id]}')
    # for key in attributes:
    #   print(f'{key}: {attributes[key]}')
    
    return jsonify(attributes)
