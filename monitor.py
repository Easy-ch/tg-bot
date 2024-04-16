import requests
import time
server_url = 'https://bbbb-alpha.vercel.app/'
update_interval = 20
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
