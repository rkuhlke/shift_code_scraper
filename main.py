"""
Borderlands Web Scraper
"""
import requests

from bs4 import BeautifulSoup as bs

BRODERLANDS_BOT = -296659970
TEST = -380161856


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
    :return: string
    """
    compare_list = []

    code = build_soup().item.title.text

    return code


def description():
    """
    grabs the description of the shift code
    :return: list
    """

    des_list = []
    des = build_soup().item.description.text.split('<br>')
    for item in des:
        des_list.append(item)
    note = des_list[-1].split(':')
    reward = des_list[1].split(':')
    game = des_list[2].split(':')

    string = f'Game: {game[1]}\nReward: {reward[1]}\nNote: {note[1]}'

    return string


def send_to_telegram(group, text):
    code = requests.get('https://api.telegram.org/bot924108836:'
                        'AAHZykalHR8INIwplZERIwibUtDnUUdQN-8/'
                        f'sendMessage?chat_id={group}'
                        '=&text={}'.format(text))
    return code


def main():
    text = description()
    code = shift_code()

    _code = send_to_telegram(TEST, code)
    _description = send_to_telegram(TEST, text)


if __name__ == '__main__':
    main()



