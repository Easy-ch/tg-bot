import json
from http.server import SimpleHTTPRequestHandler
import requests
import time 
from telebot import types
from bot import bot  # Подключаем вашего бота из другого файла
server_url = "https://bbbb-alpha.vercel.app"
update_interval = 120
def update_server():
    try:
        response = requests.get(server_url)
        if response.status_code == 200:
            print("Страница успешно обновлена.")
        else:
            print(f"Ошибка при обновлении страницы. Код состояния: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при попытке обновления страницы: {str(e)}")

if __name__ == "__main__":
    while True:
        update_server()
        time.sleep(update_interval)
class handler(SimpleHTTPRequestHandler):
    server_version = 'WebhookHandler/1.0'

    def do_GET(self):
        try:
            # Устанавливаем вебхук при получении GET-запроса
            bot.set_webhook('https://' + 'bbbb-alpha.vercel.app')
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
my_handler = handler()

# Функция, которая будет вызываться Vercel при обработке запросов
def vercel_handler(request):
    # Вызываем методы обработки запросов вручную
    if request.method == 'POST':
        my_handler.do_POST(request)
    elif request.method == 'GET':
        my_handler.do_GET(request)

# Это необходимо для корректной работы Vercel
if __name__ == '__main__':
    from http.server import HTTPServer
    import os
    server = HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 5000))), my_handler)
    server.serve_forever()
