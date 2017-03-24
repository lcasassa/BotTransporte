#!/usr/bin/env python
import logging

import os
from google.appengine.ext import vendor
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))

import telegram
from flask import Flask, request
from db import Post


app = Flask(__name__)

global bot
bot = telegram.Bot(token='361644162:AAGbFjy05HbhgK5CptAp6RNPuj70-AjmU8E')


@app.route('/webhook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id

        text = update.message.text.encode('utf-8')

        posts = Post.query(Post.date > (datetime.datetime.now()-datetime.timedelta(hours=12))).order(-Post.date).fetch(2)
        for post in posts:
            bot.sendMessage(chat_id=chat_id, text=u'%s' % str(post.date) + u'\n' + u'%s' % post.text)

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

