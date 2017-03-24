#!/usr/bin/env python
import logging

import os
from google.appengine.ext import vendor
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))

import telegram
from flask import Flask, request
from db import Post, LastPostSent
import datetime


app = Flask(__name__)

global bot
bot = telegram.Bot(token='361644162:AAGbFjy05HbhgK5CptAp6RNPuj70-AjmU8E')


@app.route('/webhook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id

        text = update.message.text.encode('utf-8')

        date = datetime.datetime.now() - datetime.timedelta(hours=12)
        lastpostsent = LastPostSent().get_or_insert(str(chat_id), date=date)
        bot.sendMessage(chat_id=chat_id, text=str(lastpostsent))

        if lastpostsent.date < date:
            lastpostsent.date = date

        posts = Post.query(Post.date > lastpostsent.date).order(Post.date).fetch(2)
        for post in posts:
            bot.sendMessage(chat_id=chat_id, text=u'%s' % str(post.date) + u'\n' + u'%s' % post.text)
            postdate = post.date
        if len(posts) <= 0:
            bot.sendMessage(chat_id=chat_id, text=u'No hay nuevos posts. :/ Intenta mas tarde.')
        else:
            lastpostsent.date = postdate
            lastpostsent.put()

    return 'ok'

@app.route('/reset', methods=['GET', 'POST'])
def set_webhook():
    l = LastPostSent().get_or_insert('90004065')
    l.delete()
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

