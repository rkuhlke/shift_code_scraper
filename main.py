"""
Borderlands Web Scraper
"""
import json
import os
import pandas as pd
import requests
import random
import sys
import time
import xmltodict
from dotenv import load_dotenv
from upload_to_shift import Upload2Shift

load_dotenv()

BORDERLANDS_CODES = os.getenv("BORDERLANDS_CODES")
TEST = os.getenv("TEST")
BOT_ID = os.getenv("BOT_ID")


def getRawShiftData():
    try:
        r = requests.get("https://shift.orcicorn.com/index.xml")
    except requests.RequestException as error:
        sys.exit(send2Telegram(TEST, error))
    parseShiftData(xmltodict.parse(r.content))


def parseShiftData(data):
    with open("./shiftcode.json") as reader:
        stored_codes = json.loads(reader.read())
    mostRecentStoredCode = stored_codes.get("Shift_Codes")[-1]
    lastPublishedDate = pd.to_datetime(mostRecentStoredCode.get("Published"))
    content = data.get("rss").get("channel").get("item")
    new_codes = False
    for item in reversed(content):
        pubDate = pd.to_datetime(item.get("pubDate")[:-6])
        game  = item.get("archive:shift").get("shift:game")
        if pubDate > lastPublishedDate and "Borderlands" in game:
            sendCode(item)
            new_codes = True
            code = item.get("archive:shift").get("shift:code")
            item_dict = {
                "Game": game,
                "Platform": item.get("archive:shift").get("shift:platform"),
                "Reward": item.get("archive:shift").get("shift:reward"),
                "Code": code,
                "Published": str(pubDate),
                "Expires": str(pd.to_datetime(item.get("archive:shift").get("shift:expires")[:-6]))
            }
            stored_codes["Shift_Codes"].append(item_dict)
    if new_codes == True:
        with open("./shiftcode.json", "w+") as writer:
            writer.write(json.dumps(stored_codes))
    else:
        send2Telegram(TEST, "No New Codes")


def sendCode(item):
    game = item.get("archive:shift").get("shift:game")
    platform = item.get("archive:shift").get("shift:platform")
    reward = item.get("archive:shift").get("shift:reward")
    code = item.get("archive:shift").get("shift:code")
    expires = item.get("archive:shift").get("shift:expires")[:-6]
    with open("./creds.json", "r") as reader:
        creds_list = json.loads(reader.read())
    for users in creds_list:
        for _, creds in users.items():
            srv = Upload2Shift(creds.get("username"), creds.get("password"))
            srv.uploadCode(code)
            msg = f"New {game} Code!\n\nPlatform: {platform}\nReward: {reward}\nThis has been successfully uploaded to your account for all linked borderlands accounts"
            send2Telegram(creds.get("telegram_id"), msg)
    message = f"New {game} Code!\n\nPlatform: {platform}\nReward: {reward}\nExpires: {expires}"
    send2Telegram(BORDERLANDS_CODES, message)
    send2Telegram(BORDERLANDS_CODES, code)


def send2Telegram(group, text):
    """
    sends the message to telegram
    :param group: choose what telegram group to send message to
    :param text: allows you to choose what message to send
    :return: message
    """
    # sends a message to telegram
    return requests.get(f"""https://api.telegram.org/bot{BOT_ID}/sendMessage?chat_id={group}=&text={text}""")


def main():
    time.sleep(random.randint(0, 7200))
    getRawShiftData()


if __name__ == "__main__":
    main()
