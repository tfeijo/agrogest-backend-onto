from owlready2 import *
import json

onto_path.append("src/ontology/")
onto = get_ontology("bd.owl").load()

infered = get_ontology("bd_infered.owl").load()

def save_onto(onto):
  onto.save(file = "./src/ontology/bd_infered.owl", format = "rdfxml")

def get_id(obj):
  
  data = {}
  
  r = open('./src/ontology/id.json', "r")
  data = json.load(r)

  if obj in data: data[obj] += 1
  else: data[obj] = 1

  w = open('./src/ontology/id.json', "w")
  json.dump(data, w)
    
  return data[obj]
