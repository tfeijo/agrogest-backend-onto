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

  