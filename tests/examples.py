
class TypeInstance(object):

  def __init__(self):
    object.__init__(self)
    self.integer = None
    self.string = None
    self.dict = None
    self.list = None

  def get_base_float(self):
    return self.float

class SubTypeInstance(TypeInstance):

  def __init__(self):
    TypeInstance.__init__(self)

  def check_shadow_vars(self):
    return self.float == super(SubTypeInstance,self).get_base_float()


class FooInstance(object):

  def __init__(self):
    object.__init__(self)


class BarInstance(FooInstance):

  def __init__(self):
    object.__init__(self)
