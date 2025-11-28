import requests
import time
import json
from bs4 import BeautifulSoup
from telegram import Bot

# === НАСТРОЙКИ ===
URL = "https://fruityblox.com/stock"  # источник данных
CHECK_INTERVAL = 5 * 60  # каждые 5 минут

TELEGRAM_TOKEN = "8537002336:AAGGbHi_Amexh6dbKVVU_7Fr-HIZGJtZG2w"
TELEGRAM_CHAT_ID = -1003378537484  # ID чата/группы

tg_bot = Bot(token=TELEGRAM_TOKEN)
STATE_FILE = "blox_stock_state.json"

def fetch_stock(url=URL):
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    result = {"normal": [], "mirage": []}

    # === Важно! Подставь свои селекторы под сайт ===
    normal_div = soup.find(id="normal-stock")  # пример
    if normal_div:
        result["normal"] = [li.get_text(strip=True) for li in normal_div.find_all("li")]

    mirage_div = soup.find(id="mirage-stock")  # пример
    if mirage_div:
        result["mirage"] = [li.get_text(strip=True) for li in mirage_div.find_all("li")]

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

    # обычный сток
    added_normal = set(new.get("normal", [])) - set(old.get("normal", []))
    if added_normal:
        messages.append("🍎 Новый обычный сток:\n" + "\n".join(sorted(added_normal)))

    # мираж
    added_mirage = set(new.get("mirage", [])) - set(old.get("mirage", []))
    if added_mirage:
        messages.append("✨ Новый мираж‑сток:\n" + "\n".join(sorted(added_mirage)))

    for msg in messages:
        tg_bot.send_message(TELEGRAM_CHAT_ID, msg)

    return bool(messages)

def monitor_loop():
    prev_state = load_state()
    while True:
        try:
            current_state = fetch_stock()
        except Exception as e:
            print("Ошибка при получении стока:", e)
            time.sleep(60)
            continue

        changed = diff_and_notify(prev_state, current_state)
        if changed:
            save_state(current_state)
        else:
            # отправляем даже если изменений нет
            tg_bot.send_message(TELEGRAM_CHAT_ID, "🕒 Проверка стока: изменений нет")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_loop()
