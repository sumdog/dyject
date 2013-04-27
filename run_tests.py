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


from tests import Tester
import logging
from optparse import OptionParser

if __name__ == '__main__':


  parser = OptionParser(usage='%prog [-d]',
                        description='pyject unit tests',
                        epilog='Sumit Khanna. Apache License 2.0. PenguinDreams.org')
  parser.add_option('-d','--debug',action='store_true',dest='debug',help='Display Debug Level Logging')
  (options, args) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel('DEBUG')
  
  Tester().run_tests()
