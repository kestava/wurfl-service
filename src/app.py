
import cherrypy

class AppController(object):

    @cherrypy.expose
    def getUserAgentInfo(self, userAgentString):
    
        def tokenizer(devwindow=30):
            def _analyze(ua_str):
                return devices.select_ua(ua_str, search=Tokenizer(devwindow))
            return _analyze
            
        def two_step_analysis():
            def _analyze(ua_str):
                return devices.select_ua(ua_str, search=TwoStepAnalysis(devices))
            return _analyze
            
        cherrypy.log.error('\n\nUser Agent string: {0}'.format(userAgentString))
        cherrypy.response.headers['content-type'] = 'application/json'
        func = two_step_analysis()
        device = func(userAgentString)
        cherrypy.log.error('Device UA: {0}\nDevice Id: {1}'.format(device.devua, device.devid))
        
        o = {
            'device_ua': device.devua,
            'device_id': device.devid
        }
        
        for i in device:
            group = i[0]
            property = i[1]
            value = i[2]
            
            if group not in o:
                o[group] = {}
                
            o[group][property] = value
        
        print('Detected User Agent: {0}\nDetected Device Id: {1}'.format(device.devua, device.devid))
        #pprint(o)
        return json.dumps(o)
        

def main(config_file_path):
    cherrypy.quickstart(
        root=AppController(),
        config=config_file_path)

if __name__ == '__main__':
    import argparse
    import json
    from pprint import pprint
    
    from wurfl import devices
    from pywurfl.algorithms import TwoStepAnalysis, Tokenizer
    
    parser = argparse.ArgumentParser(description='A web service to deliver user agent information based on its user agent string')
    parser.add_argument('-c', '--config',
        dest='config_file', help='The full path to the configuration file.',
        required=True)
    args = parser.parse_args()
    main(args.config_file)