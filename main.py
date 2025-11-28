import requests
import time
from bs4 import BeautifulSoup
from telegram import Bot

# === НАСТРОЙКИ ===
URL = "https://fruityblox.com/stock"  # источник данных
CHECK_INTERVAL = 5 * 60  # каждые 5 минут

TELEGRAM_TOKEN = "8537002336:AAGGbHi_Amexh6dbKVVU_7Fr-HIZGJtZG2w"
TELEGRAM_CHAT_ID = -1003378537484  # ID чата/группы

tg_bot = Bot(token=TELEGRAM_TOKEN)

# Список всех фруктов игры
ALL_FRUITS = [
    "Bomb", "Spike", "Chop", "Spring", "Rocked", "Smoke", "Spin", "Flame",
    "Ice", "Sand", "Dark", "Diamond", "Light", "Love", "Rubber", "Creation",
    "Magma", "Quake", "Buddha", "String", "Phoenix", "Portal", "Rumble",
    "Pain", "Gravity", "Dough", "Shadow", "Venom", "Control", "Spirit",
    "Dragon", "Leopard", "Ghost", "Spider", "Sound",
    "Blizzard", "Mammoth", "T-Rex", "Kitsune", "Yeti", "Tiger", "Gas"
]

def fetch_stock(url=URL):
    """Парсим сайт и возвращаем нормальный и миражный сток"""
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Получаем все элементы стока с сайта
    # Сайт может показывать фрукты в списках <li>, настраиваем селекторы
    stock_items = soup.find_all("li")
    normal_stock = []
    mirage_stock = []

    for li in stock_items:
        text = li.get_text(strip=True)
        # Определяем тип стока по тексту (обычно сайт пишет Normal / Mirage рядом)
        if "Normal" in text:
            fruit_name = text.replace("Normal:", "").strip()
            if fruit_name in ALL_FRUITS:
                normal_stock.append(fruit_name)
        elif "Mirage" in text:
            fruit_name = text.replace("Mirage:", "").strip()
            if fruit_name in ALL_FRUITS:
                mirage_stock.append(fruit_name)

    return {"normal": normal_stock, "mirage": mirage_stock}

def format_stock_message(stock):
    msg_lines = []
    normal = stock.get("normal", [])
    mirage = stock.get("mirage", [])

    if normal:
        msg_lines.append("🍎 Нормальный сток:")
        msg_lines.extend(f"- {fruit}" for fruit in normal)
    else:
        msg_lines.append("🍎 Нормальный сток: пусто")

    if mirage:
        msg_lines.append("\n✨ Миражный сток:")
        msg_lines.extend(f"- {fruit}" for fruit in mirage)
    else:
        msg_lines.append("\n✨ Миражный сток: пусто")

    return "\n".join(msg_lines)

def monitor_loop():
    while True:
        try:
            stock = fetch_stock()
            message = format_stock_message(stock)
            tg_bot.send_message(TELEGRAM_CHAT_ID, message)
        except Exception as e:
            print("Ошибка при получении или отправке стока:", e)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_loop()
