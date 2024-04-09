import json
import os
import time
from http.server import BaseHTTPRequestHandler
from telebot import types
from main import bot
import asyncio
import websockets
async def connect_to_server():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send("Hello, Server!")
        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.get_event_loop().run_until_complete(connect_to_server())

class handler(BaseHTTPRequestHandler):
    server_version = 'WebhookHandler/1.0'

    def do_GET(self):
        time.sleep(2)
        bot.set_webhook('https://bbbb-alpha.vercel.app/')
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        cl = int(self.headers['Content-Length'])
        post_data = self.rfile.read(cl)
        body = json.loads(post_data.decode())

        self.process_message(body)  # Вызов метода для обработки сообщения

        self.send_response(204)
        self.end_headers()

    def process_message(self, body):
        bot.process_new_updates([types.Update.de_json(body)])
