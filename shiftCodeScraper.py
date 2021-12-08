
import json
import os
import requests
import sys
import xmltodict
from datetime import datetime
from utilities.aws.aws import AWS

BUCKET = os.getenv("BUCKET")
KEY = os.getenv("KEY")

class ShiftCodeScraper:
    def __init__(self):
        self.secrets = AWS.getSecret("shift_code_scraper_secrets")
        self.bot_id = self.secrets.get("bot_id")
        self.testGroup = self.secrets.get("telegram_id_bobby")
        
    def __getNewCodes__(self):
        try:
            r = requests.get("https://shift.orcicorn.com/index.xml")
        except requests.RequestException as error:
            return
            # sys.exit(send2Telegram(TEST, error))
        return xmltodict.parse(r.content)

    def __parseCodes__(self, shiftCodes):
        storedCodes = self.__getStoredCodes__()
        mostRecentStoredCodePublishedDate = datetime.strptime(storedCodes.get("Shift_Codes")[-1].get("Published"), "%Y-%m-%d %H:%M:%S")
        newCode = False
        content = shiftCodes.get("rss").get("channel").get("item")
        newShiftCodes = []
        for shiftcode in content:
            # Converts existing string datetime to a datetime object and then converts it to a string datetime and then Converts it back to a datatime
            pubDate = datetime.strptime(datetime.strftime(datetime.strptime(shiftcode.get("pubDate"), "%a, %d %b %Y %H:%M:%S %z"), "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            if "Borderlands" in shiftcode.get("archive:shift").get("shift:game") and pubDate > mostRecentStoredCodePublishedDate:
                newCode = True
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
        else:
            self.__send2Telegram__(AWS.getSecret("username_bobby"), "No New Codes")
        
        return newShiftCodes

    def __getStoredCodes__(self):
        # return json.loads(AWS.s3GetObject(BUCKET, KEY))
        with open("./shiftcode.json", "r") as reader:
            return json.loads(reader.read())

    def __writeNewCodes__(self, data):
        # AWS.s3PutObject(bucket=BUCKET, key=KEY, data=data)
        with open("./shiftcode.json", "w+") as writer:
            writer.write(json.dumps(data))

    def send2Telegram(self, group, text):
        """
        sends the message to telegram
        :param group: choose what telegram group to send message to
        :param text: allows you to choose what message to send
        :return: message
        """
        # sends a message to telegram
        return requests.get(f"https://api.telegram.org/bot{self.bot_id}/sendMessage?chat_id={group}=&text={text}")


        # users = ["bobby", "phillip", "hardy"]
        # creds = []
        # for user in users:
        #     creds.append({
        #         "username": AWS.getSecret(f"username_{user}"),
        #         "password": 
        #     })
        
    
def main():
    ShiftCodeScraper()

if __name__ == '__main__':
    main()
    