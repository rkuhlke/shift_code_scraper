"""
Borderlands Web Scraper
"""
import datetime
import json
import os
import requests
import random
import sys
import time
import xmltodict
from dotenv import load_dotenv

load_dotenv()
BRODERLANDS_BOT = os.getenv("BRODERLANDS_BOT")
TEST = os.getenv("TEST")
PATH_TO_CODES = os.getenv("PATH_TO_CODES")
BOT_ID = os.getenv("BOT_ID")


def get_data():
    """
    Description:\n
    \t Pulls the data from the url
    \t and converts the data from xml to json

    Returns:\n
    \t data(dict): json converted data
    """
    try:
        request = requests.get('https://shift.orcicorn.com/index.xml')
    except Exception as e:
        sys.exit(send_to_telegram(TEST, e))
    response = xmltodict.parse(request.content)
    parsed_response = json.dumps(response)
    data = json.loads(parsed_response)
    return data


def parse_data():
    """
    Description:\n
    \t Parses the data and creates a list

    Returns:\n
    \t content-list(list): list of dictionaires
    """
    content_list = []
    data = get_data()
    content = data.get("rss").get("channel")
    for item in content.get("item"):
        if "Borderlands 3" in item.get("title"):
            published_date = item.get("pubDate")[:-6]
            shift_archive = item.get("archive:shift")
            item_dict = {
                "Date_Published": published_date,
                "Code": shift_archive.get("shift:code"),
                "Reward": shift_archive.get("shift:reward"),
                "Expires": shift_archive.get("shift:expires")[:-6]
            }
            content_list.append(item_dict)
    return content_list


def send_to_telegram(group, text):
    """
    sends the message to telegram
    :param group: choose what telegram group to send message to
    :param text: allows you to choose what message to send
    :return: message
    """
    # sends a message to telegram
    message = requests.get(f"""https://api.telegram.org/bot{BOT_ID}/sendMessage?chat_id={group}=&text={text}""")
    return message


def send_code():
    """
    Desctiption:\n
    \t Main functionality that will compare
    \t the old code and the experation data
    \t will send the code if the expireation date
    \t is greater than current time and if the old code
    \t is different from new code

    Returns:\n
    \t None
    """
    sent_code = False
    code = parse_data()
    now = datetime.datetime.now().strftime("%d %b %Y %H:%M:%S")
    now_fromated = datetime.datetime.strptime(now, "%d %b %Y %H:%M:%S")
    with open(f"{PATH_TO_CODES}shiftcode.json", "r") as read:
        data = json.load(read)
    for item in code:
        for codes in data.get("Shift_Codes"):
            expires_date = item.get("Expires")
            refromat_expires = datetime.datetime.strptime(
                expires_date, "%d %b %Y %H:%M:%S")
            message = f"""
            New Borderlands 3 Shift Code!!!\n\nReward: {item.get("Reward")}\nExpires: {expires_date}\nCode:
            """
            code_sent = item.get("Code")
            if refromat_expires > now_fromated and item.get("Code") not in codes.get("Code"):                
                new_codes = {
                        "Date_Published": item.get("Date_Published"),
                        "Code": item.get("Code"),
                        "Reward": item.get("Reward"),
                        "Expires": item.get("Expires"),
                    }
                if new_codes in data["Shift_Codes"]:
                    continue
                data["Shift_Codes"].append(new_codes)
                with open(f"{PATH_TO_CODES}shiftcode.json", "w") as write:
                    json.dump(data, write)
                send_to_telegram(BRODERLANDS_BOT, message)
                send_to_telegram(BRODERLANDS_BOT, code_sent)
                sent_code = True

    if sent_code == False:
        send_to_telegram(TEST, "No New Codes Available")     
        
    

def main():
    rand_time = random.randrange(7200)
    time.sleep(rand_time)
    send_code()
    date = datetime.datetime.date(datetime.datetime.now())
    now = datetime.datetime.now()
    with open(f"{PATH_TO_CODES}logs/Shift_Bot_Logs_{date}.txt", "w+") as writer:
        writer.write(f"Time Ran: {now}")


if __name__ == '__main__':
    main()
