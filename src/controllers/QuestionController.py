from flask import jsonify
from owlready2 import *
from src.models.Classes import *
from src.models.Rules import *
from src.utils.methods import *
from src.ontology.config import onto, increase_id

class QuestionController:
  def store(question):
    id_question = increase_id('Question')
    id_document = increase_id('Document')
    name_question = f'Question_{id_question}'
    name_document = f'Document_{id_document}'

    uf = str(question['uf']).upper()
    attribute = Attribute(question['attribute'])
    category = Category(question['category'])
    url = str(question['url'])
    answer = question['answer']
    question['question_title'] = clear_string(question['question_title'])
    question_title = question['question_title']
    
    new_question = Question(
        name_question,
        id = [id_question],
        question_title = [question_title],
    )

    if uf != '':  
      state = onto.search_one(
        is_a = onto.State,
        uf=[uf],
      )
      new_document = Document(
        name_document,
        id = [id_document],
        url = [url],
        answer = [answer],
        has_category = [category],
        has_attribute = [attribute],
        has_question = [new_question],
        has_state_associated = [state]
      )
    else:
      new_document = Document(
        name_document,
        id = [id_document],
        url = [url],
        answer = [answer],
        has_category = [category],
        has_attribute = [attribute],
        has_question = [new_question]
      )
      
    question['question_title'] = normal_string(question['question_title'])

    onto.save()

    return jsonify(question)
