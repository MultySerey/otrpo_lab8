# Лабораторная работа 8 по ОТРПО
Телеграм-бот для отправки электронных писем
## Требования
- Python >= 3.9.0
- Токен Telegram API
- Электронная почта для отправки писем
- SMTP-сервер
## Зависимости
- python-telegram-bot
- python-dotenv
## Использование
1. Переименуйте `.env.example` в `.env` и заполните все поля.
2. Создаём Virtual Env
```shell
python -m venv .venv
```
3. Активируем Virtual Env
```shell
.venv\Scripts\Activate
```
4. Устанавливаем необходимые библиотеки
```shell
pip install -r requirements.txt
```
5. Запускаем бота
```shell
python main.py
```