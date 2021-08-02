from flask import jsonify
from owlready2 import World, OwlReadyError, sync_reasoner_pellet
from src.models.Classes import farm_to_json
from src.ontology.config import increase_id, decrease_id
from src.utils.methods import *
import glob, json


class SustainabilityController():

  def index():
    r = open('./src/ontology/last_id_fullontology.json', "r")
    data = json.load(r)
    farms = data["farms"]

    return jsonify(farms)