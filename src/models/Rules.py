from owlready2 import *
from src.ontology.config import onto
from src.models.Classes import *
from src.models.ObjectProperties import *
from src.models.DataProperties import *
import owlready2

with onto:
  '''
  SWRL rules can be used to integrate ‘if… then…’ rules in ontologies.

  Note: loading SWRL rules is only supported from RDF/XML and NTriples
  files, but not from OWL/XML files.
  class Drug(Thing): pass
  
  class number_of_tablets(Drug >> int, FunctionalProperty): pass
  class price(Drug >> float, FunctionalProperty): pass
  class price_per_tablet(Drug >> float, FunctionalProperty): pass

  rule = Imp()
  rule.set_as_rule("""
                    Drug(?d),
                    price(?d, ?p),
                    number_of_tablets(?d, ?n),
                    divide(?r, ?p, ?n)
                    -> price_per_tablet(?d, ?r)
                  """)
  drug = Drug(number_of_tablets = 10, price = 25.0)
  sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
  drug.price_per_tablet
  2.5
  '''
  # 
  rules = [
    {
      'name': 'Farm has state associated from city',
      'desc': """
              City(?c),
              has_city(?f, ?c),
              has_state(?c, ?s)
                -> has_state_associated(?f, ?s)
            """
    },{
      'name': 'Farm has biome associated from city',
      'desc': """
                City(?c),
                has_city(?f, ?c),
                has_biome(?c, ?b)
                  -> has_biome_associated(?f, ?b)
              """
    },{
      'name': 'Farm has fiscal module associated from city',
      'desc': """
                City(?c),
                Farm(?f),
                has_city(?f, ?c),
                fiscal_module(?c, ?fm)
                  -> fiscal_module(?f, ?fm)
              """
    },{ 
      'name': 'Divide fm by Farm Size and insert result_fm',
      'desc': """
                City(?c),
                has_city(?f, ?c),
                fiscal_module(?c, ?fm),
                hectare(?f, ?hec),
                divide(?r, ?hec, ?fm)
                  -> result_fm(?f, ?r)
              """
    },{
      'name': 'result_fm <= 4 -> Size = Small',
      'desc': """
                result_fm(?f, ?r),
                lessThanOrEqual(?r, 4.0)
                  -> has_size(?f, Small)
              """
    },{
      'name': 'result_fm > 4 || <= 15 -> Size = Medium',
      'desc': """
                result_fm(?f, ?r),
                greaterThan(?r, 4.0), lessThanOrEqual(?r, 15.0)
                  -> has_size(?f, Medium)
              """
    },{
      'name': 'result_fm == 15 -> Size = Medium',
      'desc': """
                result_fm(?f, ?r),
                greaterThan(?r, 15.0)
                  -> has_size(?f, Large)"""
    },
    {
      'name': 'Farm has_document_associated',
      'desc': """
                Farm(?f),
                Document(?d),
                ProductionActivity(?pa),
                has_production_associated(?d,?pa),
                has_production(?f,?pa),
                  -> has_document_associated(?f, ?d)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Production(?prod),
      has_measurement(?prod, modulo_fiscal),
      is_production_of(?prod,?fa),
      result_fm(?fa,?fm)
        -> result_prod(?prod,?fm)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Production(?prod),
      has_measurement(?prod, area),
      is_production_of(?prod,?fa),
      hectare(?fa,?fm)
        -> result_prod(?prod,?fm)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Production(?prod),
      has_measurement(?prod, n_de_cabecas),
      num_animals(?prod,?fm)
        -> result_prod(?prod,?fm)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Production(?prod),
      has_measurement(?prod, area_de_pastagem),
      num_area(?prod,?fm)
        -> result_prod(?prod,?fm)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Production(?prod),
      has_measurement(?prod, vacas_em_lactacao),
      num_animals(?prod,?fm),
      multiply(?r, 0.7, ?fm)
        -> result_prod(?prod,?r)"""
    },
    {
      'name': 'Parameter association',
      'desc': """
      Production(?prod),
      has_state_associated(?prod, ?st),
      has_activity(?prod, ?act),
      has_handling(?prod, ?hand),
      
      is_agricultura(?prod,?isAg),
      equal(?isAg,false),

      Parameter(?param),
      has_state_associated(?param, ?st),
      has_activity(?param, ?act),
      has_handling(?param, ?hand)
      
        -> has_parameter_associated(?prod, ?param)"""
    },
    {
      'name': 'Parameter association',
      'desc': """
      Production(?prod),
      has_state_associated(?prod, ?st),
      has_activity(?prod, ?act),

      is_agricultura(?prod,?isAg),
      equal(?isAg,false),
      
      Parameter(?param),
      has_state_associated(?param, ?st),
      has_activity(?param, ?act),

      has_handling(?param, sem_especificacao),
      
        -> has_parameter_associated(?prod, ?param)"""
    },
    {
      'name': 'Parameter association - agriculture',
      'desc': """
      Parameter(?param),
      has_state_associated(?param, ?st),
      has_activity(?param, ?act),
      
      Production(?prod),
      has_state_associated(?prod, ?st),
      has_activity(?prod, ?act),
      
      is_agricultura(?prod,?isAg),
      equal(?isAg,true),

      has_handling(?prod, ?hand),
      has_cultivation(?prod, ?cult),
      has_handling(?param, ?hand),
      has_cultivation(?param, ?cult),
        -> has_parameter_associated(?prod, ?param)"""
    },
    {
      'name': 'Parameter association - agriculture',
      'desc': """
      Parameter(?param),
      has_state_associated(?param, ?st),
      has_activity(?param, ?act),
      Production(?prod),
      has_state_associated(?prod, ?st),
      has_activity(?prod, ?act),
      
      is_agricultura(?prod,?isAg),
      equal(?isAg,true),

      has_cultivation(?prod, ?cult),
      has_handling(?param, sem_especificacao),
      has_cultivation(?param, ?cult),

        -> has_parameter_associated(?prod, ?param)"""
    },
    {
      'name': 'Parameter association - agriculture',
      'desc': """
      Parameter(?param),
      has_activity(?param, ?act),
      has_state_associated(?param, ?st),
      Production(?prod),
      has_state_associated(?prod, ?st),
      has_activity(?prod, ?act),

      is_agricultura(?prod,?isAg),
      equal(?isAg,true),
      
      has_handling(?prod, ?hand),
      has_handling(?param, ?hand),
      has_cultivation(?param, sem_especificacao),
        -> has_parameter_associated(?prod, ?param)"""
    },
    {
      'name': 'Parameter association - agriculture',
      'desc': """
      Parameter(?param),
      has_activity(?param, ?act),
      has_state_associated(?param, ?st),
      Production(?prod),
      has_state_associated(?prod, ?st),
      has_activity(?prod, ?act),

      is_agricultura(?prod,?isAg),
      equal(?isAg,true),
      
      has_handling(?param,  sem_especificacao),
      has_cultivation(?param, sem_especificacao),
      
        -> has_parameter_associated(?prod, ?param)"""
    },
    
    {
      'name':'Factor association',
      'desc': """
      Production(?prod),
      has_parameter_associated(?prod,?param),
      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },

  ]

  for rule in rules:
    insert_rule = Imp()
    insert_rule.set_as_rule(rule['desc'])
