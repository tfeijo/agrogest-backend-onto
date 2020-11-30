from flask import jsonify
import json
from owlready2 import OwlReadyError
from src.ontology.config import increase_id, onto
from src.models.Classes import state_to_json


r = open('./src/ontology/static_states.json', "r")
data = json.load(r)
class StateController():
  
  def index():

    try:
      # states_query = onto.State.instances()
      # states = []
      # for query in states_query: 
      #   if (query!=onto.State("any")): 
      #     states.append(state_to_json(query))
      # feedback = sorted(states, key = lambda i: (i['name']))
      # w = open('./src/ontology/static_states.json', "w")
      # json.dump(feedback, w)

      return jsonify(data)
    except OwlReadyError as e:
      print(e)
      return jsonify({"Error": str(e)}), 500
    

  
  def show(id):
    state = onto.search_one(is_a=State, id=id)
    return jsonify(state.to_json())
  
  def store(state):
    name = clear_string(state['name'])
    id = increase_id('State')
    new = State(
      name,
      id = [state['id']],
      uf = [state['uf']],
      name = [str(state['name'])]
    )
    onto.save()
    return jsonify(new.to_json())
  
