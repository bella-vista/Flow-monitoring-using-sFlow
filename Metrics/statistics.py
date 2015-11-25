#!/usr/bin/python

#!/usr/bin/python
"""
   Statistics class is invoked by parse_metrics to periodically get metrics values from sFlow-RT. The class receives the REST command from parse_metrics.py as a parameter. It then makes the periodic REST calls using 'requests' python package.

__author__      = "Shafqat Rehman (shafqat.rehman@gmail.com)"
__version__     = "$Revision: 1.0 $"
__date__        = "$Date: 2013/10/18 14:00:00 $"
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
import json
import time
import socket


class Statistics:
    '''
    classdocs
    '''

    def __init__(self, cmds):
        '''
        Constructor
        '''
        self.flows = {}
        self.flows  = cmds;



    # precondition: sflow-rt must be running
    def sflowrt2graphite(self):
        """
         Calls GET REST command every 30 seconds to get summary statistics for all the metrics defined in the metrics description file.
        """
	# precondition: graphite must be running
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1",2003))

	for k, cmd in self.flows.items():
            print ("%s, %s" %(k,cmd))
	#v = self.flows.items()
	while 1 == 1:
	    print (cmd)
  	    r = requests.get(cmd)
  	    if r.status_code != 200: break
  	    vals = r.json()
  	    if len(vals) == 0: continue
	    print (vals)
            mtime=int(round(time.time()))
	    print ("metric time = %s" %(mtime))
  	    for v in vals:
    		mname  = v["metricName"]
    		if "metricValue" not in v: continue
		mvalue = v["metricValue"]
		#if "lastUpdate" in v: key = "lastUpdate"
		#else: key = "lastUpdateMin"
    		#mtime  = v[key] / 1000
    		message = "OFTEIN.%s %f %i\n" % (mname,mvalue,mtime)
    		print message
    		sock.sendall(message)
    	    time.sleep(30)

	pass
