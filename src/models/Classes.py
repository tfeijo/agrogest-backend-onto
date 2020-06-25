from owlready2 import *
from src.ontology.config import onto
from src.utils.methods import *

with onto:
  class Device(Thing): pass

  class State(Thing):
    def to_json(self):
      return {
        "id": self.id[0],
        "name": get_name(self),
        "uf": self.uf[0],
      }

  class City(Thing):
    def to_json(self):
      query_biomes = onto.search(is_a=Biome, is_biome_of=[self])
      
      biomes = []
      for biome in query_biomes:
        
        biomes.append({
          "id": biome.id[0],
          "name": get_name(biome)
        })
      return {
        "id": self.id[0],
        "name": get_name(self)[:-3],
        "state": {
          "id": self.state[0].id[0],
          "name": get_name(self.state[0]),
          "uf": self.state[0].uf[0],
        },
        "biomes": biomes,
        "fiscal_module": self.fiscal_module[0],
      }

  class Biome(Thing):
    def to_json(self):
      return {
        "id": self.id[0],
        "name": get_name(self),
      }

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

  