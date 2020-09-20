from owlready2 import *
import json

# reasoning.JAVA_MEMORY = 15000  

onto_path.append("src/ontology/")
onto = get_ontology("db.owl").load()

def increase_id(obj):
  
  data = {}
  
  r = open('./src/ontology/id.json', "r")
  data = json.load(r)

  if obj in data: data[obj] += 1
  else: data[obj] = 1

  w = open('./src/ontology/id.json', "w")
  json.dump(data, w)

  return data[obj]

def decrease_id(obj):
  data = {}
  
  r = open('./src/ontology/id.json', "r")
  data = json.load(r)

  if obj in data: data[obj] -= 1
  else: data[obj] = 0

  w = open('./src/ontology/id.json', "w")
  json.dump(data, w)

  return data[obj]
