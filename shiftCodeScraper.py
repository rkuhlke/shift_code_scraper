""""""
import os
import requests
import sys
import xmltodict
from utilities.aws.aws import AWS
from utilities.messaging.telegram import TelegramBots

BUCKET = os.getenv("BUCKET")
KEY = os.getenv("KEY")

class ShiftCodeScraper:
    def __init__(self, secret):
        self.aws = AWS()
        self.tableName = os.getenv("TABLE_NAME")
        self.secrets = secret
        self.bot_id = self.secrets.get("bot_id")
    
    def shiftCodeScraper(self):
        newCodes = self.__parseCodes__()
        if newCodes:
            return newCodes
        return False
    
    def __parseCodes__(self):
        content = self.__getNewCodes__().get("rss").get("channel").get("item")
        newShiftCodes = []
        for shiftcode in content:
            # Converts existing string datetime to a datetime object and then converts it to a string datetime and then Converts it back to a datatime
            item_dict = {
                "game": shiftcode.get("archive:shift").get("shift:game"),
                "platform": shiftcode.get("archive:shift").get("shift:platform"),
                "reward": shiftcode.get("archive:shift").get("shift:reward"),
                "code": shiftcode.get("archive:shift").get("shift:code"),
                "published": shiftcode.get("pubDate"),
                "expires": shiftcode.get("archive:shift").get("shift:expires")
            }
            if self.__checkDDB__(item_dict):
                continue
            newShiftCodes.append(item_dict)
            self.aws.ddbPutItem(self.tableName, item_dict)
        if newShiftCodes:
            return newShiftCodes
        else:
            TelegramBots().send2Telegram(self.bot_id, self.secrets.get("telegram_id_bobby"), "No New Codes")
            return False
    
    def __getNewCodes__(self):
        try:
            r = requests.get("https://shift.orcicorn.com/index.xml")
        except requests.RequestException as error:
            # Alerts me directly if there is an issue with requesting source data
            sys.exit(TelegramBots().send2Telegram(self.bot_id, self.secrets.get("telegram_id_bobby"), error))
        return xmltodict.parse(r.content)
    
    def __checkDDB__(self, codes):
        code = codes.get("code")
        tableData = self.aws.ddbGettem(self.tableName, "code", code)
        if tableData:
            return True
        return False
        
    # def __getStoredCodes__(self):
    #     return json.loads(AWS().s3GetObject(BUCKET, KEY))

    # def __writeNewCodes__(self, data):
    #     AWS().s3PutObject(bucket=BUCKET, key=KEY, data=data)
    #     return
