from flask import jsonify
from src.models.Classes import *
from src.ontology.config import onto
from src.utils.methods import *

class StateController():

  def index():
    states_query = onto.State.instances()
    
    states = []

    for query in states_query:
      states.append(query.to_json())

    return jsonify(states)
  
  def show(id):
    state = onto.search_one(is_a=State, id=id)
    return jsonify(state.to_json())
  
  def store(state):
    
    name = clear_string(state['name'])
    new = State(
      name,
      id = [state['id']],
      uf = [state['uf']]
    )

    onto.save()
    
    return jsonify(new.to_json())
  
