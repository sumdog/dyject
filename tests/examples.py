
class TypeInstance(object):

  def __init__(self):
    self.integer = None
    self.string = None
    self.dict = None
    self.list = None

class FooInstance(object):

  def __init__(self):
    pass

class BarInstance(FooInstance):

  def __init__(self):
    pass
