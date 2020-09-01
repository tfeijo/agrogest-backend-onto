from flask import jsonify
from src.models.Classes import *
from src.ontology.config import onto, increase_id, decrease_id

class ProductionController: 
 
  def store(productions):
    try:
      new_list = []
      with onto:
        farm = onto.search_one(is_a=Farm, id=productions['farm_id'])
        for production in productions['productions']: 
          id = increase_id('Production')
          new = Production(
            f'farm-{farm.id[0]}_{id}',
            id = [id],
            num_area=[float(production["num_area"])],
            has_activity=[ProductionActivity(clear_string(production["activity"]))],
            has_handling=[ProductionHandling(clear_string(production["handling"]))],
            has_state_associated=farm.has_state_associated
          )
          farm.has_production.append(new)
          
          if 'cultivation' in production:
            new.is_agricultura = [True]
            new.num_animals = [0]
            new.has_cultivation = [ProductionCultivation(clear_string(production["cultivation"]))]
          else:
            new.num_animals = [int(production["num_animals"])]
            new.is_agricultura = [False]
            
          new_list.append(new)
      
      with onto: sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
      onto.save()
      
    except Exception as e:
      decrease_id('Production')
      return jsonify({
        "Error": "Something went wrong in inserting",
        "msg": e
      }), 400
    else:
      try:
        list_retorned = []
        param = Parameter("sem_especificacao")
        for item in new_list:
          if item.has_parameter_associated == []:
            item.has_parameter_associated = [param]
            item.has_size = [param]
            item.has_factor_associated = [param]
            onto.save()
          
          if item.has_parameter_associated[0] != param and item.has_size == [] :
            item.has_size = [param]
            onto.save()

          if item.has_parameter_associated[0] != param and item.has_factor_associated == [] :
            item.has_factor_associated = [param]
            onto.save()

          list_retorned.append(item.to_json())
        
        return jsonify(list_retorned),200
      except Exception as e:
        return jsonify({
          'Error':'Inserted but not queried',
          "msg": e
        }),400
    
  def index():
    query = onto.Production.instances()
    productions = []
    for production in query:
      productions.append(production.to_json())
    return jsonify(productions)
