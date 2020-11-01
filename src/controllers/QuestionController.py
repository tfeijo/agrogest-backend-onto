from flask import jsonify
from owlready2 import *
from src.models.Classes import *
from src.models.Rules import *
from src.utils.methods import *
from src.ontology.config import onto, increase_id

class QuestionController:
  def store(question):
    return jsonify(question)
