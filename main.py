import requests
import time
import json
from bs4 import BeautifulSoup
from telegram import Bot

# === НАСТРОЙКИ ===
URL = "https://fruityblox.com/stock"  # можно заменить, если найдёшь другой источник
CHECK_INTERVAL = 2 * 60 * 60  # проверять каждые 2 часа

TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN"
TELEGRAM_CHAT_ID = 123456789  # <- твой chat_id

tg_bot = Bot(token=TELEGRAM_TOKEN)
STATE_FILE = "blox_stock_state.json"

def fetch_stock(url=URL):
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    result = {"normal": [], "mirage": []}

    # Примерные селекторы — их может потребоваться подстроить под реальный HTML сайта
    # Предположим, обычный сток в <div id="normal-stock">, мираж — в <div id="mirage-stock">
    normal_div = soup.find(id="normal-stock")
    if normal_div:
        for li in normal_div.find_all("li"):
            name = li.get_text(strip=True)
            if name:
                result["normal"].append(name)

    mirage_div = soup.find(id="mirage-stock")
    if mirage_div:
        for li in mirage_div.find_all("li"):
            name = li.get_text(strip=True)
            if name:
                result["mirage"].append(name)

    # Если HTML другая структура — нужно подправить парсинг
    return result

def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"normal": [], "mirage": []}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False)

def diff_and_notify(old, new):
    messages = []
    # Проверить обычный сток
    new_norm = set(new.get("normal", []))
    old_norm = set(old.get("normal", []))
    added_norm = new_norm - old_norm
    if added_norm:
        messages.append("🍎 Новый обычный сток:\n" + "\n".join(sorted(added_norm)))

    # Проверить мираж‑сток
    new_mir = set(new.get("mirage", []))
    old_mir = set(old.get("mirage", []))
    added_mir = new_mir - old_mir
    if added_mir:
        messages.append("✨ Новый мираж‑сток:\n" + "\n".join(sorted(added_mir)))

    # Если есть, отправить
    for msg in messages:
        tg_bot.send_message(TELEGRAM_CHAT_ID, msg)

    return bool(messages)

def monitor_loop():
    prev = load_state()
    while True:
        try:
            current = fetch_stock()
        except Exception as e:
            print("Ошибка при получении стока:", e)
            time.sleep(60)
            continue

        changed = diff_and_notify(prev, current)
        if changed:
            save_state(current)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_loop()
