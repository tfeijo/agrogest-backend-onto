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
    
    
    farm.has_attribute = []
    farm.has_missing_attribute = []

    for key in attributes:
      if key!="farm_id":

        if (attributes[key]):
          farm.has_attribute.append(Attribute(key))
        else:
          farm.has_missing_attribute.append(Attribute(key))
    
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
          'description': str(document['description']),
          'is_file': str(document['is_file']),
        }
      else:
        
        list_documents[url]['description'] = str(document['description'])
        list_documents[url]['is_file'] = str(document['is_file'])
        
        if not str(document['question']) in list_documents[url]['questions']:
          list_documents[url]['questions'].append(str(document['question']))
        
        if not str(document['category']) in list_documents[url]['category']:
          list_documents[url]['category'].append(str(document.category))

    
    return jsonify(list_documents) 
