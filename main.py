import requests
import time
from bs4 import BeautifulSoup
from telegram import Bot

# === НАСТРОЙКИ ===
URL = "https://fruityblox.com/stock"
CHECK_INTERVAL = 30  # проверять каждые 30 сек

TELEGRAM_TOKEN = "8537002336:AAGGbHi_Amexh6dbKVVU_7Fr-HIZGJtZG2w"  # <-- Вставь свой токен
TELEGRAM_CHAT_ID = -5026548489              # <-- ID твоего чата

tg_bot = Bot(token=TELEGRAM_TOKEN)

# список фруктов игры
FRUITS = [
    "Rocket", "Spin", "Chop", "Spring", "Bomb", "Smoke", "Spike",
    "Flame", "Ice", "Sand", "Dark", "Diamond", "Light", "Rubber",
    "Barrier", "Ghost", "Magma", "Quake", "Buddha", "Love", "Spider",
    "Sound", "Phoenix", "Portal", "Rumble", "Pain", "Blizzard", 
    "Gravity", "Mammoth", "T-Rex", "Dough", "Shadow", "Venom",
    "Control", "Spirit", "Dragon", "Leopard", "Kitsune", "Yeti",
    "Tiger", "Gas"
]

last_stock = set()  # прошлый сток


def get_stock():
    """Скачивает сайт и ищет фрукты в тексте."""
    response = requests.get(URL, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text(separator=" ").lower()

    found = [f for f in FRUITS if f.lower() in text]
    return set(found)


def send_new_fruits(new):
    text = "🆕 *Новые фрукты в стоке:*\n\n" + "\n".join(f"• {f}" for f in new)

    tg_bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=text,
        parse_mode="Markdown"
    )


def monitor():
    global last_stock
    print("Бот запущен, мониторинг сайта...")

    while True:
        try:
            current_stock = get_stock()

            # новые фрукты = те, которых раньше не было
            new_fruits = current_stock - last_stock

            if new_fruits:
                send_new_fruits(new_fruits)
                print("Новые фрукты:", new_fruits)

            # запоминаем текущий сток
            last_stock = current_stock

        except Exception as e:
            print("Ошибка:", e)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor()
