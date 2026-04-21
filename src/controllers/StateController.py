import json

from flask import jsonify
from owlready2 import OwlReadyError

from src.models.Classes import State, state_to_json
from src.ontology.config import increase_id, onto
from src.utils.methods import clear_string


with open('./src/ontology/static_states.json', 'r') as _r:
  _static_states = json.load(_r)


class StateController:

  @staticmethod
  def index():
    try:
      return jsonify(_static_states)
    except OwlReadyError as e:
      return jsonify({'error': str(e)}), 500

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
