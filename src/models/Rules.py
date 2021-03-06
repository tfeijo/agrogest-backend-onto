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
                Farm(?f),
                fiscal_module(?f, ?fm),
                hectare(?f, ?hec),
                divide(?r, ?hec, ?fm)
                  -> result_fm(?f, ?r)
              """
    },{
      'name': 'result_fm <= 4 -> Size = Small',
      'desc': """
                Farm(?f),
                result_fm(?f, ?r),
                lessThanOrEqual(?r, 4.0)
                  -> has_size(?f, Small)
              """
    },{
      'name': 'result_fm > 4 || <= 15 -> Size = Medium',
      'desc': """
                Farm(?f),
                result_fm(?f, ?r),
                greaterThan(?r, 4.0), lessThanOrEqual(?r, 15.0)
                  -> has_size(?f, Medium)
              """
    },{
      'name': 'result_fm == 15 -> Size = Medium',
      'desc': """
                Farm(?f),
                result_fm(?f, ?r),
                greaterThan(?r, 15.0)
                  -> has_size(?f, Large)"""
    },

    ################ PARAMETER ASSOCIATION
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

    #####################################
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

    ################ SIZE BASED ON MODULE_FISCAL 
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, modulo_fiscal),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      result_fm(?fa,?result),
      
      base(?param,?floor),
      min(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThanOrEqual(?result,?floor),

      -> has_size(?prod,Minimum)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, modulo_fiscal),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      result_fm(?fa,?result),
      
      base(?param,?floor),
      min(?param,?baseMin),
      sma(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Small)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, modulo_fiscal),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      result_fm(?fa,?result),
      
      base(?param,?floor),
      sma(?param,?baseMin),
      medi(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Medium)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, modulo_fiscal),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      result_fm(?fa,?result),
      
      base(?param,?floor),
      medi(?param,?baseMin),
      larg(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Large)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, modulo_fiscal),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      result_fm(?fa,?result),
      
      base(?param,?floor),
      larg(?param,?baseMin),
      excep(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Exceptional)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, modulo_fiscal),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      result_fm(?fa,?result),
      
      top(?param,?t),
      
      greaterThan(?result,?t),
      
        -> has_size(?prod,sem_especificacao)"""
    },
    ################ SIZE BASED ON AREA
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_da_propriedade),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      hectare(?fa,?result),

      base(?param,?floor),
      min(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Minimum)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_da_propriedade),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      hectare(?fa,?result),
      
      base(?param,?floor),
      min(?param,?baseMin),
      sma(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Small)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_da_propriedade),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      hectare(?fa,?result),
      
      base(?param,?floor),
      sma(?param,?baseMin),
      medi(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Medium)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_da_propriedade),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      hectare(?fa,?result),
      
      base(?param,?floor),
      medi(?param,?baseMin),
      larg(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Large)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_da_propriedade),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      hectare(?fa,?result),
      
      base(?param,?floor),
      larg(?param,?baseMin),
      excep(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Exceptional)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_da_propriedade),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      hectare(?fa,?result),
      
      top(?param,?t),
      
      greaterThan(?result,?t),
      
        -> has_size(?prod,sem_especificacao)"""
    },
    ################ SIZE BASED ON N_DE_CABECAS
    {
      'name': 'Production measurement',
      'desc': """
      
      Parameter(?param),
      has_measurement(?param, n_de_cabecas),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?result),

      base(?param,?floor),
      min(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Minimum)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, n_de_cabecas),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?result),
      
      base(?param,?floor),
      min(?param,?baseMin),
      sma(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Small)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, n_de_cabecas),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?result),
      
      base(?param,?floor),
      sma(?param,?baseMin),
      medi(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Medium)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, n_de_cabecas),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?result),
      
      base(?param,?floor),
      medi(?param,?baseMin),
      larg(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Large)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, n_de_cabecas),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?result),
      
      base(?param,?floor),
      larg(?param,?baseMin),
      excep(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Exceptional)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, n_de_cabecas),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?result),
      
      top(?param,?t),
      
      greaterThan(?result,?t),
        -> has_size(?prod,sem_especificacao)"""
    },
    
    ################ SIZE BASED ON N_DE_AREA
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_de_producao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_area(?prod,?result),

      base(?param,?floor),
      min(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Minimum)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_de_producao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_area(?prod,?result),
      
      base(?param,?floor),
      min(?param,?baseMin),
      sma(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Small)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_de_producao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_area(?prod,?result),

      base(?param,?floor),
      sma(?param,?baseMin),
      medi(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Medium)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_de_producao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_area(?prod,?result),
      
      base(?param,?floor),
      medi(?param,?baseMin),
      larg(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Large)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_de_producao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_area(?prod,?result),

      base(?param,?floor),
      larg(?param,?baseMin),
      excep(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Exceptional)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_de_producao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_area(?prod,?result),
      
      top(?param,?t),
      
      greaterThan(?result,?t),
        -> has_size(?prod,sem_especificacao)"""
    },
    ################ SIZE BASED ON VACAS_EM_LACTACAO
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, vacas_em_lactacao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?fm),
      multiply(?result, 0.7, ?fm),

      base(?param,?floor),
      min(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Minimum)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, vacas_em_lactacao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?fm),
      multiply(?result, 0.7, ?fm),
      
      base(?param,?floor),
      min(?param,?baseMin),
      sma(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Small)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, vacas_em_lactacao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?fm),
      multiply(?result, 0.7, ?fm),
      
      base(?param,?floor),
      sma(?param,?baseMin),
      medi(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Medium)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, vacas_em_lactacao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?fm),
      multiply(?result, 0.7, ?fm),
      
      base(?param,?floor),
      medi(?param,?baseMin),
      larg(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Large)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, vacas_em_lactacao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?fm),
      multiply(?result, 0.7, ?fm),
      
      base(?param,?floor),
      larg(?param,?baseMin),
      excep(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

        -> has_size(?prod,Exceptional)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, vacas_em_lactacao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?fm),
      multiply(?result, 0.7, ?fm),
      
      top(?param,?t),
      greaterThan(?result,?t),
      
        -> has_size(?prod,sem_especificacao)"""
    },
    
    ############
    ############ SAME RULES TO FACTOR ####
    ############
    ################  FACTOR BASED ON MODULO FISCAL

    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, modulo_fiscal),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      result_fm(?fa,?result),
      
      base(?param,?floor),
      min(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, modulo_fiscal),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      result_fm(?fa,?result),
      
      base(?param,?floor),
      min(?param,?baseMin),
      sma(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, modulo_fiscal),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      result_fm(?fa,?result),
      
      base(?param,?floor),
      sma(?param,?baseMin),
      medi(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, modulo_fiscal),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      result_fm(?fa,?result),
      
      base(?param,?floor),
      medi(?param,?baseMin),
      larg(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, modulo_fiscal),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      result_fm(?fa,?result),
      
      base(?param,?floor),
      larg(?param,?baseMin),
      excep(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, modulo_fiscal),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      result_fm(?fa,?result),
      
      top(?param,?t),
      
      has_factor(?param,?fac),
      greaterThan(?result,?t)
        -> has_factor_associated(?prod,?fac)"""
    },
    ################ FACTOR BASED ON AREA
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_da_propriedade),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      hectare(?fa,?result),

      base(?param,?floor),
      min(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_da_propriedade),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      hectare(?fa,?result),
      
      base(?param,?floor),
      min(?param,?baseMin),
      sma(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_da_propriedade),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      hectare(?fa,?result),
      
      base(?param,?floor),
      sma(?param,?baseMin),
      medi(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_da_propriedade),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      hectare(?fa,?result),
      
      base(?param,?floor),
      medi(?param,?baseMin),
      larg(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_da_propriedade),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      hectare(?fa,?result),
      
      base(?param,?floor),
      larg(?param,?baseMin),
      excep(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_da_propriedade),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      is_production_of(?prod,?fa),
      hectare(?fa,?result),
      
      top(?param,?t),
      
      has_factor(?param,?fac),
      greaterThan(?result,?t)
        -> has_factor_associated(?prod,?fac)"""
    },
    ################ FACTOR BASED ON N_DE_CABECAS
    {
      'name': 'Production measurement',
      'desc': """
      
      Parameter(?param),
      has_measurement(?param, n_de_cabecas),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?result),

      base(?param,?floor),
      min(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, n_de_cabecas),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?result),
      
      base(?param,?floor),
      min(?param,?baseMin),
      sma(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, n_de_cabecas),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?result),
      
      base(?param,?floor),
      sma(?param,?baseMin),
      medi(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, n_de_cabecas),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?result),
      
      base(?param,?floor),
      medi(?param,?baseMin),
      larg(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, n_de_cabecas),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?result),
      
      base(?param,?floor),
      larg(?param,?baseMin),
      excep(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, n_de_cabecas),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?result),
      
      top(?param,?t),
      
      has_factor(?param,?fac),
      greaterThan(?result,?t)
        -> has_factor_associated(?prod,?fac)"""
    },
    ################ FACTOR BASED ON N_DE_AREA
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_de_producao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_area(?prod,?result),

      base(?param,?floor),
      min(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_de_producao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_area(?prod,?result),
      
      base(?param,?floor),
      min(?param,?baseMin),
      sma(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_de_producao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_area(?prod,?result),

      base(?param,?floor),
      sma(?param,?baseMin),
      medi(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_de_producao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_area(?prod,?result),
      
      base(?param,?floor),
      medi(?param,?baseMin),
      larg(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_de_producao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_area(?prod,?result),

      base(?param,?floor),
      larg(?param,?baseMin),
      excep(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, area_de_producao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_area(?prod,?result),
      
      top(?param,?t),
      
      has_factor(?param,?fac),
      greaterThan(?result,?t)
        -> has_factor_associated(?prod,?fac)"""
    },
    ################ FACTOR BASED ON VACAS_EM_LACTACAO
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, vacas_em_lactacao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?fm),
      multiply(?result, 0.7, ?fm),

      base(?param,?floor),
      min(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, vacas_em_lactacao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?fm),
      multiply(?result, 0.7, ?fm),
      
      base(?param,?floor),
      min(?param,?baseMin),
      sma(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, vacas_em_lactacao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?fm),
      multiply(?result, 0.7, ?fm),
      
      base(?param,?floor),
      sma(?param,?baseMin),
      medi(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, vacas_em_lactacao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?fm),
      multiply(?result, 0.7, ?fm),
      
      base(?param,?floor),
      medi(?param,?baseMin),
      larg(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, vacas_em_lactacao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?fm),
      multiply(?result, 0.7, ?fm),
      
      base(?param,?floor),
      larg(?param,?baseMin),
      excep(?param,?baseMax),

      lessThanOrEqual(?result,?baseMax),
      greaterThan(?result,?baseMin),
      greaterThanOrEqual(?result,?floor),

      has_factor(?param,?factor)
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'Production measurement',
      'desc': """
      Parameter(?param),
      has_measurement(?param, vacas_em_lactacao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      num_animals(?prod,?fm),
      multiply(?result, 0.7, ?fm),
      
      top(?param,?t),
      
      has_factor(?param,?fac),
      greaterThan(?result,?t)
        -> has_factor_associated(?prod,?fac)"""
    },
    ### MEASUREMENT SEM_ESPECIFICACAO
    ### SIZE SEM_ESPECIFICACAO
    ### FACTOR ASSOCIATION
    {
      'name': 'FACTOR ASSOCIATION',
      'desc': """
      Parameter(?param),
      has_measurement(?param, sem_especificacao),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      has_factor(?param,?factor),
       -> has_factor_associated(?prod,?factor)"""
    },
    {
      'name': 'FACTOR ASSOCIATION',
      'desc': """
      Parameter(?param),
      is_parameter_associated_of(?param,?prod),
      Production(?prod),
      has_factor(?param,?factor),
      top(?param,?t),
      
       -> has_factor_associated(?prod,?factor)"""
    },
    ##########################
    ########################## Document recomendation
    ##########################
    {
      'name': 'Document Association',
      'desc': """
      Farm(?f),
      has_attribute(?f,?attrib),
      
      Document(?doc),
      has_attribute(?doc,?attrib),
      has_state_associated(?doc,any),
      has_activity(?doc,any),
      
      answer(?doc,?asw),
      equal(?asw,true)
      
       -> has_recommended_document(?f,?doc)"""
    },
    {
      'name': 'Document Association',
      'desc': """
      Farm(?f),
      has_missing_attribute(?f,?attrib),
      
      Document(?doc),
      has_attribute(?doc,?attrib),
      has_state_associated(?doc,any),
      has_activity(?doc,any),
      
      answer(?doc,?asw),
      equal(?asw,false)
      
       -> has_recommended_document(?f,?doc)"""
    },
    {
      'name': 'Document Association',
      'desc': """
      Farm(?f),
      has_state_associated(?f,?sta),
      has_missing_attribute(?f,?attrib),

      Document(?doc),
      has_attribute(?doc,?attrib),
      has_state_associated(?doc,?sta),
      
      answer(?doc,?asw),
      equal(?asw,false)
      
       -> has_recommended_document(?f,?doc)"""
    },
     {
       'name': 'Document Association',
       'desc': """
       Farm(?f),
       has_production(?f,?prod),
       has_missing_attribute(?f,?attrib),
       has_activity(?prod,?act),

       Document(?doc),
       has_attribute(?doc,?attrib),
       has_activity(?doc,?act),
       has_state_associated(?doc,any),
       
       answer(?doc,?asw),
       equal(?asw,false)
      
        -> has_recommended_document(?f,?doc)"""
    }
  ]

  for rule in rules:
    insert_rule = Imp()
    insert_rule.set_as_rule(rule['desc'])
