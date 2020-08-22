from owlready2 import *
from src.ontology.config import onto
from src.utils.methods import *

with onto:
  class Device(Thing): pass
  
  class Document(Thing): pass

  class State(Thing):
    def to_json(self):
      return {
        "id": self.id[0],
        "name": get_name_to_api(self),
        "uf": self.uf[0],
      }

  class City(Thing):
    def to_json(self):
      biomes = []
      for biome in self.has_biome:
        biomes.append(biome.to_json())
      
      return {
        "id": self.id[0],
        "name": get_name_to_api(self)[:-3],
        "state": self.has_state[0].to_json(),
        "biomes": biomes,
        "fiscal_module": self.fiscal_module[0],
      }

  class Biome(Thing):
    def to_json(self):
      return {
        "id": self.id[0],
        "name": get_name_to_api(self),
      }

  class Farm(Thing):
    
    def to_json(self):

      return {
        "id": self.id[0],
        "installation_id": get_name_to_api(self.is_created_by[0]),
        "hectare": self.hectare[0],
        "licensing": self.licensing[0],
        "city": self.has_city[0].to_json(),
        "size": {
          "id": size_to_id(self.has_size[0]),
          "name": size_to_portuguese(self.has_size[0])
        } 
      }

  class Parameter(Thing): pass

  class Size(Thing): pass

  class Factor(Thing): pass

  class Production(Thing): pass

  class ProductionActivity(Thing): pass

  class Measurement(Thing): pass

  class ProductionSystem(Thing): pass

  class ProductionHandling(Thing): pass

  Size('Minumum')
  Size('Small')
  Size('Medium')
  Size('Large')
  Size('Exceptional')