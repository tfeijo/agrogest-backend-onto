from flask import jsonify
from owlready2 import *
from src.models.Classes import *
from src.models.Rules import *
from src.ontology.config import onto, infered

class CityController:
  def index():
    state = State('MG')
    biome1 = Biome('Caatinga')
    biome2 = Biome('Mata_Atlantica')
    city = City('JUIZ_DE_FORA',
                biome = [biome2,biome1],
                fiscal_module=[25.0],
                state=[state])
    farm = Farm('Farm1', city=[city], hectare=[375.1])
    

    with onto:
      sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
    
      onto.save(file = "./src/ontology/bd_infered.owl", format = "rdfxml")


    # print(onto.get_parents_of(farm))
    print()

    # farm_query = onto["Farm"].individuals
    # >>> onto.search_one(is_a = onto.Pizza)
    # >>> onto.search_one(label = "my label")
    # >>> onto.search(is_a = onto.Pizza, has_topping = onto.search(is_a = onto.TomatoTopping))

    print(f'Return: {infered.search_one(is_a  = infered["Farm"])}')
    return jsonify({})

  def show(id):
    city1 = City('Cidade1', id)
    return jsonify(city1.toJSON())
  
  def index_by_state(state_id):
    city1 = City('Cidade1')
    city2 = City('Cidade2')
    cities= [city1.toJSON(),city2.toJSON()]
    return jsonify(cities)

  def index_by_biome(biome_id):
    city1 = City('Cidade1')
    city2 = City('Cidade2')
    cities= [city1.toJSON(),city2.toJSON()]
    return jsonify(cities)
