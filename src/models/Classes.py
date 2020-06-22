from owlready2 import *
from src.ontology.config import onto

with onto:
  class State(Thing): pass

  class City(Thing): pass

  class Biome(Thing): pass

  class Farm(Thing): pass

  class Parameter(Thing): pass

  class Size(Thing): pass

  class Minimum(Size): pass
  
  class Small(Size): pass

  class Medium(Size): pass
  
  class Large(Size): pass
  
  class Exceptional(Size): pass

  class Factor(Thing): pass

  class Production(Thing): pass

  class ProductionActivity(Thing): pass

  class Measurement(Thing): pass

  class ProductionSystem(Thing): pass

  class ProductionHandling(Thing): pass


  ###########################################
  # OBJECT PROPERTIES
  class has_city(ObjectProperty):
    domain = [State]
    range = [City]

  class is_city_of(ObjectProperty):
    domain = [City]
    range = [State]
    inverse_property = has_city

  class has_parameter(ObjectProperty):
    domain = [State]
    range = [Parameter]

  class is_parameter_of(ObjectProperty):
    domain = [Parameter]
    range = [State]
    inverse_property = has_parameter

  class has_biome(ObjectProperty):
    domain = [City]
    range = [Biome]

  class is_biome_of(ObjectProperty):
    domain = [Biome]
    range = [City]
    inverse_property = has_biome
  
  class has_farm(ObjectProperty):
    domain = [City]
    range = [Farm]

  class is_farm_of(ObjectProperty):
    domain = [Farm]
    range = [City]
    inverse_property = has_farm
  
  class has_size(ObjectProperty):
    domain = [Farm, Factor,Production]
    range = [Size,Minimum,Small,Medium,Large, Exceptional]

  class is_size_of(ObjectProperty):
    domain = [Size,Small,Medium,Large]
    range = [Farm, Factor,Production]
    inverse_property = has_size
  
  class has_activity(ObjectProperty):
    domain = [Farm, Parameter, Production]
    range = [ProductionActivity]

  class is_activity_of(ObjectProperty):
    domain = [ProductionActivity]
    range = [Farm, Parameter, Production]
    inverse_property = has_activity
  
  class has_measurement(ObjectProperty):
    domain = [Parameter]
    range = [Measurement]

  class is_measurement_of(ObjectProperty):
    domain = [Measurement]
    range = [Parameter]
    inverse_property = has_measurement
  
  class has_factor(ObjectProperty):
    domain = [Parameter]
    range = [Factor]

  class is_factor_of(ObjectProperty):
    domain = [Factor]
    range = [Parameter]
    inverse_property = has_factor
  
  class has_production(ObjectProperty):
    domain = [Farm]
    range = [Production]

  class is_production_of(ObjectProperty):
    domain = [Production]
    range = [Farm]
    inverse_property = has_production
  
  class has_production_system(ObjectProperty):
    domain = [ProductionActivity]
    range = [ProductionSystem]

  class is_production_system_of(ObjectProperty):
    domain = [ProductionSystem]
    range = [ProductionActivity]
    inverse_property = has_production_system
  
  class has_production_handling(ObjectProperty):
    domain = [ProductionSystem]
    range = [ProductionHandling]

  class is_production_handling_of(ObjectProperty):
    domain = [ProductionHandling]
    range = [ProductionSystem]
    inverse_property = has_production_handling

  
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
  ###########################################
  # OBJECT PROPERTIES
  class fiscal_module(DataProperty):
    range = [int]

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