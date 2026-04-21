from owlready2 import DataProperty

from src.models.Classes import State
from src.ontology.config import onto


with onto:

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

  class description(DataProperty):
    range = [str]
    python_name = 'description'

  class url(DataProperty):
    range = [str]
    python_name = 'url'

  class question_title(DataProperty):
    range = [str]
    python_name = 'question_title'

  class hectare(DataProperty):
    range = [float]
    python_name = 'hectare'

  class unique_id(DataProperty):
    range = [str]

  class licensing(DataProperty):
    range = [bool]
    python_name = 'licensing'

  class is_file(DataProperty):
    range = [bool]
    python_name = 'is_file'

  class answer(DataProperty):
    range = [bool]
    python_name = 'answer'

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
