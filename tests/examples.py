"""
Copyright [2013] [dyject.com]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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


class SubSubInstance(SubTypeInstance):

  def __init__(self):
    object.__init__(self)
