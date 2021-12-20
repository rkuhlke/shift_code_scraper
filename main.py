"""
Borderlands Web Scraper
"""
from upload_to_shift import Upload2Shift
from shiftCodeScraper import ShiftCodeScraper
from utilities.aws.aws import AWS
from utilities.messaging.telegram import TelegramBots


def upload2Shift(secrets, codes):
    users = ["bobby", "hardy", "phillip"]
    for user in users:
        srv = Upload2Shift(secrets.get(f"username_{user}"), secrets.get(f"password_{user}"))
        for code in codes:
            srv.uploadCode(code.get("code"))
            msg = f"New Reward For {code.get('game')}\n{code.get('reward')}\nThis has been successfully uploaded to your account for all linked borderlands accounts"
            TelegramBots().send2Telegram(secrets.get("bot_id"), secrets.get(f"telegram_id_{user}"), msg)
    return

def sendCodes(secrets, codes):
    for code in codes:
        descriptionMsg = f"New {code.get('game')} Code!\n\n Platform: {code.get('platform')}\nReward: {code.get('reward')}\nExpires: {code.get('expires')}"
        TelegramBots().send2Telegram(secrets.get("bot_id"), secrets.get("telegram_id_borderlands"), descriptionMsg)
        TelegramBots().send2Telegram(secrets.get("bot_id"), secrets.get("telegram_id_borderlands"), code.get("code"))
    return

def main(event, context):
    secrets = AWS().secretsManagerGetSecret("shift_code_scraper_secrets")
    codes = ShiftCodeScraper(secrets).shiftCodeScraper()
    if codes:
        upload2Shift(secrets, codes)
        sendCodes(secrets, codes)
    return
