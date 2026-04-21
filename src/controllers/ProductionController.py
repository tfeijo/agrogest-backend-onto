from flask import jsonify
from owlready2 import World, OwlReadyError, sync_reasoner_pellet, destroy_entity

from src.models.Classes import production_to_json
from src.ontology.config import decrease_id, increase_id, onto
from src.utils.methods import Ontology, clear_string


class ProductionController:
  @staticmethod
  def store(productions):
    db = Ontology(f'./src/ontology/temp/{productions["farm_id"]}')
    db.load()

    try:
      new_list = []

      with db.onto:
        farm = db.onto.search_one(is_a=db.onto.Farm, id=productions['farm_id'])
        for production in productions['productions']:
          new_id = increase_id('Production')
          name = f'farm-{farm.id[0]}_{clear_string(production["activity"])}_{new_id}'

          new = db.onto.Production(
            name,
            id=[new_id],
            num_area=[float(production['num_area'])],
            has_activity=[db.onto.ProductionActivity(clear_string(production['activity']))],
            has_handling=[db.onto.ProductionHandling(clear_string(production['handling']))],
            has_state_associated=farm.has_state_associated,
          )
          farm.has_production.append(new)

          if 'cultivation' in production:
            new.is_agricultura = [True]
            new.num_animals = [0]
            new.has_cultivation = [db.onto.ProductionCultivation(clear_string(production['cultivation']))]
          else:
            new.num_animals = [int(production['num_animals'])]
            new.is_agricultura = [False]

          new_list.append(new)

        sync_reasoner_pellet(db.world, infer_property_values=True, infer_data_property_values=True)

        param = db.onto.Parameter('sem_especificacao')
        for item in new_list:
          if item.has_parameter_associated == []:
            item.has_parameter_associated = [param]
            item.has_size = [param]
            item.has_factor_associated = [param]

          if item.has_parameter_associated[0] != param and item.has_size == []:
            item.has_size = [param]

          if item.has_parameter_associated[0] != param and item.has_factor_associated == []:
            item.has_factor_associated = [param]
      db.save()

    except OwlReadyError as e:
      decrease_id('Production')
      return jsonify({'error': 'Something went wrong in inserting', 'msg': str(e)}), 400

    try:
      query_prod = db.onto.search(is_a=db.onto.Production, is_production_of=farm)
      result = [production_to_json(prod) for prod in query_prod]
      return jsonify(result), 200
    except OwlReadyError as e:
      return jsonify({'error': 'Inserted but not queried', 'msg': str(e)}), 400
    finally:
      db.save()
      db.close()

  @staticmethod
  def index():
    productions = [production.to_json() for production in onto.Production.instances()]
    return jsonify(productions)

  @staticmethod
  def delete(farm_id, id):
    world = World(filename=f'./src/ontology/temp/{farm_id}.sqlite3', exclusive=False)
    local_onto = world.get_ontology(f'./src/ontology/temp/{farm_id}.owl').load()

    try:
      with local_onto:
        query_prod = local_onto.search_one(is_a=local_onto.Production, id=id)
        if query_prod is None:
          return jsonify({'error': 'Production not found'}), 404
        destroy_entity(query_prod)

      world.save(file=f'./src/ontology/temp/{farm_id}.owl')
      return jsonify({'msg': 'Successfull'}), 200

    except OwlReadyError as e:
      return jsonify({'error': 'Something went wrong in deleting', 'msg': str(e)}), 400
    finally:
      local_onto.destroy()
      world.close()
