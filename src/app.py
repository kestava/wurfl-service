
import argparse
import json

import cherrypy

from wurfl import devices
from pywurfl.algorithms import TwoStepAnalysis

class AppController(object):

    @cherrypy.expose
    def getUserAgentInfo(self, userAgentString):
        cherrypy.response.headers['content-type'] = 'application/json'
        algo = TwoStepAnalysis(devices)
        device = devices.select_ua(userAgentString, search=algo)
        #s = json.dumps(device)
        #print(s)
        #o = [i for i in device]
        #print(o)
        #s = json.dumps(o)
        #print(s)
        #return s
        #return 'blah'
        
        o = {}
        
        for i in device:
            group = i[0]
            property = i[1]
            value = i[2]
            
            if group not in o:
                o[group] = {}
                
            o[group][property] = value
        
        return json.dumps(o)
        

def main(config_file_path):
    cherrypy.quickstart(
        root=AppController(),
        config=config_file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A web service to deliver user agent information based on its user agent string')
    parser.add_argument('-c', '--config',
        dest='config_file', help='The full path to the configuration file.',
        required=True)
    args = parser.parse_args()
    main(args.config_file)