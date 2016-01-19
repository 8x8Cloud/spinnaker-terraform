#!/usr/bin/env python

import sys
import pprint
import os
import time

try:
    import requests
except ImportError, e:
    print "Missing requests module.  Install with: sudo pip install requests"
    print "If you don't have pip, do this first: sudo easy_install pip"
    exit(2)

#r_lb = requests.get(lb_url + "/healthcheck", timeout=request_timeout)
def main(argv):
    pp = pprint.PrettyPrinter(indent=4)

    num_tries = 20
    request_timeout = 10.0

    lb_found = False

    app_name = 'kenzanapp' #Hardcoded for now, shouldn't be a problem to hardocde it as long as scripts create the applicaiton, lb, etc.
    lb_name = 'kenzanapp-jpstack' #same as above, should be OK to hardcode

    spinnaker_lb_url = 'http://localhost:8084/applications/' + app_name + '/loadBalancers'

    r_find_lb = requests.get(spinnaker_lb_url, timeout=request_timeout)

    lbs = r_find_lb.json()

    for lb in lbs:
        if lb['name'] == lb_name:
            lb_ip = lb['ipAddress']
            lb_found = True



    if lb_found:
        lb_url = 'http://' + lb_ip

        print "Attempting to determine health of: " + lb_url + ". NOTE: This could take awhile."
        successful_load = False
        current_try = 1

        while not successful_load and current_try < num_tries:
            print "Try #" + str(current_try)
            current_try += 1
            r_lb = requests.get(lb_url + ":7070/healthcheck", timeout=request_timeout)
            if r_lb.status_code == requests.codes.ok:
                successful_load = True
                print "\tSUCCESS!"

            else:
                print "\tWaiting another " + str(request_timeout) + " seconds..."
                time.sleep(request_timeout)

        if successful_load:
            print "\n\nGo to the following URL in your brower to see the example app you just deployed:"
            print "\t" + lb_url + "/hello"
        else:
            print lb_url + " is not healthy. It does take some time for the instance to show up as healthy in the LB, you might want to try again in a few minutes."

    else:
        print "NO LB could be found for the test application."


if __name__ == "__main__":
    main(sys.argv)
