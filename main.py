from fastapi import FastAPI

# Инициализация FastAPI приложения
app = FastAPI()

# Проверка работоспособности сервера
@app.get("/")
async def root():
    """
    Корневой обработчик для проверки работоспособности сервера.
    """
    return {"status": "OK"}

# Запуск сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
