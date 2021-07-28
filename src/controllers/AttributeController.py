from flask import jsonify
from owlready2 import *
import json
from src.models.Classes import *
from src.models.Rules import *
from src.utils.methods import Ontology
from src.ontology.config import increase_id

class AttributeController:
  def store(attributes):
    farm_json = None
    db = Ontology(f'./src/ontology/temp/{attributes["farm_id"]}')
    db.load()
    
    try:
      with db.onto:
        farm = db.onto.search_one(is_a=db.onto.Farm, id=attributes['farm_id'])
        farm.has_attribute = []
        farm.has_missing_attribute = []
        farm.has_recommended_document = []
        farm_json = farm_to_json(farm)
        farm_json['attributes'] = {}

        for key in attributes:
          if key!="farm_id":
            farm_json['attributes'][key] = attributes[key]
            print(f'{key}={attributes[key]}')
            if (attributes[key]):
              farm.has_attribute.append(db.onto.Attribute(key))
            else:
              farm.has_missing_attribute.append(db.onto.Attribute(key))
        
        sync_reasoner_pellet(db.world, infer_property_values = True, infer_data_property_values = True)
      db.save()

      document_query = list(db.onto.search(
        is_a=db.onto.Document, is_document_recommended_of=farm
      ))
      
      list_documents = {}
      farm_json['documents'] = []
      

      for document in document_query:
        document = document_to_json(document)
        farm_json['documents'].append(document)
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
      
    finally:
      db.save()
      db.close()