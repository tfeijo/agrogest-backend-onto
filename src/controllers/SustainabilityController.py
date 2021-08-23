from flask import jsonify, json

class SustainabilityController():
  def index(production_type = None):
    r = open('./src/ontology/last_id_fullontology.json', "r")
    data = json.load(r)
    farms = data["farms"]

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

      farms = farms_filtered

    indicators_state_temp = {}
    documents_average_state_temp = {}
    indicator_by_size_temp = {
      "Pequeno" : {},
      "Médio" : {},
      "Grande": {}
    }
    indicator_by_production_temp = {
      "Suinocultura": {},
      "Bovinocultura De Leite": {},
      "Bovinocultura De Corte": {},
      "Agricultura": {},
      "Avicultura": {}
    }

    for farm in farms:
      uf = farm['city']['state']['uf']

      if not uf in documents_average_state_temp:
        documents_average_state_temp[uf] = {}
        documents_average_state_temp[uf]['doc'] = 0
        documents_average_state_temp[uf]['farm'] = 0
      
      documents_average_state_temp[uf]['doc'] += len(farm["documents"])
      documents_average_state_temp[uf]['farm'] += 1

      if not uf in indicators_state_temp: indicators_state_temp[uf] = {}

      for production in farm['productions']:
        for indicator in farm['indicators']:
          if not indicator in indicator_by_production_temp[production['activity']]:
            indicator_by_production_temp[production['activity']][indicator] = 1
          else:
            indicator_by_production_temp[production['activity']][indicator] += 1
          
          if indicator in indicators_state_temp[uf]:
            indicators_state_temp[uf][indicator] += 1
          else:
            indicators_state_temp[uf][indicator] = 1
          
          if not indicator in indicator_by_size_temp[farm["size"]["name"]]:
            indicator_by_size_temp[farm["size"]["name"]][indicator] = 1
          else:
            indicator_by_size_temp[farm["size"]["name"]][indicator] += 1


    total_indicators = []
    obj_temp = {}
    
    indicator_by_state_temp = {}
    for state in indicators_state_temp:
      indicator_by_state_temp[state] = None
      larger = 0

      for indicator in indicators_state_temp[state]:
        if indicators_state_temp[state][indicator] > larger:
          indicator_by_state_temp[state] = indicator
          larger = indicators_state_temp[state][indicator]
      
        if indicator in obj_temp:
          obj_temp[indicator] += indicators_state_temp[state][indicator]
        else:
          obj_temp[indicator] = 1
    
    indicator_by_state = []
    for state in indicator_by_state_temp:
      indicator_by_state.append([state,indicator_by_state_temp[state]])
      
    for indicator in obj_temp:
      total_indicators.append([indicator, obj_temp[indicator]])
    
    documents_average_state = []
    for document in documents_average_state_temp:
      average = documents_average_state_temp[document]['doc']/documents_average_state_temp[document]['farm']
      documents_average_state.append([document, average])
      
    indicator_by_production = [[],]
    for production in indicator_by_production_temp:
      list_temp = [production]
      for indicator in indicator_by_production_temp[production]:
        if not indicator in indicator_by_production[0]:
          indicator_by_production[0].append(indicator)

      for indicator in indicator_by_production[0]:
        if not indicator in indicator_by_production_temp[production]:
          list_temp.append(0)
        else:
          list_temp.append(indicator_by_production_temp[production][indicator])
      
      indicator_by_production.append(list_temp)
    indicator_by_production[0].insert(0,"Produção")

    indicator_by_size = [[],]
    for size in indicator_by_size_temp:
      list_temp = [size]

      for indicator in indicator_by_size_temp[size]:
        if not indicator in indicator_by_size[0]:
          indicator_by_size[0].append(indicator)

      for indicator in indicator_by_size[0]:
        if not indicator in indicator_by_size_temp[size]:
          list_temp.append(0)
        else:
          list_temp.append(indicator_by_size_temp[size][indicator])
      
      indicator_by_size.append(list_temp)
    indicator_by_size[0].insert(0,"Tamanho")

    return jsonify({
      "indicator_by_state": indicator_by_state,
      "total_indicators": total_indicators,
      "documents_average_state": documents_average_state,
      "indicator_by_production": indicator_by_production,
      "indicator_by_size": indicator_by_size
    })