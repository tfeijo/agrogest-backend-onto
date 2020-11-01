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

  class url(DataProperty):
    range = [str]
    python_name = 'url'

  class hectare(DataProperty):
    range = [float]
    python_name = 'hectare'

  class unique_id(DataProperty):
    range = [str]

  class hectare(DataProperty):
    range = [float]

  class licensing(DataProperty):
    range = [bool]
    python_name = 'licensing'

  class is_agricultura(DataProperty):
    range = [bool]
    python_name = 'is_agricultura'
  
  class base(DataProperty):
    range = [float]
    python_name = 'base'
  
  class top(DataProperty):
    range = [float]
    python_name = 'top'
  
  class min(DataProperty):
    range = [float]
    python_name = 'min'
  
  class sma(DataProperty):
    range = [float]
    python_name = 'sma'
  
  class medi(DataProperty):
    range = [float]
    python_name = 'medi'

  class larg(DataProperty):
    range = [float]
    python_name = 'larg'

  class excep(DataProperty):
    range = [float]
    python_name = 'excep'

  class num_animals(DataProperty):
    range = [int]
    python_name = 'num_animals'

  class num_area(DataProperty):
    range = [float]
    python_name = 'num_area'

  class result_prod(DataProperty):
    range = [float]
    python_name = 'result_prod'
  
