#!/usr/bin/env python
import logging

import os
from google.appengine.ext import vendor
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))

from db import Post
from flask import Flask
import facebook
import datetime

access_token = '143482932843931|_cRZXkEO6FGQgyC1Vv0xK66wKKA'
group = '402215639851440'
#group = '147488415316365'

app = Flask(__name__)


@app.route('/cron', methods=['GET', 'POST'])
def cron_handler():
    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object(group+'/feed?fields=message,from,created_time,permalink_url')
    data = profile['data']
    for k in xrange(len(data)):
        data[k]['created_time'] = datetime.datetime.strptime(data[k]['created_time'], "%Y-%m-%dT%H:%M:%S+%f")

    for p in sorted(data, key=lambda x: x['created_time']):
        query = Post.query(Post.fb_id == p['id']).fetch(1)
        if len(query) <= 0:
            post = Post(fb_id=p['id'], date=p['created_time'], text=p['message'], username=p['from']['name'], user_id=p['from']['id'], url=p['permalink_url'])
            k = post.put()
            logging.info("key id: %s %s" % (str(k.id), p['id']))

    return 'ok'

