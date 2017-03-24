#!/usr/bin/env python
import logging

import os
from google.appengine.ext import vendor
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))

from flask import Flask, request
import facebook
import requests
import datetime


app = Flask(__name__)


@app.route('/cron', methods=['GET', 'POST'])
def cron_handler():
	group = '402215639851440'
	#group = '147488415316365'

	graph = facebook.GraphAPI(access_token)
	profile = graph.get_object(group+'/feed')

	data = profile['data']
	for k in xrange(len(data)):
	    data[k]['updated_time'] = datetime.datetime.strptime(data[k]['updated_time'], "%Y-%m-%dT%H:%M:%S+%f")
        text = []
	for p in sorted(data, key=lambda x: x['updated_time']):
            text.append(u"%s" % str(p['updated_time']) + u': '+ p['message'])

    return 'ok'

