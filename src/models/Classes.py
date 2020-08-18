from owlready2 import *
from src.ontology.config import onto
from src.utils.methods import *

with onto:
  class Device(Thing): pass
  
  class Documents(Thing): pass

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
      for biome in self.biome:
        biomes.append({
          "id": biome.id[0],
          "name": get_name_to_api(biome)
        })
      
      return {
        "id": self.id[0],
        "name": get_name_to_api(self)[:-3],
        "state": {
          "id": self.state[0].id[0],
          "name": get_name_to_api(self.state[0]),
          "uf": self.state[0].uf[0],
        },
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
    def store_json(self):

      return {
        "id": self.id[0],
        "installation_id": get_name_to_api(self.device[0]),
        "hectare": self.hectare[0],
        "city_id": self.city[0].id[0],
        "licensing": self.licensing[0] 
      }

    def show_json(self):
      query_city = onto.search_one(is_a=City, id=self.city[0].id[0])
      biomes = []
      for biome in query_city.biome:
        biomes.append({
              "id": biome.id[0],
              "name": get_name_to_api(biome)
            })
      return {
        "id": self.id[0],
        "installation_id": get_name_to_api(self.device[0]),
        "hectare": self.hectare[0],
        "licensing": self.licensing[0],
        "city": {
          "id": query_city.id[0],
          "name": get_name_to_api(query_city)[:-3],
          "state": {
            "id": query_city.state[0].id[0],
            "name": get_name_to_api(query_city.state[0]),
            "uf": query_city.state[0].uf[0]
          },
          "biomes": biomes,
        },
        "size": {
          "id": size_to_id(self.size[0]),
          "name": get_name_to_onto(self.size[0])
        } 
      }

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

  