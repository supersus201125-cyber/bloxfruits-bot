import requests
import time
from telegram import Bot

# === НАСТРОЙКИ ===
API_URL = "https://fruityblox.com/api/stock"  # новый рабочий API
CHECK_INTERVAL = 5 * 60  # каждые 5 минут

TELEGRAM_TOKEN = "8537002336:AAGGbHi_Amexh6dbKVVU_7Fr-HIZGJtZG2w"
TELEGRAM_CHAT_ID = -1003378537484

tg_bot = Bot(token=TELEGRAM_TOKEN)

ALL_FRUITS = [
    "Bomb", "Spike", "Chop", "Spring", "Rocket", "Smoke", "Spin", "Flame",
    "Ice", "Sand", "Dark", "Diamond", "Light", "Love", "Rubber", "Creation",
    "Magma", "Quake", "Buddha", "String", "Phoenix", "Portal", "Rumble",
    "Pain", "Gravity", "Dough", "Shadow", "Venom", "Control", "Spirit",
    "Dragon", "Leopard", "Ghost", "Spider", "Sound",
    "Blizzard", "Mammoth", "T-Rex", "Kitsune", "Yeti", "Tiger", "Gas"
]

def fetch_stock():
    """Получает сток через официальный JSON API сайта"""
    try:
        response = requests.get(API_URL, timeout=15)
        data = response.json()

        # API возвращает {"stock": ["Flame", "Portal", ...]}
        fruits = data.get("stock", [])

        # фильтруем только реальные фрукты
        fruits = [f for f in fruits if f in ALL_FRUITS]

        return fruits

    except Exception as e:
        print("Ошибка API:", e)
        return []


def format_stock_message(stock):
    if not stock:
        return "❌ Сток пуст или сайт временно недоступен."

    message = "🍇 *Текущий сток FruityBlox:*\n\n"
    message += "\n".join(f"• {fruit}" for fruit in stock)

    return message


def monitor_loop():
    while True:
        try:
            stock = fetch_stock()
            msg = format_stock_message(stock)
            tg_bot.send_message(TELEGRAM_CHAT_ID, msg, parse_mode="Markdown")
            print("Сток отправлен.")
        except Exception as e:
            print("Ошибка при отправке в Telegram:", e)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor_loop()
