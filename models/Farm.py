from dao.FarmDAO import FarmDAO

class Farm:
  def __init__(self, hectare, city_id, licensing, id=None, installation_id=None):
    self.id = id
    self.hectare = hectare
    self.city_id = city_id
    self.licensing = licensing
    self.installation_id = installation_id
    calculo_size_id = 123123
    self.size_id = calculo_size_id

  def toJSON(self):
    return {
      "id": self.id,
      "installation_id": self.installation_id,
      "hectare": self.hectare,
      "city_id": self.city_id,
      "licensing": self.licensing,
      "size_id": self.size_id,
    }