'''
Created on Jun 29, 2011

@author: Sumit Khanna <sumit@penguindreams.org>
'''
#!/usr/bin/env python

import sys
from dyject import Context
import tests
 
class Tester:         

  #Display Color Codes
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAILRED = '\033[91m'
  ENDC = '\033[0m'
  
  

  def write_test_results(self,title,tuples):
    print("  " + self.HEADER + title + self.ENDC)
    for (status,message) in tuples:
      if status == True:
        resp = self.OKBLUE + '[' + self.OKGREEN + '  ok  ' + self.OKBLUE + ']' + self.ENDC
      elif status == False:
        resp = self.OKBLUE + '[' + self.FAILRED  + ' fail ' + self.OKBLUE + ']' + self.ENDC
      else:
        resp = self.OKBLUE + '[' + self.WARNING  + '  !!  ' + self.OKBLUE + ']' + self.ENDC
        
      print('   ' + message.ljust(85) + resp)
      sys.stdout.flush()

              

  def run_tests(self):

    results = []
    
    ctx = Context()
    ctx.load_config('tests/tests.config')
    
    status = []

    types = ctx.get_class('Types')
    
    status.append((type(types.integer) is int , 'Checking for Integer Type'))
    status.append((type(types.string) is str , 'Checking for String Type'))
    status.append((type(types.dict) is dict , 'Checking for Dict Type'))
    status.append((type(types.list) is list , 'Checking for List Type'))
    status.append((type(types.float) is float , 'Checking for Float Type'))
    status.append((type(types.int_string) is str , 'Checking for Int as String'))
    status.append((type(types.tuple) is tuple , 'Checking for Tuple'))
    status.append((type(types.complex) is complex , 'Checking for Complex'))
    

    self.write_test_results('Typing Tests',status)
    
    status = []

    subclass = ctx.get_class('TypesPartTwo')

    status.append((subclass.integer == 5,'Checking for override Int 5'))
    status.append((subclass.string == "Something Else", 'Checking for override String'))
    status.append((subclass.float == 2.0, 'Check for Parent Float 2.0'))

    self.write_test_results('Inheritance Tests',status)

    status = []
    
    subtype = ctx.get_class('TypesPartTwoWithZombies')
    
    status.append((subtype.check_shadow_vars() , 'Ensure Variables are not Shadowed'))
    
    status.append((isinstance(subtype,tests.examples.TypeInstance), 'Class is Instance of Parent' ))
    status.append((isinstance(subtype,tests.examples.SubTypeInstance), 'Class is Instance of Child' ))
    status.append((not isinstance(subtype,tests.examples.FooInstance), 'Class is not Instance of Another Defined Class' ))
    status.append((isinstance(subtype.foo,tests.examples.FooInstance),'FooInstance Dependency Injection Test'))
    status.append(( type(subtype.bar) is list and 
                    len(subtype.bar) is 2 and
                    isinstance(subtype.bar[0],tests.examples.FooInstance) and
                    isinstance(subtype.bar[1],tests.examples.TypeInstance) ,
                    'List of Objects Dependency Injection Test' ))
    

    self.write_test_results('Class References Tests',status)

    status = []

    status.append(( id(subtype.foo) == id(ctx.get_class('Foos'))  , 'Singleton Injection of Class Foo'))
    status.append(( id(subtype.bar[0]) == id(subtype.foo)  , 'Singleton Injection in List'))
    status.append(( id(subtype.foo) != id(ctx.get_class('Foos',prototype=True)), 'Compare Prototype to Injected Class Test'))

    #must be assigned to vars or else the Python2 garbage collecor will be so greedy
    # that this test will fail
    foo_a = ctx.get_class('Foos',prototype=True)
    foo_b = ctx.get_class('Foos',prototype=True)

    status.append(( id(foo_a) != id(foo_b)  , 'Create Two Prototypes'))

    #This test will pass in Python3 and fail in Python2
    #status.append(( id(ctx.get_class('Foos',prototype=True)) != id(ctx.get_class('Foos',prototype=True))  , 'Create Two Prototypes'))

    self.write_test_results('Prototypes (non-singleton) Tests',status)

    
    status = []
    
    ssclass = ctx.get_class('TypesPartThreeTheReckoning')
    
    status.append(( ssclass.topvar == 'top' , 'Class Variable Test' ))
    status.append(( ssclass.float == 5.0 , 'Parent Variable Test' ))
    status.append(( ssclass.int_string == '4' , 'Grandparent Variable Test' ))
    status.append(( isinstance(ssclass,tests.examples.SubSubInstance) , 'Class Instance Test' ))
    status.append(( isinstance(ssclass,tests.examples.SubTypeInstance) , 'Parent Class Instance Test' ))
    status.append(( isinstance(ssclass,tests.examples.TypeInstance) , 'Grandparent Class Instance Test' ))

    status.append(( type(ssclass.bar) is list and 
                    len(ssclass.bar) is 2 and
                    isinstance(ssclass.bar[0],tests.examples.FooInstance) and
                    isinstance(ssclass.bar[1],tests.examples.TypeInstance) ,
                    'List of Objects in Parent Dependency Injection Test' ))


    self.write_test_results('Third Subclass Tests',status)


