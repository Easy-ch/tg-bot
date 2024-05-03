import json
from http.server import BaseHTTPRequestHandler
import time 
from telebot import types
from handler import bot  # Подключаем вашего бота из другого файла

class handler(BaseHTTPRequestHandler):
    server_version = 'WebhookHandler/1.0'
    time.sleep(5)
    def do_GET(self):
        try:
            # Устанавливаем вебхук при получении GET-запроса
            bot.set_webhook('https://bbbb-alpha.vercel.app')
            self.send_response(200)
            self.end_headers()
        except Exception as e:
            print(e)
    def do_POST(self):
        try:
            # Обрабатываем POST-запросы (входящие обновления от Telegram)
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode())
            bot.process_new_updates([types.Update.de_json(body)])
            self.send_response(204)
            self.end_headers()
        except Exception as e:
            print(e)
