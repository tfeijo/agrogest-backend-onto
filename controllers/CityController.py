from flask import jsonify
from models.City import City
from dao.CityDAO import CityDAO

class CityController:


  def index():
    city1 = City('Cidade1')
    city2 = City('Cidade2')
    cities= [city1.toJSON(),city2.toJSON()]

    return jsonify(cities)
