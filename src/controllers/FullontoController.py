import string
from flask import jsonify
from owlready2 import World, OwlReadyError
from src.models.Classes import farm_to_json
from src.utils.methods import Ontology, get_name_to_onto,\
clear_string,size_to_name_onto,all_attributes

class FullontoController():
  
  def index():
    default_world = World(filename = "./src/ontology/interlink.sqlite3", exclusive=False)
    interlink = default_world.get_ontology("./src/ontology/interlink.owl").load()
    sustainability = list(interlink.imported_ontologies)[0]
    ontogest = list(interlink.imported_ontologies)[1]
       
    list_onto = list(ontogest.classes())
    list_sust = list(sustainability.classes())
    
    sustainability.destroy()
    ontogest.destroy()
    interlink.destroy()
    default_world.close()

    return jsonify({
      "ontogest": str(list_onto),
      "sustainability": str(list_sust)
      })

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
          print(name_prod)
        new.has_production.append(new_prod)
      except:
        print("Empty production")
        new.has_production = []
      
      return jsonify({"Farm inserted": str(new)}), 200
    
    except OwlReadyError as e:
      print(f'Something went wrong in inserting: {e}')
      return jsonify({"Error": "Something went wrong in inserting"}), 400

    finally:
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