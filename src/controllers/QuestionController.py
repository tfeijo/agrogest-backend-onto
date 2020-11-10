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
    description_name = str(question['name'])
    question_title = str(question['question_title'])
    question_activity= question['activity']
    is_file = question['is_file']
    new_question = Question(
        name_question,
        id = [id_question],
        question_title = [question_title],
    )

    activities = []
    
    if question_activity == 'pecuaria':
      activities.append(ProductionActivity('bovinocultura_de_corte'))
      activities.append(ProductionActivity('bovinocultura_de_leite'))
      activities.append(ProductionActivity('suinocultura'))
      activities.append(ProductionActivity('avicultura'))
    
    if question_activity == 'bovino':
      activities.append(ProductionActivity('bovinocultura_de_corte'))
      activities.append(ProductionActivity('bovinocultura_de_leite'))
    
    if question_activity == 'suino':
      activities.append(ProductionActivity('suinocultura'))
        
    if question_activity == 'avicultura':
      activities.append(ProductionActivity('avicultura'))
    
    if question_activity == 'agricultura':
      activities.append(ProductionActivity('agricultura'))
        
    if question_activity == 'any':
      activities.append(ProductionActivity('any'))
    
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
        has_state_associated = [state],
        has_activity = activities,
        description = [description_name],
        is_file = [is_file]
      )
    else:
      new_document = Document(
        name_document,
        id = [id_document],
        url = [url],
        answer = [answer],
        has_category = [category],
        has_attribute = [attribute],
        has_question = [new_question],
        has_activity = activities,
        has_state_associated = [State('any')],
        description = [description_name],
        is_file = [is_file]
      )
      
    onto.save()

    return jsonify(question)
