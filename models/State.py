from dao.StateDAO import StateDAO

class State:
  def __init__(self, name, id=None):
    self.id = id
    self.name = name
  
  def toJSON(self):
    return {
      'id': self.id,
      'name': self.name
    }