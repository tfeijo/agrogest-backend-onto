class City:
  
  
  def __init__(self, name):
      self.name = name
  

  def toJSON(self):
    return {
      'name': self.name
    }