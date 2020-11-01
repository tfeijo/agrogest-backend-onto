from owlready2 import *
from src.ontology.config import onto
from src.models.Classes import *

with onto:
  class has_state(ObjectProperty):
    domain = [City]
    range = [State]
    python_name = 'has_state'

  class is_state_of(ObjectProperty):
    domain = [State]
    range = [City]
    inverse_property = has_state

  class has_city(ObjectProperty):
    domain = [Farm]
    range = [City]
    python_name = 'has_city'

  class is_city_of(ObjectProperty):
    domain = [City]
    range = [Farm]
    inverse_property = has_city

  class has_parameter(ObjectProperty):
    domain = [State]
    range = [Parameter]

  class is_parameter_of(ObjectProperty):
    domain = [Parameter]
    range = [State]
    inverse_property = has_parameter

  class has_biome(ObjectProperty):
    domain = [City]
    range = [Biome]
    python_name = 'has_biome'
 
  class is_biome_of(ObjectProperty):
    domain = [Biome]
    range = [City]
    inverse_property = has_biome
    python_name = 'is_biome_of'
  
  class has_farm(ObjectProperty):
    domain = [City]
    range = [Farm]

  class is_farm_of(ObjectProperty):
    domain = [Farm]
    range = [City]
    inverse_property = has_farm
  
  class has_size(ObjectProperty):
    range = [Size]
    python_name = 'has_size'

  class is_size_of(ObjectProperty):
    domain = [Size]
    inverse_property = has_size
  
  class has_activity(ObjectProperty): pass

  class is_activity_of(ObjectProperty):
    inverse_property = has_activity
  
  class has_measurement(ObjectProperty): pass

  class is_measurement_of(ObjectProperty):
    inverse_property = has_measurement
  
  class has_factor(ObjectProperty): pass

  class is_factor_of(ObjectProperty):
    inverse_property = has_factor
  

  class is_production_of(ObjectProperty): pass
  
  class has_production(ObjectProperty): 
    inverse_property = is_production_of
   
  class has_handling(ObjectProperty):
    python_name = 'has_handling'

  class is_handling_of(ObjectProperty):
    inverse_property = has_handling

  class is_created_by(ObjectProperty):
    domain = [Farm]
    range = [Device]
    python_name = 'is_created_by'

  class has_farm_created(ObjectProperty):
    domain = [Device]
    range = [Farm]
    inverse_property = is_created_by
  
  class has_cultivation(ObjectProperty):
    pass
    
  class is_cultivation_of(ObjectProperty):
    inverse_property = has_cultivation

  class has_biome_associated(ObjectProperty):
    pass
  class is_biome_associated_of(ObjectProperty):
    inverse_property = has_biome_associated

  class has_state_associated(ObjectProperty):
    pass
  class is_state_associated_of(ObjectProperty):
    inverse_property = has_state_associated

  class has_document_associated(ObjectProperty):
    pass
  class is_document_associated_of(ObjectProperty):
    inverse_property = has_document_associated

  class has_production_associated(ObjectProperty):
    pass
  class is_production_associated_of(ObjectProperty):
    inverse_property = has_production_associated
  
  class has_parameter_associated(ObjectProperty): pass
  
  class is_parameter_associated_of(ObjectProperty):
    inverse_property = has_parameter_associated

  class has_factor_associated(ObjectProperty):
    pass
  class is_factor_associated_of(ObjectProperty):
    inverse_property = has_factor_associated

  class has_attended_document(ObjectProperty):
    pass
  class is_attended_document_by (ObjectProperty):
    inverse_property = has_attended_document

  class has_attribute(ObjectProperty):
    pass
  class is_attribute_of(ObjectProperty):
    inverse_property = has_attribute

  class has_recommended_document(ObjectProperty):
    pass
  class is_document_recommended_of(ObjectProperty):
    inverse_property = has_recommended_document

  class has_question(ObjectProperty):
    pass
  class is_question_of(ObjectProperty):
    inverse_property = has_question

  class has_category(ObjectProperty):
    pass
  class is_category_of(ObjectProperty):
    inverse_property = has_category

  class has_missing_attribute(ObjectProperty):
    pass
  class is_missing_attribute_of(ObjectProperty):
    inverse_property = has_missing_attribute
  
  AllDisjoint([City, Farm, State, Biome, Size])