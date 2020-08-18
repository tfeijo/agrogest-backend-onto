from flask import jsonify
from src.models.Classes import *
from src.ontology.config import onto, get_id
from src.utils.methods import *

class StateController():

  def index():
    states_query = onto.State.instances()
    
    states = []
    for query in states_query: states.append(query.to_json())
    return jsonify(sorted(states, key = lambda i: (i['name'])))
  
  def show(id):
    state = onto.search_one(is_a=onto.State, id=id)
    return jsonify(state.to_json())
  
  def store(state):
    name = clear_string(state['name'])
    id = get_id('State')
    new = State(
      name,
      # id = [id],
      id = [state['id']],
      uf = [state['uf']]
    )
    onto.save()
    return jsonify(new.to_json())
  
