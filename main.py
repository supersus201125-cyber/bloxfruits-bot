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

def fetch_stock(url=URL):
    """Получаем сток обычных и миражных фруктов с сайта"""
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    result = {"normal": [], "mirage": []}

    # === Важно! Подставь селекторы под сайт ===
    normal_div = soup.find(id="normal-stock")  # пример
    if normal_div:
        result["normal"] = [li.get_text(strip=True) for li in normal_div.find_all("li")]

    mirage_div = soup.find(id="mirage-stock")  # пример
    if mirage_div:
        result["mirage"] = [li.get_text(strip=True) for li in mirage_div.find_all("li")]

    return result

def format_stock_message(stock):
    """Форматируем сообщение с текущим состоянием стока"""
    msg_lines = []

    normal = stock.get("normal", [])
    mirage = stock.get("mirage", [])

    if normal:
        msg_lines.append("🍎 Обычный сток:")
        msg_lines.extend(f"- {fruit}" for fruit in normal)
    else:
        msg_lines.append("🍎 Обычный сток: пусто")

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
