#!/usr/bin/env python

from tests import Tester
import logging
from optparse import OptionParser

if __name__ == '__main__':


  parser = OptionParser(usage='%prog [-d]',
                        description='pyject unit tests',
                        epilog='Sumit Khanna. GNU GPLv3 PenguinDreams.org')
  parser.add_option('-d','--debug',action='store_true',dest='debug',help='Display Debug Level Logging')
  (options, args) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel('DEBUG')
  
  Tester().run_tests()
