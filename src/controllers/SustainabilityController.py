from flask import jsonify
from owlready2 import World, OwlReadyError, sync_reasoner_pellet
from src.models.Classes import farm_to_json
from src.ontology.config import increase_id, decrease_id
from src.utils.methods import *
import glob, json


class SustainabilityController():
  
  def index():
    
    try:
      default_world = World(filename = f'src/ontology/sustainability.sqlite3', exclusive=False)
      sustainability = default_world.get_ontology(f'src/ontology/sustainability.owl').load()
    except:
      return jsonify({ "Error" : "loading ontology"}),500

    classes = list(sustainability.classes())    

    sustainability.destroy()
    default_world.close()
    return { "HELLO" : str(classes) }
      
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