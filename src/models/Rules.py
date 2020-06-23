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
      'name': 'result_fm < 4 -> Size = Small',
      'desc': """
                result_fm(?f, ?r),
                lessThan(?r, 4.0)
                  -> has_size(?f, Small)
              """
    },{
      'name': 'result_fm == 4 -> Size = Small',
      'desc': """
                result_fm(?f, ?r),
                equal(?r, 4.0)
                  -> has_size(?f, Small)
              """
    },{
      'name': 'result_fm > 4 || < 15 -> Size = Medium',
      'desc': """
                result_fm(?f, ?r),
                greaterThan(?r, 4.0), lessThan(?r, 15.0)
                  -> has_size(?f, Medium)
              """
    },{ 
      'name': 'result_fm == 15 -> Size = Medium',
      'desc': """
                result_fm(?f, ?r),
                equal(?r, 15.0)
                  -> has_size(?f, Medium)"""
    },{
      'name': 'result_fm == 15 -> Size = Medium',
      'desc': """
                result_fm(?f, ?r),
                greaterThan(?r, 15.0)
                  -> has_size(?f, Large)"""
    }
  ]

  for rule in rules:
    insert_rule = Imp()
    insert_rule.set_as_rule(rule['desc'])
