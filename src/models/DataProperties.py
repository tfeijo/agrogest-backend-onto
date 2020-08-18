from owlready2 import *
from src.ontology.config import onto
from src.models.Classes import *

with onto:

  '''  
  DATA PROPERTIES
    int
    float
    bool
    str (string)
    owlready2.normstr (normalized string, a single-line string)
    owlready2.locstr (localized string, a string with a language associated)
    datetime.date
    datetime.time
    datetime.datetime

  with onto:
    class has_for_synonym(DataProperty):
      range = [str]

  acetaminophen.has_for_synonym = ["acetaminophen", "paracétamol"]

  '''
  class fiscal_module(DataProperty):
    range = [float]
    python_name = 'fiscal_module'

  class result_fm(DataProperty):
    range = [float]
  
  class id(DataProperty):
    range = [int]
    python_name = 'id'

  class uf(DataProperty):
    range = [str]
    domain = [State]
    python_name = 'uf'

  class hectare(DataProperty):
    range = [float]
    python_name = 'hectare'

  class unique_id(DataProperty):
    range = [str]

  class hectare(DataProperty):
    range = [float]

  class prod_milk(DataProperty):
    range = [bool]

  class prod_beef(DataProperty):
    range = [bool]

  class prod_aviculture(DataProperty):
    range = [bool]

  class prod_pig(DataProperty):
    range = [bool]

  class prod_agriculture(DataProperty):
    range = [bool]

  class licensing(DataProperty):
    range = [bool]
    python_name = 'licensing'