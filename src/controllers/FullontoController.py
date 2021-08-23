import string
from flask import json, jsonify
from owlready2 import World, OwlReadyError, sync_reasoner_pellet
from src.models.Classes import farm_to_json
from src.controllers.FarmController import FarmController
from src.utils.methods import Ontology, get_name_to_onto,\
clear_string,size_to_name_onto,all_attributes

class FullontoController():
  
  def index(production_type = None):
    # Bovinocultura De Leite
    # Bovinocultura de Corte
    # Avicultura
    # Suinocultura
    # Agricultura

    FarmController.index()
    r = open('./src/ontology/static_farms.json', "r")
    data = json.load(r)
    last_id = data["last_id"]

    r = open('./src/ontology/last_id_fullontology.json', "r")
    data = json.load(r)
    last_id_full = data["last_id"]
    farms = data["farms"]

    default_world = World(filename = "./src/ontology/interlink.sqlite3", exclusive=False)
    interlink = default_world.get_ontology("./src/ontology/interlink.owl").load()
    sustainability = None
    ontogest = None

    for ontology in interlink.imported_ontologies:
      if "ontogest" in str(ontology): ontogest = ontology
      if "sustainability" in str(ontology): sustainability = ontology
    
    try:
      if last_id > last_id_full:
        w = open('./src/ontology/last_id_fullontology.json', "w")

        farms = []
        with ontogest:
          for farm in ontogest.Farm.instances():

            farm_json = farm_to_json(farm)
            farm_json["indicators"] = {}
            total = {
              "Bioeconomia": 9,
              "Conservação dos recursos hidrícos": 9,
              "Emissão de carbono": 9,
              "Fonte de energias renováveis": 8,
              "Gestão de resíduos": 5,
              "Métodos Naturais de Controle de Adversidades": 7,
              "Proteção da biodiversidade": 12,
              "Responsabilidade Corporativa": 18,
              "Redução do desmatamento": 14
            }

            for document in farm_json["documents"]:
              for indicator in document["indicators"]:
                if indicator not in farm_json["indicators"]:
                  farm_json["indicators"][indicator] = [1,total[indicator]]
                else:
                  farm_json["indicators"][indicator] = [farm_json["indicators"][indicator][0] + 1, total[indicator]]

            farms.append(farm_json)

          json.dump({
            "last_id": last_id,
            "farms": farms
          }, w)
      if production_type != None:
        farms_filtered = []
        for farm in farms:
          insert = False
          for production in farm["productions"]:
            if production['activity'].upper() == production_type.upper():
              insert = True
              break
          if insert:
            farms_filtered.append(farm)
          
        return jsonify(farms_filtered)

      return jsonify(farms)

    except OwlReadyError as e:
      print(f'Something went wrong in query: {e}')
      return jsonify({"Error": "Something went wrong in query"}), 400

    finally:
      ontogest.destroy()
      interlink.destroy()
      sustainability.destroy()
      default_world.close()

  def index_id(id):
    r = open('./src/ontology/last_id_fullontology.json', "r")
    data = json.load(r)
    last_id_full = data["last_id"]
    farms = data["farms"]

    for farm in farms:
      if farm['id'] == id:
        return jsonify(farm)
      
    return jsonify({"Error": "Not found"})

  
  def store(farm):
    default_world = World(filename = "./src/ontology/interlink.sqlite3", exclusive=False)
    interlink = default_world.get_ontology("./src/ontology/interlink.owl").load()

    ontogest = list(interlink.imported_ontologies)[0]

    try:
      city_name = f'{clear_string(farm["city"]["name"])}_{farm["city"]["state"]["uf"]}'.upper()
      state_name = string.capwords(f'{clear_string(farm["city"]["state"]["name"])}'.replace("_"," ")).replace(" ","_").replace("Do", "do").replace("De", "de")
      device_name = farm['installation_id']
      device = ontogest.Device(device_name)
      new = ontogest.Farm(f'{get_name_to_onto(device)}_{farm["id"]}')
      new.id = [int(farm["id"])]
      new.hectare = [float(farm["hectare"])]
      new.is_created_by = [device]
      new.result_fm = [float(farm["result_fm"])]
      new.has_city = [ontogest.City(city_name)]
      new.has_size = [ontogest.Size(size_to_name_onto(farm["size"]["name"]))]
      new.has_state_associated = [ontogest.State(state_name)]

      try:
        new.has_biome_associated = []
        for biome in farm["city"]["biomes"]:
          new.has_biome_associated.append(ontogest.Biome(biome["name"].replace("_"," ").replace("â","a").replace("ô","o")))
      except:
        new.has_biome_associated = []
      
      try:
        new.has_recommended_document = []
        for document in farm["documents"]:
          new.has_recommended_document.append(ontogest.Document(f"Document_{document['id']}"))
      except:
        new.has_recommended_document = []

      try:
        new.has_attribute = []
        for key in farm["attributes"]:
          if key!="farm_id":
            new.has_attribute.append(ontogest.Attribute(key))
        for key in all_attributes():
          if key !="farm_id" and key not in farm["attributes"]:
              new.has_missing_attribute.append(ontogest.Attribute(key))
      except:
        new.has_attribute = []
 
      try:  
        new.has_production = [] 
        for production in farm["productions"]:
          name_prod = f'farm-{farm["id"]}_{clear_string(production["activity"])}_{production["id"][0]}'
          new_prod = ontogest.Production(name_prod)
          new_prod.id=[int(production["id"][0])]
          new_prod.num_area=[float(production["num_area"])]
          new_prod.has_activity=[ontogest.ProductionActivity(clear_string(production["activity"]))]
          new_prod.has_handling=[ontogest.ProductionHandling(clear_string(production["handling"]))]
          new_prod.has_state_associated=[ontogest.State(state_name)]
          new_prod.has_size=[ontogest.Size(size_to_name_onto(production["size"]))]
          new_prod.has_factor_associated=[ontogest.Factor(clear_string(production["factor"]).lower())]
          
          if 'cultivation' in production:
            new_prod.is_agricultura = [True]
            new_prod.num_animals = [0]
            new_prod.has_cultivation = [ontogest.ProductionCultivation(clear_string(production["cultivation"]))]
          else:
            new_prod.num_animals = [int(production["num_animals"])]
            new_prod.is_agricultura = [False]
        new.has_production.append(new_prod)
      except:
        print("Empty production")
        new.has_production = []
      
      return jsonify({"Farm inserted": farm_to_json(new)}), 200
    
    except OwlReadyError as e:
      print(f'Something went wrong in inserting: {e}')
      return jsonify({"Error": "Something went wrong in inserting"}), 400

    finally:
      with interlink:
        sync_reasoner_pellet(default_world, infer_property_values = True, infer_data_property_values = True)
      
      ontogest.save()
      ontogest.destroy()
      interlink.save()
      interlink.destroy()
      default_world.close()

  def show(id):
    default_world = World(filename = "./src/ontology/ontogest.sqlite3", exclusive=False)
    ontogest = default_world.get_ontology("./src/ontology/ontogest.owl").load()
    farm = ontogest.search_one(is_a=ontogest.Farm, id=id)
    
    if farm == None: return jsonify({ 'error': 'Not found'}), 404
    json = farm_to_json(farm)
    
    ontogest.destroy()
    default_world.close()
    return jsonify(json)