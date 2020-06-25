import unicodedata
import re
from src.models.Classes import *

def clear_string(string):
  nfkd = unicodedata.normalize('NFKD', string)
  cleanedString = "".join([c for c in nfkd if not unicodedata.combining(c)])
  string = re.sub('[^a-zA-Z0-9 \\\]', '', cleanedString).strip().replace(" ", "_")
  return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII')

def normal_string(string):
  return string.replace("_", " ")

def get_name(obj):
  return normal_string(str(obj).split('.',1)[1])

def state_to_JSON(state):
  
  return obj