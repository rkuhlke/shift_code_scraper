"""
Borderlands Web Scraper
"""
import json
from upload_to_shift import Upload2Shift
from shiftCodeScraper import ShiftCodeScraper
from utilities.aws.aws import AWS
from utilities.messaging.telegram import TelegramBots


def upload2Shift(secrets, codes):
    users = ["bobby", "philip", "hardy"]
    for user in users:
        srv = Upload2Shift(secrets.get(f"username_{user}"), secrets.get(f"password_{user}"))
        for code in codes:
            srv.uploadCode(code.get("Code"))
            msg = f"New Reward For {code.get('Game')}\n{code.get('Reward')}\nThis has been successfully uploaded to your account for all linked borderlands accounts"
            TelegramBots.send2Telegram(secrets.get("bot_id"), secrets.get(f"telegram_id_{user}"), msg)
    return

def sendCodes(secrets, codes):
    for code in codes:
        descriptionMsg = f"New {code.get('Game')} Code!\n\n Platform: {code.get('Platform')}\nReward: {code.get('Reward')}\nExpires: {code.get('Expires')}"
        TelegramBots.send2Telegram(secrets.get("bot_id"), secrets.get("telegram_id_borderlands"), descriptionMsg)
        TelegramBots.send2Telegram(secrets.get("bot_id"), secrets.get("telegram_id_borderlands"), code.get("Code"))

def main(event, context):
    secrets = AWS.getSecret("shift_code_scraper_secrets")
    codes = ShiftCodeScraper(secrets).shiftCodeScraper()
    if codes:
        upload2Shift(secrets, codes)
        sendCodes(secrets, codes)
    return
