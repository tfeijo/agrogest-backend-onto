import unicodedata
import uuid
import string as st
import re
from threading import Thread
from owlready2 import World

class Ontology():
  def __init__(self, path):
    self.path = path
  
  def load(self):
      self.world = World(filename=f'{self.path}.sqlite3', exclusive=False)
      self.onto = self.world.get_ontology(f'{self.path}.owl').load()

  def save(self):
      self.onto.save(file = f'{self.path}.owl')
      self.world.save(file = f'{self.path}.owl')

  def close(self):
      self.onto.destroy()
      self.world.close()

class Reasoner(Thread):
    def __init__(self):
      threading.Thread.__init__(self)
      Thread.__init__(self)

    def run(self):
      with onto: sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
      onto.save()

def clear_string(string):
  nfkd = unicodedata.normalize('NFKD', string)
  cleanedString = "".join([c for c in nfkd if not unicodedata.combining(c)])
  string = re.sub('[^a-zA-Z0-9 \\\]', '', cleanedString).strip().replace(" ", "_").lower()
  return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII')

def normal_string(string):
  return st.capwords(string.replace("_", " "))

def get_name_to_api(obj):
  return normal_string(str(obj).split('.',1)[1])

def get_name_to_onto(obj):
  return str(obj).split('.',1)[1]


def state_to_JSON(state):
  return obj

def UUID():
  return uuid.uuid1()
  
def size_to_id(obj):
  json = {
    "Minimum": 4,
    "Small": 1,
    "Medium": 2,
    "Large": 3,
    "Exceptional": 5,
  }
  return int(json[get_name_to_onto(obj)])

def size_to_portuguese(obj):
  json = {
    "Minimum": "Mínimo",
    "Small": "Pequeno",
    "Medium": "Médio",
    "Large": "Grande",
    "Exceptional": "Excepcional",
    "baixo": "Baixo",
    "alto": "Alto",
    "medio": "Médio",
    "sem_especificacao": "Sem Especificação",
  }
  return str(json[get_name_to_onto(obj)])

