import json
import os
import time
from http.server import BaseHTTPRequestHandler

from telebot import types

from bot import bot


class handler(BaseHTTPRequestHandler):
    server_version = 'WebhookHandler/1.0'
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_GET(self):
        bot.set_webhook('https://' + 'bbbb-alpha.vercel.app')
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        cl = int(self.headers.get('Content-Length',0))
        post_data = self.rfile.read(cl)
        body = json.loads(post_data.decode())

        bot.process_new_updates([types.Update.de_json(body)])

        self.send_response(204)
        self.end_headers()

