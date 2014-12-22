#!/usr/bin/env python

import urllib3
from parse import *
import time
import pickle
import os
import datetime
import atexit


def get_densities(source):
    places = [a.fixed[0] for a in findall("<li class=\"list-group-item\"><h4>{}</h4>", source)]
    percentages = [a.fixed[0] for a in findall("aria-valuenow=\"{}\"", source)]
    return dict([(places[i], percentages[i]) for i in range(len(places))])


def notify_exit(email):
    os.system("mutt -s \"rho_t exited unexpectedly\" %s < /dev/null" % email)


email = raw_input('Email to notify in case of problems: ')
atexit.register(notify_exit, email)
http = urllib3.PoolManager()

while True:
    r = http.request('GET', 'http://density.adicu.com/')
    if r.status == 200:
        densities = get_densities(r.data)
        print datetime.datetime.now()
        if os.path.isfile('history.p'):
            history = pickle.load(open('history.p', 'rb'))
        else:
            history = dict()
            for place in densities.keys():
                history[place] = []
        for place in densities.keys():
            if place not in history.keys():
                history[place] = []
            history[place].append((datetime.datetime.now(), densities[place]))
        pickle.dump(history, open('history.p', 'wb'))
        execfile('plot.py')
    else:
        os.system("mutt -s \"rho_t didn't get 200 OK\" %s < /dev/null" % email)

    time.sleep(15*60)
