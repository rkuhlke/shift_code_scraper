"""
Borderlands Web Scraper
"""
import json
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from datetime import datetime

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def fetch_shift_codes():
    url = "https://www.pcgamer.com/games/fps/borderlands-4-shift-codes/"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    codes = []
    rows = soup.select("table")
    for row in rows:
        cols = row.select("tr", {"class": "table__body__row"})
        for col in cols:
            data = col.find_all("p")
            expires = data[0].get_text(strip=True)
            reward = data[1].get_text(strip=True)
            code = data[2].get_text(strip=True)

            if code != "Shift Code":
                codes.append({
                    "code": code,
                    "reward": reward,
                    "expires": expires,
                    "source": url
                })
        break # multiple tables only grabbing first due to active ones
    return codes
def send_to_discord(message):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "embeds": [message]
    }
    response = requests.post(WEBHOOK_URL, data=json.dumps(data, indent=2, default=str), headers=headers)
    if 200 <= response.status_code < 300:
        print(f"Webhook sent successfully: {response.status_code}")
    else:
        print(f"Failed to send webhook: {response.status_code}, response: {response.text}")
    return

def main():
    with open("shift_codes.json", "r") as r:
        cached_codes = json.loads(r.read())
    data = fetch_shift_codes()
    for shift_code in data:
        if cached_codes.get(shift_code.get("code")):
            continue
        embed = {
            "title": "New Shift Code Found",
            "description": "Upload code to https://shift.gearboxsoftware.com/rewards",
            "color": 0xE17C35,  # Green color
            "fields": [
                {"name": "Code", "value": shift_code.get("code"), "inline": True},
                {"name": "Reward", "value": shift_code.get("reward"), "inline": True},
                {"name": "Expires", "value": shift_code.get("expires"), "inline": True},
            ]
        }
        send_to_discord(embed)
        cached_codes.update({
            shift_code.get("code"): shift_code
        })
        with open("shift_codes.json", "w") as w:
            w.write(json.dumps(cached_codes, indent=4, default=str))
if __name__ == "__main__":
    main()
