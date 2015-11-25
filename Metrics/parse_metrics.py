#!/usr/bin/python

"""
Parses xml based specification of metrics.

The xml file "metrics" contains the set of metrics user/administrator wants to monitor.

The program builds an index of json formatted specification of metrics.
The index is used to get the statistics from the sFlow-RT Engine using REST API.

Usage: parse.py [options] [source]

Options:
  -m ..., --metrics=...    user specified description file
  -h, --help               show this help
  -d                       show debugging information while parsing

Examples:
  parse_metrics.py                parses the defaul metrics file in the working directory
  parse_metrics.py -m metrics.xml parses the file passed as command line parameter e.g., metrics.xml

"""

__author__      = "Shafqat Rehman (shafqat.rehman@gmail.com)"
__version__     = "$Revision: 1.0 $"
__date__        = "$Date: 2013/10/18 13:00:00 $"
__copyright__   = "Copyright (c) 2013 Shafqat Rehman"
__license__     = "Python"



from xml.dom import minidom, Node

import sys
import os.path
import getopt
import traceback
import statistics
import xmlutils
import requests


_debug = 0

#class NoSourceError(Exception): pass

class MetricsParser:
    """generates metrics tasks based on a xml scenario definition file"""

    def __init__(self, metrics, source=None):
        """
          Constructor: Initialize class attributes
        """
        self.xml = metrics;
        self.host = "http://localhost:8008"
        self.rest_cmds = {}

    def _load(self, source):
        """
        load XML input source, return XML DOM (document object model) object
        """
        dom = minidom.parse(source).documentElement;
        return dom


    def parseMetrics(self):
        """Parse the metrics description file"""
        self.metrics_def = self._load(self.xml)
        """ get list of metrics defined under the root/document element"""
        # metrics = self.metrics_def.getElementsByTagName("metrics");
        metrics = self.metrics_def.childNodes
    	#print ("metrics %s" % (metrics))

        """ Prepare the REST command for all the metrics"""
        url =  "%s/" %(self.host)
        url +=  "metric/ALL/"
        for metric in metrics:
            if metric.nodeType == metric.TEXT_NODE and metric.nodeValue.strip() != "" :    # if this is a text node
                value  = metric.nodeValue.strip();
                url +=  "%s/" %(value)
	url += "json"
	print (url)
        # data for the GET HTTP method
        self.rest_cmds[url] = url
        pass


def error(error=""):
    """
    Display error message and call stack if the program encountered a problem during the execution 
    """
    if (len(str(error)) > 0):
            print ("ERROR: %s" % (error))
            print ("STACK TRACE:")
    traceback.print_exc()
    print (__doc__)


def usage(error=""):
    """
    Display usage information of parse_metrics.py 
    """
    print ("USAGE:")
    print ("%s -m metrics" % (sys.argv[0]))
    print ("OR: %s -h" % (sys.argv[0]))
    print ("OPTIONS:")
    print ("--metrics | -m        : name of the file containing the flow definitions")
    print ("--help  | -h        : print this information")

def extractOptions(argv):
      """
      Extract command line options and return a tuple
      @param argv the sys.argv object
      @return a tuple containing the information
      """
      try:
        opts, args = getopt.getopt(argv[1:], "h:m", ["help", "metrics="])
      except getopt.GetoptError:
        usage()
        sys.exit(2)
      for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-d':
            global _debug
            _debug = 1
        elif opt in ("-m", "--metrics"):
            metrics = args[0]

      return (metrics);

def main(argv):
    """
      Extract command line options.
      Parse metrics description XML file and build an the REST command.
    """
    metrics = "metrics.xml"
    try:
        """ Get command line options"""
        (metrics) = extractOptions(sys.argv)
        source = "".join(metrics)
        print (source)
        """load the metrics file in XML DOM"""
        fp = MetricsParser(metrics, source)
        """parse metrics desctiption"""
        fp.parseMetrics()
        """Get metrics values from sFlow-RT"""
        stats = statistics.Statistics(fp.rest_cmds)
        stats.sflowrt2graphite();
    except AssertionError as e:
        error(e)
    except Exception as e:
        error(e)

if __name__ == "__main__":
    main(sys.argv[1:])
