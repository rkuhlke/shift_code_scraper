"""
Borderlands Web Scraper
"""
import requests

from bs4 import BeautifulSoup as bs

BRODERLANDS_BOT = -296659970
TEST = -380161856
BOT_ID = '924108836:AAHZykalHR8INIwplZERIwibUtDnUUdQN-8'


# def date():
#     x = datetime.today()
#     return x.strftime("%a, %d %b %Y")


def build_soup():
    """
    builds the html parser
    :return: soup
    """
    get_page = requests.get('https://shift.orcicorn.com/index.xml')
    soup = bs(get_page.text, 'html.parser')

    return soup


def shift_code():
    """
    grabs the shift code
    :TODO: compare old shift code to new shift code
    :return: string
    """
    # send = False
    # compare_list = []

    code = build_soup().item.title.text

    return code


def description():
    """
    grabs the description of the shift code
    :return: string
    """
    # if code returns true then description will be sent
    # if shift_code():

    des = build_soup().item.description.text.split('<br>')
    des_list = []

    # Parses through the description and pulls out
    # necessary information needed to send the message
    for item in des:
        des_list.append(item)
    note = des_list[-1].split(':')
    reward = des_list[1].split(':')
    game = des_list[2].split(':')

    string = f'Game: {game[1]}\nReward: {reward[1]}\nNote: {note[1]}'

    return string


def send_to_telegram(group, text):
    """
    sends the message to telegram
    :param group: choose what telegram group to send message to
    :param text: allows you to choose what message to send
    :return: message
    """
    message = requests.get(
        'https://api.telegram.org/bot924108836:AAHZykalHR8INIwplZERIwibUtDnUUdQN-8/'
        f'sendMessage?chat_id={group}'
        '=&text={}'.format(text)
    )

    return message


def main():
    """
    main functionality
    :return: None
    """
    text = description()
    code = shift_code()

    _code = send_to_telegram(TEST, code)
    _description = send_to_telegram(TEST, text)


if __name__ == '__main__':
    main()
