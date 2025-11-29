Зimport requests
import time
from telegram import Bot

API_URL = "https://blox-fruits-api.onrender.com/api/bloxfruits/stock"
CHECK_INTERVAL = 300 # проверяем каждые 60 секунд

TELEGRAM_TOKEN = "8537002336:AAGGbHi_Amexh6dbKVVU_7Fr-HIZGJtZG2w"
TELEGRAM_CHAT_ID = -1003378537484

tg_bot = Bot(token=TELEGRAM_TOKEN)

def fetch_stock():
    """Получает сток и логирует полный ответ API"""
    try:
        response = requests.get(API_URL, timeout=15)

        # Логируем статус и полный текст ответа
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

        # Пытаемся получить JSON
        data = response.json()
        stock = data.get("stock", [])

        return stock
    except Exception as e:
        print("Ошибка при запросе API:", e)
        return []

def format_stock_message(stock):
    if not stock:
        return "❌ Сток пуст или API недоступен."

    msg = "🍇 *Текущий сток Blox Fruits:*\n\n"
    msg += "\n".join(f"• {fruit}" for fruit in stock)

    return msg

def monitor_loop():
    while True:
        try:
            stock = fetch_stock()
            msg = format_stock_message(stock)
            tg_bot.send_message(TELEGRAM_CHAT_ID, msg, parse_mode="Markdown")
            print("Сток отправлен:", stock)
        except Exception as e:
            print("Ошибка отправки в Telegram:", e)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_loop()
