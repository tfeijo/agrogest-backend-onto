from flask import jsonify
from src.models.Classes import *
from src.ontology.config import onto, get_id

class ProductionController: 
 
  def store(productions):
    try:
      new_list = []
      with onto:
        farm = onto.search_one(is_a=Farm, id=productions['farm_id'])
        for production in productions['productions']: 
          id = get_id('Production')
          new = Production(
            f'farm-{farm.id[0]}_{id}',
            id = [id],
            num_animals=[int(production["num_animals"])],
            num_area=[float(production["num_area"])],
            has_activity=[ProductionActivity(production["activity"])],
            has_handling=[ProductionHandling(production["handling"])]
          )
          farm.has_production.append(new)
          if 'cultivation' in production:
            new.has_cultivation = [ProductionCultivation(production["cultivation"])]
          new_list.append(new.to_json())
      onto.save()
      print(new_list)
    except:
      return jsonify({"Error": "Something went wrong in inserting"}), 400
    else:
      try:
        return jsonify(new_list),200
      except:
        return jsonify({'Error':'Inserted but not queried'}),400
    
  def index():
    query = onto.Production.instances()
    productions = []
    for production in query:
      productions.append(production.to_json())
    return jsonify(productions)
