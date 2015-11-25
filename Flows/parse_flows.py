#!/usr/bin/python

"""
Parses xml based description of flows and generates json formatted flow definitions.

The xml file "flows.xml" defines all the user traffic flows.

The program builds an index of json formatted flow definitions.
The index is used to push the flow definitions to the sFlow-RT Engine using REST API.

Usage: parse_flows.py [options] [source]

Options:
  -f ..., --flows=...   user specified description file or URL
  -h, --help            show this help
  -d                    show debugging information while parsing

Examples:
  Parser_flows.py                       generates flows for defaul flow definition file in the working folder
  Parser.py -f flows.xml generates JSON flow definitions for XML-based flow definitions in flows.xml

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
import submit
import xmlutils
import requests


_debug = 0

# class NoSourceError(Exception): pass

class FlowParser:
    """generates flows tasks based on a xml scenario definition file"""

    def __init__(self, flows, source=None):
        """
        Constructor: Initialize class attributes
        """
        self.xml = flows;
        self.host = "http://localhost:8008"
        self.rest_cmds = {}


    def _load(self, source):
        """
        load XML input source, return parsed XML in DOM (Document Object Model) object
        """
        dom = minidom.parse(source).documentElement;
        return dom


    def parseFlows(self):
        """
        Parse the xml file containing flow definitions.
        Create flow definitons in JSON format.
        Create REST commands for flow definitions and store them in an index 'rest_cmds'. The index is used by 'submit' class to load flow definitions in sFlow-RT engine.  
        """
        self.flows_def = self._load(self.xml)
        # get list of flows defined under the root/document element
        flows = self.flows_def.getElementsByTagName("flow");
        for flow in flows:
            name   = flow.getAttribute("name");
            keys   = flow.getAttribute("keys");
            value  = flow.getAttribute("value");
            filtr  = flow.getAttribute("filter");
            # Prepare the REST API for this flow definition
            url =  "%s/" %(self.host)
            url +=  "flow/%s/json" %(name)
            # data for the PUT HTTP method
            if (len(str(filtr)) > 0):
                data = "{'keys':'%s','value':'%s','filter':'%s'}" %(keys, value, filtr)
            else:
                data = "{'keys':'%s','value':'%s'}" %(keys, value)
            self.rest_cmds[url] = data
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
    Display usage information of parse_flows.py 
    """
    print ("USAGE:")
    print ("%s -f flows" % (sys.argv[0]))
    print ("OR: %s -h" % (sys.argv[0]))
    print ("OPTIONS:")
    print ("--flows | -f        : name of the file containing the flow definitions")
    print ("--help  | -h        : print this information")

def extractOptions(argv):
      """
      Extract command line options and return a tuple
      @param argv the sys.argv object
      @return a tuple containing the command line information
      """
      try:
        opts, args = getopt.getopt(argv[1:], "h:f", ["help", "flows="])
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
        elif opt in ("-f", "--flows"):
            flows = args[0]

      return (flows);



def main(argv):

    """
      Extract command line options.
      Parse flow definition XML file and build an index of REST commands.
      Traverse the index and send each flow definition to sFlow-RT 
    """

    flows = "flows.xml"
    try:
        (flows) = extractOptions(sys.argv)
        source = "".join(flows)
        print (source)
        fp = FlowParser(flows, source)
        # parse xml specifications
        fp.parseFlows()
        # Push flow definitions to sFlow-RT analytics engine
        sub = submit.Submit(fp.rest_cmds)
        sub.submit();
    except AssertionError as e:
        error(e)
    except Exception as e:
        error(e)

if __name__ == "__main__":
    main(sys.argv[1:])
