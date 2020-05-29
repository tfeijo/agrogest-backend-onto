from flask import jsonify
from models.State import State

class StateController():
  def index():
    state1 = State('Rio de Janeiro')
    state2 = State('São Paulo')
    states = [state1.toJSON(), state2.toJSON()]
    return jsonify(states)
  
  def show(id):
    state1 = State('Rio de Janeiro', id)
    return jsonify(state1.toJSON())