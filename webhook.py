import json
from http.server import BaseHTTPRequestHandler

from telebot import types
from handler import bot  # Подключаем вашего бота из другого файла

class handler(BaseHTTPRequestHandler):
    server_version = 'WebhookHandler/1.0'

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

def vercel_handler(request):
    # Вызываем методы обработки запросов вручную
    if request.method == 'POST':
        handler.do_POST(request)
    elif request.method == 'GET':
        handler.do_GET(request)

# Это необходимо для корректной работы Vercel
if __name__ == '__main__':
    from http.server import HTTPServer
    import os
    server = HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 5000))),handler())
    server.serve_forever()
