"""
Borderlands Web Scraper
"""
import datetime
import json
import os
import requests
import sys
import xmltodict
from dotenv import load_dotenv

load_dotenv()
BRODERLANDS_BOT = os.getenv("BRODERLANDS_BOT")
TEST = os.getenv("TEST")


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
        shift_archive = item.get("archive:shift")
        if shift_archive.get("shift:game") == "Borderlands 3":
            item_dict = {
                "Reward": shift_archive.get("shift:reward"),
                "Code": shift_archive.get("shift:code"),
                "Expires": shift_archive.get("shift:expires")
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
    message = requests.get(
        'https://api.telegram.org/bot924108836:AAHZykalHR8INIwplZERIwibUtDnUUdQN-8/'
        f'sendMessage?chat_id={group}'
        '=&text={}'.format(text)
    )

    return message


def main():
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
    code = parse_data()
    now = datetime.datetime.now().strftime("%d %b %Y %H:%M:%S")
    now_fromated = datetime.datetime.strptime(now, "%d %b %Y %H:%M:%S")
    with open("shiftcode.json", "r") as read:
        data = json.load(read)
    for shift_code in data.get("Shift_Codes"):
        old_code = shift_code.get("code")
        for item in code:
            # print(item.get("Code"))
            expires_date = item.get("Expires")[:-6]
            refromat_expires = datetime.datetime.strptime(
                expires_date, "%d %b %Y %H:%M:%S")
            message = f"""
            New Borderlands 3 Shift Code:\nReward: {item.get("Reward")}\nExpires: {expires_date}\nCode:
            """
            shift_code = item.get('Code')
            # print(shift_code)
    
            if refromat_expires > now_fromated and item.get("Code") != old_code:
                new_codes = {
                        "code": item.get("Code"),
                        "reward": item.get("Reward"),
                        "expires": item.get("Expires")
                    }
                if new_codes in data["Shift_Codes"]:
                    continue
                print(new_codes)
                data["Shift_Codes"].append(new_codes)
                with open("shiftcode.json", "w") as write:
                        json.dump(data, write)
                send_to_telegram(TEST, message)
                send_to_telegram(TEST, shift_code)
        return
    send_to_telegram(TEST, "No New Codes Available")


if __name__ == '__main__':
    main()
