"""
Borderlands Web Scraper
"""
import csv
import json
import requests
import xmltodict
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
BRODERLANDS_BOT = os.getenv("BRODERLANDS_BOT")
TEST = os.getenv("TEST")


def get_data():
    """
    builds the html parser
    :return: soup
    """
    xml = requests.get('https://shift.orcicorn.com/index.xml')
    data = xmltodict.parse(xml.content)
    j = json.dumps(data)
    d = json.loads(j)
    return d


def parse_data():
    l = []
    data = get_data()
    content = data.get("rss").get("channel")
    for item in content.get("item"):
        shift_archive = item.get("archive:shift")
        if shift_archive.get("shift:game") == "Borderlands 3":
            d = {
                "Game": shift_archive.get("shift:game"),
                "Reward": shift_archive.get("shift:reward"),
                "Code": shift_archive.get("shift:code"),
                "Expires": shift_archive.get("shift:expires")
            }
            l.append(d)
    return l


def send_to_telegram(group, text):
    """
    sends the message to telegram
    :param group: choose what telegram group to send message to
    :param text: allows you to choose what message to send
    :return: message
    """

    # sends a message to telegram
    message = requests.get(
        'https://api.telegram.org/bot924108836:AAHZykalHR8INIwplZERIwibUtDnUUdQN-8/'
        f'sendMessage?chat_id={group}'
        '=&text={}'.format(text)
    )

    return message


def main():
    code = parse_data()
    with open("shiftcode.txt", "r") as read:
        old_code = read.read()
    now = datetime.datetime.now().strftime("%d %b %Y %H:%M:%S")
    now_fromated = datetime.datetime.strptime(now, "%d %b %Y %H:%M:%S")
    for item in code:
        expires_date = item.get("Expires")[:-6]
        refromat_expires = datetime.datetime.strptime(
            expires_date, "%d %b %Y %H:%M:%S")
        message = f"""
        New Borderlands 3 Shift Code:\nReward: {item.get("Reward")}\nExpires: {expires_date}\nCode:
        """
        shift_code = f"{item.get('Code')}"
        if refromat_expires > now_fromated and item.get("Code") != old_code:
            send_to_telegram(BRODERLANDS_BOT, message)
            send_to_telegram(BRODERLANDS_BOT, shift_code)
        with open("shiftcode.txt", "w") as write:
            write.write(item.get("Code"))


if __name__ == '__main__':
    main()
