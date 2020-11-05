from flask import jsonify
from owlready2 import *
import json
from src.models.Classes import *
from src.models.Rules import *
from src.utils.methods import *
from src.ontology.config import onto, increase_id

class AttributeController:
  def store(attributes):
    farm = onto.search_one(is_a=Farm, id=attributes['farm_id'])
    print(f'ID: {attributes["farm_id"]}')
    
    new_attributes = []
    new_missing_attributes = []

    for key in attributes:
      if (attributes[key]):
        new_attributes.append(Attribute(key))
      else:
        new_missing_attributes.append(Attribute(key))
    
    farm.has_attribute = new_attributes
    farm.has_missing_attribute = new_missing_attributes
    with onto: 
      sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
    onto.save()


    document_query = list(onto.search(
      is_a=onto.Document, is_document_recommended_of=farm
    )) 

    documents_JSON = []
    
    for document in document_query:
      documents_JSON.append(document.to_json())

    list_documents = {}
    
    for document in documents_JSON:
      url = str(document['url'])

      if not url in list_documents:
        list_documents[url] = {
          'questions': [
            str(document['question'])
          ],
          'category': [
            str(document['category'])
          ],
        }
      else:
        if not str(document['question']) in list_documents[url]['questions']:
          list_documents[url]['questions'].append(str(document['question']))
        
        if not str(document['category']) in list_documents[url]['category']:
          list_documents[url]['category'].append(str(document.category))
    print(list_documents)
    return jsonify(list_documents) 
