#!/usr/bin/python
"""
   Submit class is invoked by parse_flows to send flow definitions to sFlow-RT.
   The class receives the index containing REST commands.
   It then traverses the index and makes the REST calls using 'requests' python package.

__author__      = "Shafqat Rehman (shafqat.rehman@gmail.com)"
__version__     = "$Revision: 1.0 $"
__date__        = "$Date: 2013/10/18 155555:00:00 $"
__copyright__   = "Copyright (c) 2013 Shafqat Rehman"
__license__     = "Python"

"""

import sys
import os
import os.path
import subprocess
import getopt
import traceback
import requests


class Submit:
    '''
    classdocs
    '''

    def __init__(self, cmds):
        '''
        Constructor
        '''
        self.flows = {}
        self.flows  = cmds;


    def submit(self):
        """
        Send the flow definitions to sFlow-RT.
        Print the status of each REST call. Status code of 200 means REST command was successful.
        """
        for k, v in self.flows.items():
	    print ("%s, %s" %(k,v))
            #r = requests.put(k, v, headers={"content-type":"application/json"})
            r = requests.put(k, data="%s" %(v))
	    print (r.status_code)
        pass
