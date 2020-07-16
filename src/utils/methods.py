import unicodedata
import uuid 
import re
from src.models.Classes import *

def clear_string(string):
  nfkd = unicodedata.normalize('NFKD', string)
  cleanedString = "".join([c for c in nfkd if not unicodedata.combining(c)])
  string = re.sub('[^a-zA-Z0-9 \\\]', '', cleanedString).strip().replace(" ", "_")
  return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII')

def normal_string(string):
  return string.replace("_", " ")

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
