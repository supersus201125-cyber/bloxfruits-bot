import requests
import time
from telegram import Bot

# === НАСТРОЙКИ ===
API_URL = "https://blox-fruits-api.vercel.app/api/stock"
CHECK_INTERVAL = 5 * 60  # проверка каждые 5 минут

TELEGRAM_TOKEN = "8537002336:AAGGbHi_Amexh6dbKVVU_7Fr-HIZGJtZG2w"
TELEGRAM_CHAT_ID = -1003378537484

tg_bot = Bot(token=TELEGRAM_TOKEN)

def fetch_stock():
    """Получает Normal и Mirage сток с рабочего API"""
    try:
        response = requests.get(API_URL, timeout=15)
        data = response.json()

        normal = data.get("normal", [])
        mirage = data.get("mirage", [])

        return {"normal": normal, "mirage": mirage}

    except Exception as e:
        print("Ошибка API:", e)
        return {"normal": [], "mirage": []}


def format_stock_message(stock):
    normal = stock.get("normal", [])
    mirage = stock.get("mirage", [])

    msg_lines = []

    if normal:
        msg_lines.append("🍎 *Normal сток:*")
        msg_lines.extend(f"• {f}" for f in normal)
    else:
        msg_lines.append("🍎 Normal сток пуст")

    if mirage:
        msg_lines.append("\n✨ *Mirage сток:*")
        msg_lines.extend(f"• {f}" for f in mirage)
    else:
        msg_lines.append("\n✨ Mirage сток пуст")

    return "\n".join(msg_lines)


def monitor_loop():
    while True:
        try:
            stock = fetch_stock()
            msg = format_stock_message(stock)
            tg_bot.send_message(TELEGRAM_CHAT_ID, msg, parse_mode="Markdown")
            print("Сток отправлен:", stock)
        except Exception as e:
            print("Ошибка при отправке в Telegram:", e)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor_loop()
