#!/usr/bin/env python
import logging

import os
from google.appengine.ext import vendor
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))

import telegram
from flask import Flask, request
import facebook
import requests
import datetime


app = Flask(__name__)

global bot
bot = telegram.Bot(token='361644162:AAGbFjy05HbhgK5CptAp6RNPuj70-AjmU8E')


@app.route('/webhook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        chat_id = update.message.chat.id

        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.message.text.encode('utf-8')

	access_token = '143482932843931|_cRZXkEO6FGQgyC1Vv0xK66wKKA'
	group = '402215639851440'
	#group = '147488415316365'

	graph = facebook.GraphAPI(access_token)
	profile = graph.get_object(group+'/feed')

        logging.info(str(profile))

	data = profile['data']
	for k in xrange(len(data)):
	    data[k]['updated_time'] = datetime.datetime.strptime(data[k]['updated_time'], "%Y-%m-%dT%H:%M:%S+%f")
	for p in sorted(data, key=lambda x: x['updated_time']):
            bot.sendMessage(chat_id=chat_id, text=p['updated_time']+': '+ p['message'])

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('https://viajes.casassa.cl/webhook')
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'
