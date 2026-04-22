import json

from flask import jsonify

from src.models.Classes import State
from src.ontology.config import onto
from src.utils.methods import clear_string


with open('./src/ontology/static_states.json', 'r') as _r:
  _static_states = json.load(_r)


class StateController:

  @staticmethod
  def index():
    return jsonify(_static_states)

  @staticmethod
  def show(id):
    state = onto.search_one(is_a=onto.State, id=id)
    if state is None:
      return jsonify({'error': 'State not found'}), 404
    return jsonify(state.to_json())

  @staticmethod
  def store(state):
    new = State(
      clear_string(state['name']),
      id=[state['id']],
      uf=[state['uf']],
      name=[str(state['name'])],
    )
    onto.save()
    return jsonify(new.to_json())
