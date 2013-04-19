'''
Created on Jun 29, 2011

@author: Sumit Khanna <sumit@penguindreams.org>
'''
#!/usr/bin/env python

import sys
from dyject import context
 
class Tester:         

  #Display Color Codes
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAILRED = '\033[91m'
  ENDC = '\033[0m'
  
  #output levels
  LEVEL_ERROR = 10
  LEVEL_WARN  = 20
  LEVEL_INFO  = 30
  LEVEL_DEBUG = 40
  LEVEL_TRACE = 50
  

  def write_test_results(self,title,tuples):
    print("  " + self.HEADER + title + self.ENDC)
    for (status,message) in tuples:
      if status == True:
        resp = self.OKBLUE + '[' + self.OKGREEN + '  ok  ' + self.OKBLUE + ']' + self.ENDC
      elif status == False:
        resp = self.OKBLUE + '[' + self.FAILRED  + ' fail ' + self.OKBLUE + ']' + self.ENDC
      elif status == Tester.TRACE and not self.trace:
        continue
      else:
        resp = self.OKBLUE + '[' + self.WARNING  + '  !!  ' + self.OKBLUE + ']' + self.ENDC
        
      print('   ' + message.ljust(85) + resp)
      sys.stdout.flush()

              

  def run_tests(self):
    results = []
    
    ctx = context()
    ctx.load_config('tests/tests.config')
    
    status = []

    types = ctx.get_class('Types')
    
    status.append((types.integer is int , 'Checking for Integer Type'))
    status.append((types.string is str , 'Checking for String Type'))
    status.append((types.dict is dict , 'Checking for Dict Type'))
    status.append((types.list is list , 'Checking for List Type'))
    status.append((types.float is float , 'Checking for Float Type'))
    

    self.write_test_results('Typing Tests',status)
    
    
  
    
