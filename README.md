# 🛍️ wn_market Telegram Bot

Этот репозиторий содержит исходный код Telegram-бота `wn_market`, ассистента онлайн ресейл магазина. Бот помогает пользователям рассчитать стоимость товаров по указанному курсу, предоставляет информацию о процессе оформления заказа и сроках доставки, а также включает панель администратора для установки курса. Бот написан с использованием библиотеки `aiogram` и работает на вебхуке.
## Возможности

- **Расчет стоимости**: Пользователи могут рассчитать общую стоимость товаров по текущему курсу.
- **Информация о заказе**: Бот предоставляет данные о процессе оформления заказа и предполагаемых сроках доставки.
- **Панель администратора**: Администраторы могут обновлять курс валют, используемый для расчетов стоимости, добавлять, удалять, заказ, а также изменять статус заказа в зависимости от его нахождения. 
- **Вебхуки**: Бот использует вебхуки для обработки обновлений Telegram, с документации aiogram.
- **Возможность отслеживания заказа**: Мониторинг нахождения заказа и его готовности к выдаче
## Используемые технологии

- **aiogram**: Фреймворк для работы с API Telegram на Python.
- **Postgresql**: СУБД, использумая в разработке данного бота 
- **Python**: Язык программирования, использованный для разработки бота.

## Установка

1. **Клонируйте репозиторий**:
    ```sh
    git clone https://github.com/Easy-ch/tg-bot.git
    cd bot_end
    ```

2. **Установите зависимости**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Настройте переменные окружения**:
    Создайте файл config.py и сохраните туда свои переменные 
   ```config.py
    TOKEN=your_telegram_bot_token
    ADMIN_ID=your_telegram_user_id
    Postgresql_url = your_url
   
    ```

4. **Запустите бота локально**:
    ```sh
    python handlers.py
    ```
## Использование

1. **Начните чат**: Начните чат с вашим ботом в Telegram.
2. **Команды пользователя**:
    ** Переданы ввиде клавиатуры, подробнее в keyboards.py проекта 


## Copyrigh 2024 Telny Ivan
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


Если у вас возникли вопросы или вам нужна дополнительная помощь, не стесняйтесь обращаться! Приятных покупок с `wn_market`! 🛒

---
