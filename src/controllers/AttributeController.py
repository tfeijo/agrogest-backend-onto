import threading

from flask import jsonify
from owlready2 import sync_reasoner_pellet

from src.controllers.FullontoController import FullontoController
from src.models.Classes import document_to_json, farm_to_json
from src.utils.methods import Ontology


class AttributeController:
  @staticmethod
  def store(attributes):
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

        for key, value in attributes.items():
          if key == 'farm_id':
            continue
          farm_json['attributes'][key] = value
          if value:
            farm.has_attribute.append(db.onto.Attribute(key))
          else:
            farm.has_missing_attribute.append(db.onto.Attribute(key))

        sync_reasoner_pellet(db.world, infer_property_values=True, infer_data_property_values=True)
      db.save()

      document_query = list(db.onto.search(
        is_a=db.onto.Document, is_document_recommended_of=farm
      ))

      list_documents = {}
      farm_json['documents'] = []

      for document in document_query:
        document_json = document_to_json(document)
        farm_json['documents'].append(document_json)
        url = str(document_json['url'])
        category = str(document_json['category'])
        question = str(document_json['question'])

        if url not in list_documents:
          list_documents[url] = {
            'questions': [question],
            'category': [category],
            'description': str(document_json['description']),
            'is_file': str(document_json['is_file']),
          }
        else:
          list_documents[url]['description'] = str(document_json['description'])
          list_documents[url]['is_file'] = str(document_json['is_file'])

          if question not in list_documents[url]['questions']:
            list_documents[url]['questions'].append(question)
          if category not in list_documents[url]['category']:
            list_documents[url]['category'].append(category)

      return jsonify(list_documents)

    finally:
      db.save()
      db.close()
      # Kick off fullontology update in background; must pass target+args,
      # not an already-invoked callable (previous code executed store() synchronously).
      t = threading.Thread(
        target=FullontoController.store,
        args=(farm_json,),
        daemon=True,
      )
      t.start()
