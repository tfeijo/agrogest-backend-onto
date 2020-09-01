from flask import jsonify
from src.models.Classes import *
from src.ontology.config import onto, increase_id

class ParameterController:
  def index():
    parameter_query = onto.Parameter.instances()
    parameters = []
    for query in parameter_query: parameters.append(query.to_json())
    return jsonify(parameters)

  def store(parameter):

    id = increase_id('Parameter')
    state = None
    states = onto.State.instances()
    for uf in states:
      uf_name = str(uf).split('.',1)[1]
      if uf_name.upper() == parameter['state']: state = uf
    
    if parameter['activity'] != 'agricultura':
      name = f'{state.uf[0]}_{parameter["activity"]}_{parameter["handling"]}\
_{parameter["measurement"]}_{id}'
    else:
      name = f'{state.uf[0]}_{parameter["activity"]}_{parameter["cultura"]}\
_{parameter["handling"]}_{parameter["measurement"]}_{id}'

    activity = onto.ProductionActivity(parameter['activity'])
    handling = onto.ProductionHandling(parameter['handling'])
    measurement = onto.Measurement(parameter['measurement'])
    
    new = Parameter(name)
    new.id = [id]
    if parameter['cultura'] != None:
      new.has_cultivation=[ProductionCultivation(parameter['cultura'])]
    new.has_state_associated=[state]
    if parameter['factor'] != None:
      new.has_factor=[Factor(parameter['factor'])]
    new.has_state_associated=[state]
    new.has_activity=[activity]
    new.has_handling=[handling]
    new.has_measurement=[measurement]
    new.base=[int(parameter['base'])]
    new.min=[int(parameter['min'])]
    new.sma=[int(parameter['sma'])]
    new.medi=[int(parameter['medi'])]
    new.larg=[int(parameter['larg'])]
    new.excep=[int(parameter['excep'])]
    
    onto.save()
    
    return jsonify({})
