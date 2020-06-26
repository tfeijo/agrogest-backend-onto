from owlready2 import *
from src.ontology.config import onto
from src.models.Classes import *

with onto:
  class has_state(ObjectProperty):
    domain = [City]
    range = [State]
    python_name = 'state'

  class is_state_of(ObjectProperty):
    domain = [State]
    range = [City]
    inverse_property = has_state

  class has_city(ObjectProperty):
    domain = [Farm]
    range = [City]
    python_name = 'city'

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
    python_name = 'biome'
 
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
    # domain = [Farm, Factor, Production]
    range = [Size]
    python_name = 'size'

  class is_size_of(ObjectProperty):
    domain = [Size]
    # range = [Farm, Factor,Production]
    inverse_property = has_size
  
  class has_activity(ObjectProperty):
    # domain = [Farm, Parameter, Production]
    range = [ProductionActivity]

  class is_activity_of(ObjectProperty):
    domain = [ProductionActivity]
    # range = [Farm, Parameter, Production]
    inverse_property = has_activity
  
  class has_measurement(ObjectProperty):
    domain = [Parameter]
    range = [Measurement]

  class is_measurement_of(ObjectProperty):
    domain = [Measurement]
    range = [Parameter]
    inverse_property = has_measurement
  
  class has_factor(ObjectProperty):
    domain = [Parameter]
    range = [Factor]

  class is_factor_of(ObjectProperty):
    domain = [Factor]
    range = [Parameter]
    inverse_property = has_factor
  
  class has_production(ObjectProperty):
    domain = [Farm]
    range = [Production]

  class is_production_of(ObjectProperty):
    domain = [Production]
    range = [Farm]
    inverse_property = has_production
  
  class has_production_system(ObjectProperty):
    domain = [ProductionActivity]
    range = [ProductionSystem]

  class is_production_system_of(ObjectProperty):
    domain = [ProductionSystem]
    range = [ProductionActivity]
    inverse_property = has_production_system
  
  class has_production_handling(ObjectProperty):
    domain = [ProductionSystem]
    range = [ProductionHandling]

  class is_production_handling_of(ObjectProperty):
    domain = [ProductionHandling]
    range = [ProductionSystem]
    inverse_property = has_production_handling

  class is_created_by(ObjectProperty):
    domain = [Farm]
    range = [Device]
    python_name = 'device'

  class has_farm_created(ObjectProperty):
    domain = [Device]
    range = [Farm]
    inverse_property = is_created_by
  
  class has_biome_associated(ObjectProperty):
    pass
  class has_state_associated(ObjectProperty):
    pass

  
  AllDisjoint([City, Farm, State, Biome, Size])