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
        if text == '/reset':
            lastpostsent.date = datetime.datetime.now() - datetime.timedelta(hours=100)

        if lastpostsent.date < date:
            lastpostsent.date = date

        posts = Post.query(Post.date > lastpostsent.date).order(Post.date).fetch()
        for post in posts:
            text = u'%s' % str(post.date-datetime.timedelta(hours=3)) + u'\n' + u'<a href="https://www.facebook.com/' + post.user_id + '">' + post.username + '</a>' + u'\n' + u'%s' % post.text + u'\n' + u'<a href="' + post.url + u'">Ir al post</a>'
            bot.sendMessage(chat_id=chat_id, text=text, parse_mode='HTML', disable_web_page_preview=True)
            postdate = post.date
        if len(posts) <= 0:
            bot.sendMessage(chat_id=chat_id, text=u'No hay nuevos posts. :/ Intenta mas tarde.')
        else:
            lastpostsent.date = postdate
            lastpostsent.put()

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

