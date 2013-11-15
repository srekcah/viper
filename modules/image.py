import os
import json
import urllib
import urllib2

try:
    import requests
    HAVE_REQUESTS = True
except ImportError:
    HAVE_REQUESTS = False

from viper.common.out import *
from viper.common.abstracts import Module
from viper.core.session import __session__

class Image(Module):
    cmd = 'image'
    description = 'Perform analysis on images'

    def ghiro(self):
        payload = dict(private='true', json='true')
        files = dict(image=open(__session__.file.path, 'rb'))

        response = requests.post('http://www.imageforensic.org/api/submit/', data=payload, files=files)
        results = response.json()

        if results['success']:
            report = results['report']

            if len(report['signatures']) > 0:
                print(bold("Signatures:"))

                for signature in report['signatures']:
                    print_info(signature['description'])
        else:
            print_error("The analysis failed")

    def usage(self):
        print("usage: image <command>")

    def help(self):
        self.usage()
        print("")
        print("Options:")
        print("\tghiro\t\tUpload the file to imageforensic.org and retrieve report")
        print("")

    def run(self):
        if not __session__.is_set():
            print_error("No session opened")
            return

        if not HAVE_REQUESTS:
            print_error("Missing dependency, install requests (`pip install requests`)")
            return

        if len(self.args) == 0:
            self.help()
            return

        if self.args[0] == 'ghiro':
            self.ghiro()
