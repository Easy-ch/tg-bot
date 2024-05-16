import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключаем вашего бота из другого файла
from bot import TOKEN

# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Настройки для вебхука
WEBHOOK_HOST = 'https://bbbb-alpha.vercel.app'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'  # IP-адрес сервера
WEBAPP_PORT = 3000        # Порт, на котором будет запущен веб-сервер

# Вебхук хэндлер
class WebhookHandler(BaseHTTPRequestHandler):
    server_version = 'WebhookHandler/1.0'

    def do_GET(self):
        try:
            # Устанавливаем вебхук при получении GET-запроса
            logger.info('Setting webhook...')
            bot.set_webhook(WEBHOOK_URL)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Webhook set successfully')
        except Exception as e:
            logger.error(f"Failed to set webhook: {e}")
            self.send_response(500)
            self.end_headers()

    def do_POST(self):
        try:
            # Обрабатываем POST-запросы (входящие обновления от Telegram)
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode())
            update = Update(**body)
            asyncio.run(dp.process_update(update))
            self.send_response(204)
            self.end_headers()
        except Exception as e:
            logger.error(f"Failed to process update: {e}")
            self.send_response(500)
            self.end_headers()

def run_server():
    server_address = (WEBAPP_HOST, WEBAPP_PORT)
    httpd = HTTPServer(server_address, WebhookHandler)
    logger.info(f'Starting server at http://{WEBAPP_HOST}:{WEBAPP_PORT}')
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        # Устанавливаем вебхук
        bot.set_webhook(WEBHOOK_URL)
        logger.info(f'Webhook set to {WEBHOOK_URL}')
        
        # Запускаем сервер для обработки запросов
        run_server()
    except Exception as e:
        logger.error(f'Error: {e}')
