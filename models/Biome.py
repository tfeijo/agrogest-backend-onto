from dao.BiomeDAO import BiomeDAO

class Biome:
  def __init__(self, name, id=None):
    self.id = id
    self.name = name

  def toJSON(self):
    return {
      'id': self.id,
      'name': self.name
    }