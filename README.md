# Broderlands Shift Code Scraper
Sends Borderlands 3 Shift Codes to the Telegram Client

## Configuration

First install requirements
```bash
pip install -r requirements.txt
```
If Python 2 and 3 installed used `pip3`

Create a telegram bot and create a new telegram group for help reference here:
<https://docs.microsoft.com/en-us/azure/bot-service/bot-service-channel-connect-telegram?view=azure-bot-service-4.0>

Add the group id to your `.env` file as following:

* `BORDERLANDS_BOT` = Your main group id where you want to send your codes to
* `TEST`            = Optional (used for testing)

## Maintatiners
Robert Kuhlke <bkuhlke@yahoo.com>