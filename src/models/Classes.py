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
      print(self.biome)
      
      biomes = []
      for biome in sel:
        biomes.append({
          "id": biome.id[0],
          "name": get_name(biome)
        })
      
      return {
        "id": self.id[0],
        "name": get_name(self)[:-3],
        # "state": {
        #   "id": self.state[0].id[0],
        #   "name": get_name(self.state[0]),
        #   "uf": self.state[0].uf[0],
        # },
        # "biomes": biomes,
        # "fiscal_module": self.fiscal_module[0],
      }

  class Biome(Thing):
    def to_json(self):
      return {
        "id": self.id[0],
        "name": get_name(self),
      }

  class Farm(Thing):
    def store_json(self):
      sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
      
      return {
        "id": self.id[0],
        "installation_id": get_name_to_onto(self.device[0]),
        "hectare": self.hectare[0],
        "city_id": self.city[0].id[0],
        "licensing": self.licensing[0],
        "size_id": str(self.size[0]),
      }

    def show_json(self):
      sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
      
      return {
        "id": self.id[0],
        "installation_id": str(self.device),
        "hectare": self.hectare[0],
        "city_id": str(self.city.id),
        "licensing": self.licensing[0],
        "size_id": str(self.size[0]),
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

  