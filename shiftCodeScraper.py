
import json
import os
import requests
import sys
import xmltodict
from datetime import datetime
from utilities.aws.aws import AWS
from utilities.messaging.telegram import TelegramBots

BUCKET = os.getenv("BUCKET")
KEY = os.getenv("KEY")

class ShiftCodeScraper:
    def __init__(self, secret):
        self.secrets = secret
        self.bot_id = self.secrets.get("bot_id")
    
    def shiftCodeScraper(self):
        newCodes = self.__parseCodes__()
        if newCodes:
            return newCodes
        return False
    
    def __parseCodes__(self):
        storedCodes = self.__getStoredCodes__()
        mostRecentStoredCodePublishedDate = datetime.strptime(storedCodes.get("Shift_Codes")[-1].get("Published"), "%Y-%m-%d %H:%M:%S")
        newCode = False
        content = self.__getNewCodes__().get("rss").get("channel").get("item")
        newShiftCodes = []
        for shiftcode in content:
            # Converts existing string datetime to a datetime object and then converts it to a string datetime and then Converts it back to a datatime
            pubDate = datetime.strptime(datetime.strftime(datetime.strptime(shiftcode.get("pubDate"), "%a, %d %b %Y %H:%M:%S %z"), "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            if "Borderlands" in shiftcode.get("archive:shift").get("shift:game") and pubDate > mostRecentStoredCodePublishedDate:
                newCode = True
                shiftcode.get("archive:shift").get("shift:code")
                item_dict = {
                    "Game": shiftcode.get("archive:shift").get("shift:game"),
                    "Platform": shiftcode.get("archive:shift").get("shift:platform"),
                    "Reward": shiftcode.get("archive:shift").get("shift:reward"),
                    "Code": shiftcode.get("archive:shift").get("shift:code"),
                    "Published": str(pubDate),
                    "Expires": shiftcode.get("archive:shift").get("shift:expires")
                }
                storedCodes["Shift_Codes"].append(item_dict)
                newShiftCodes.append(item_dict)
        if newCode:
            self.__writeNewCodes__(storedCodes)
            return newShiftCodes
        else:
            TelegramBots.send2Telegram(self.bot_id, self.secrets.get("telegram_id_bobby"), "No New Codes")
            return False
    
    def __getNewCodes__(self):
        try:
            r = requests.get("https://shift.orcicorn.com/index.xml")
        except requests.RequestException as error:
            # Alerts me directly if there is an issue with requesting source data
            sys.exit(TelegramBots.send2Telegram(self.bot_id, self.secrets.get("telegram_id_bobby"), error))
        return xmltodict.parse(r.content)

    def __getStoredCodes__(self):
        return json.loads(AWS.s3GetObject(BUCKET, KEY))
        # with open("./shiftcode.json", "r") as reader:
        #     return json.loads(reader.read())

    def __writeNewCodes__(self, data):
        AWS.s3PutObject(bucket=BUCKET, key=KEY, data=data)
        # with open("./shiftcode.json", "w+") as writer:
        #     writer.write(json.dumps(data, indent=4))
        return
