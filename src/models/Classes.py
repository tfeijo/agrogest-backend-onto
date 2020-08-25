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

  class Parameter(Thing):
    def to_json(self):
      obj = {
        "id": self.id[0],
        "has_measurement": get_name_to_api(self.has_measurement[0]),
        "has_handling": get_name_to_api(self.has_handling[0]),
        "has_state_associated": get_name_to_api(self.has_state_associated[0]),
        "has_activity": get_name_to_api(self.has_activity[0]),
        "minimum": self.min[0],
        "small": self.sma[0],
        "medium": self.medi[0],
        "large": self.larg[0],
        "exceptional": self.excep[0],
        "base": self.base[0],
      }
      if self.has_factor:
        obj["has_factor"] = get_name_to_api(self.has_factor[0])
      if self.has_cultivation:
        obj["has_cultivation"] = get_name_to_api(self.has_cultivation[0])
      
      return (obj)
      

  class Size(Thing): pass

  class Factor(Thing): pass

  class Production(Thing):
     def to_json(self):
      return {
        "id": self.id[0],
        "has_activity": get_name_to_api(self.has_activity[0]),
        "num_area": self.num_area[0],
        "num_animals": self.num_animals[0],
        "has_handling": get_name_to_api(self.has_handling[0]),
        "is_production_of": get_name_to_api(self.is_production_of[0])
      } 

  class ProductionActivity(Thing): pass

  class Measurement(Thing): pass

  class ProductionHandling(Thing): pass

  class ProductionCultivation(Thing): pass

  Size('Minimum')
  Size('Small')
  Size('Medium')
  Size('Large')
  Size('Exceptional')