import json
import os
import time
from http.server import BaseHTTPRequestHandler

from telebot import types
from bot import bot

class handler(BaseHTTPRequestHandler):
    server_version = 'WebhookHandler/1.0'

    def do_GET(self):
        try:
            time.sleep(2)
            bot.set_webhook('https://' + 'bbbb-alpha.vercel.app')
            self.send_response(200)
            self.end_headers()
        except Exception as e:
            print(e)

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode('utf-8'))

            bot.process_new_updates([types.Update.de_json(body)])
            self.send_response(200)
            self.end_headers()
        except Exception as e:
            print(e)
