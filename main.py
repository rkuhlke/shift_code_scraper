"""
Borderlands Web Scraper
"""
import datetime
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
BRODERLANDS_3_CODES = os.getenv("BRODERLANDS_3_CODES")
TEST = os.getenv("TEST")
BOT_ID = os.getenv("BOT_ID")
BORDERLANDS_SHIFT_CODES = os.getenv("BORDERLANDS_SHIFT_CODES")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


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
            item_dict = {
                "Game": game,
                "Platform": item.get("archive:shift").get("shift:platform"),
                "Reward": item.get("archive:shift").get("shift:reward"),
                "Code": item.get("archive:shift").get("shift:code"),
                "Published": str(pubDate),
                "Expires": str(pd.to_datetime(item.get("archive:shift").get("shift:expires")[:-6]))
            }
            stored_codes["Shift_Codes"].append(item_dict)
    if new_codes == True:
        pass
        # with open("./shiftcode.json", "w+") as writer:
        #     writer.write(json.dumps(stored_codes))
    else:
        send2Telegram(TEST, "No New Codes")


def sendCode(item):
    print(item)
    upload2Shift(item)
    # game = item.get("archive:shift").get("shift:game")
    # platform = item.get("archive:shift").get("shift:platform")
    # reward = item.get("archive:shift").get("shift:reward")
    # code = item.get("archive:shift").get("shift:code")
    # expires = item.get("archive:shift").get("shift:expires")[:-6]
    # message = f"New {game} Code!\n\nPlatform: {platform}\nReward: {reward}\nExpires: {expires}"
    # if game == "Borderlands 3":
    #     send2Telegram(TEST, message)
    #     send2Telegram(TEST, code)
    # else:
    #     send2Telegram(BORDERLANDS_SHIFT_CODES, message)
    #     send2Telegram(BORDERLANDS_SHIFT_CODES, code)
        

def upload2Shift(data):
    srv = Upload2Shift(USERNAME, PASSWORD)
    srv.uploadCode(data)


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
    getRawShiftData()


if __name__ == "__main__":
    main()


# def get_data():
#     """
#     Description:\n
#     \t Pulls the data from the url
#     \t and converts the data from xml to json

#     Returns:\n
#     \t data(dict): json converted data
#     """
#     try:
#         request = requests.get('https://shift.orcicorn.com/index.xml')
#     except Exception as e:
#         sys.exit(send_to_telegram(TEST, e))
#     response = xmltodict.parse(request.content)
#     parsed_response = json.dumps(response)
#     data = json.loads(parsed_response)
#     return data


# def parse_data():
#     """
#     Description:\n
#     \t Parses the data and creates a list

#     Returns:\n
#     \t content-list(list): list of dictionaires
#     """
#     content_list = []
#     data = get_data()
#     content = data.get("rss").get("channel")
#     for item in content.get("item"):
#         if "Borderlands 3" in item.get("title"):
#             published_date = item.get("pubDate")[:-6]
#             shift_archive = item.get("archive:shift")
#             item_dict = {
#                 "Date_Published": published_date,
#                 "Platform": shift_archive.get("shift:platform"),
#                 "Code": shift_archive.get("shift:code"),
#                 "Reward": shift_archive.get("shift:reward"),
#                 "Expires": shift_archive.get("shift:expires")[:-6]
#             }
#             content_list.append(item_dict)
#     return content_list


# def send_to_telegram(group, text):
#     """
#     sends the message to telegram
#     :param group: choose what telegram group to send message to
#     :param text: allows you to choose what message to send
#     :return: message
#     """
#     # sends a message to telegram
#     message = requests.get(f"""https://api.telegram.org/bot{BOT_ID}/sendMessage?chat_id={group}=&text={text}""")
#     return message


# def send_code():
#     """
#     Desctiption:\n
#     \t Main functionality that will compare
#     \t the old code and the experation data
#     \t will send the code if the expireation date
#     \t is greater than current time and if the old code
#     \t is different from new code

#     Returns:\n
#     \t None
#     """
#     sent_code = False
#     code = parse_data()
#     now = datetime.datetime.now().strftime("%d %b %Y %H:%M:%S")
#     now_fromated = datetime.datetime.strptime(now, "%d %b %Y %H:%M:%S")
#     with open(f"./shiftcode.json", "r") as read:
#         data = json.load(read)
#     for item in code:
#         for codes in data.get("Shift_Codes"):
#             expires_date = item.get("Expires")
#             refromat_expires = datetime.datetime.strptime(
#                 expires_date, "%d %b %Y %H:%M:%S")
#             message = f"""
#             New Borderlands 3 Shift Code!!!\n\nReward: {item.get("Reward")}\nPlatform: {item.get("Platform")}\nExpires: {expires_date}\nCode:
#             """
#             code_sent = item.get("Code")
#             if refromat_expires > now_fromated and item.get("Code") not in codes.get("Code"):                
#                 new_codes = {
#                         "Date_Published": item.get("Date_Published"),
#                         "Platform": item.get("Platform"),
#                         "Code": item.get("Code"),
#                         "Reward": item.get("Reward"),
#                         "Expires": item.get("Expires"),
#                     }
#                 if new_codes in data["Shift_Codes"]:
#                     continue
#                 data["Shift_Codes"].append(new_codes)
#                 with open(f"./shiftcode.json", "w") as write:
#                     json.dump(data, write)
#                 send_to_telegram(BRODERLANDS_3_CODES, message)
#                 send_to_telegram(BRODERLANDS_3_CODES, code_sent)
#                 sent_code = True

#     if sent_code == False:
#         send_to_telegram(TEST, "No New Codes Available")
#         return "Fail"
#     return
        
    

# def main():
#     rand_time = random.randrange(7200)
#     time.sleep(rand_time) # Comment out for testing purposes. Sets a random time to start calling website
#     date = datetime.datetime.date(datetime.datetime.now())
#     now = datetime.datetime.now()
#     if send_code() == "Fail":
#         with open(f"./logs/Shift_Bot_Logs_{date}.txt", "w+") as writer:
#             writer.write(f"Time Ran: {now}\nStatus: Fail\nRandom Time: {rand_time} seconds")
#     else:
#         with open(f"./logs/Shift_Bot_Logs_{date}.txt", "w+") as writer:
#             writer.write(f"Time Ran: {now}\nStatus: Success\nRandom Time: {rand_time} seconds")


# if __name__ == '__main__':
#     main()
