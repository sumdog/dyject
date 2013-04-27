#!/usr/bin/env python
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


import logging
import sys
import ast


def ispy3():
  """
  returns true if running in Python 3
  http://stackoverflow.com/questions/11372190/python-2-and-python-3-dual-development    
  """
  return sys.version_info >= (3,)



class Context:


  def __init__(self):
    """Loads Python2/Python3 compatability, configuration parser
       and removes case sensitivity from configuration reader"""
    if ispy3():
      import configparser
      self.config = configparser.RawConfigParser()
    else:
      import ConfigParser
      self.config = ConfigParser.RawConfigParser()

    #remove case insensitivity 
    self.config.optionxform = lambda option: option

    #Object Cache
    self.loader_classes = {}



  def __get_obj(self,name):
    """
    Dynmically loads Python class given fully qualified namespace
    http://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
    """
    components = name.split('.')
    path = '.'.join(components[:-1])
    clss = components[-1:][0]
    mod = __import__(path,globals(),locals(),clss)
    return getattr(mod,clss)()

  def load_config(self,files):
    """configuration files to load. Can be either a single file or list of files"""
    if (ispy3() and isinstance(files, str)) or isinstance(files, basestring):
      files = [ files ]
    self.config.read( files )

  def __set_args(self,object,key,value):
    arg = None
    if '\\' in value:
      (optype,opt) = value.split('\\')
      if optype == 'class-ref':
        if opt.startswith('{'):
          arg = []
          for c in opt.strip('{}').split(','):
            arg.append(self.get_class(c))
        else:  
          arg = self.get_class(opt)          
    else:
      arg = ast.literal_eval(value) #value
    
    logging.debug('Setting attribute {0} to {1} for class {2}'.format(key,arg,object))
    setattr(object,key,arg)
      

  def __get_class_name(self,bean): 
    if not self.config.has_option(bean, 'inherit'):
      return self.config.get(bean,'class')
    if self.config.has_option(bean, 'class'):
      return self.config.get(bean,'class')
    return self.__get_class_name(self.config.get(bean,'inherit'))
    
        
  def get_class(self,idu,prototype=False):
    if idu in self.loader_classes and not prototype:
      logging.debug('Loading Cached Object ' + idu)
      return self.loader_classes[idu]

    bean = self.config.items(idu)   
    name = self.__get_class_name(idu)
  
    obj = self.__get_obj(name)
    logging.debug('Created Object {0} of type {1}'.format(idu,name))
  

    #inheritence - we want to set attributes from the bottom to the top
    #  so we start with a top down list of all attribute tuples

    cur = idu
    tree = []
    while(self.config.has_option(cur,'inherit')):
      cur = self.config.get(cur,'inherit')
      tree.append(self.config.items(cur))

    #reverse that list an apply them in bottom up order

    tree.reverse()
    for item in tree:
      for (skey,svalue) in item:
        if skey != 'class' and skey != 'inherit':
          self.__set_args(obj,skey,svalue)

    
    for (key,value) in bean:
      if key == 'class' or key == 'inherit':
        continue
      else:
        self.__set_args(obj,key,value)

    if prototype == False:
      logging.debug("Caching Singleton object {0}".format(idu))
      self.loader_classes[idu] = obj
    else:
      logging.debug("Prototype request. Returning new instance {0}".format(idu))

    return obj

