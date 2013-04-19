#!/usr/bin/env python
import logging
import sys
import ast


def ispy3():
  """
  returns true if running in Python 3
  http://stackoverflow.com/questions/11372190/python-2-and-python-3-dual-development    
  """
  return sys.version_info >= (3,)



class context:


  def __init__(self):
    
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

  def set_args(self,object,key,value):
    arg = None
    if '\\' in value:
      (optype,opt) = value.split('\\')
      if optype == 'class-ref':
        if opt.startswith('{'):
          arg = []
          for c in opt.strip('{}').split(','):
            arg.append(__get_obj(c))
        else:            
          arg = self.__get_obj(opt)          
    else:
      arg = type(ast.literal_eval(value)) #value
    
    logging.debug('Setting attribute {0} to {1} for class {2}'.format(key,arg,object))
    setattr(object,key,arg)
      

  def __get_class_name(self,bean): 
    if not self.config.has_option(bean, 'inherit'):
      return self.config.get(bean,'class')
    if self.config.has_option(bean, 'class'):
      return self.config.get(bean,'class')
    return self.__get_class_name(self.config.get(bean,'inherit'))
    
        
  def get_class(self,idu,prototype=False):
    if idu in self.loader_classes:
      logging.debug('Loading Cached Object ' + idu)
      return self.loader_classes[idu]

    bean = self.config.items(idu)   
    name = self.__get_class_name(idu)
  
    obj = self.__get_obj(name)
    logging.debug('Created Object {0} of type {1}'.format(idu,name))
  
    #inherited 
    #  to do this correctly we really want to roll up
    #  and not down. This works for now. 
    cur = idu
    while(self.config.has_option(cur,'inherit')):
      cur = self.config.get(cur,'inherit')
      for (skey,svalue) in self.config.items(cur):
        if skey != 'class' and skey != 'inherit':
          self.set_args(obj,skey,svalue)        
  
    for (key,value) in bean:
      if key == 'class' or key == 'inherit':
        continue
      else:
        self.set_args(obj,key,value)

    if prototype == False:
      logging.debug("Caching Singleton object {0}".format(idu))
      self.loader_classes[idu] = obj
    else:
      logging.debug("Prototype request. Returning new instance {0}".format(idu))

    return obj
