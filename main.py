"""
Borderlands Web Scraper
"""
import csv
import requests
from bs4 import BeautifulSoup as bs

BRODERLANDS_BOT = -296659970
TEST = -380161856


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
    grabs shift code and returns the code
    :return: code
    """

    # Parses through the description and pulls out
    # necessary information needed to send the message
    des = build_soup().item.description.text.split('<br>')
    des_list = []

    for item in des:
        des_list.append(item)

    # grabs info from the description from web page
    code = des_list[3].split(':')
    game_or_type = des_list[0].split(':')
    reward = des_list[1].split(':')

    # if the type is a vip code returns vip code
    if game_or_type[1] == ' Borderlands 3':
        string = f'{code[1]}'
        return string

    # if the type is a vip code returns vip code
    elif game_or_type[1] == ' VIP Vault':
        string = f'New VIP Code!!!\nReward: {reward[1]}'
        return string

    return ''


def description():
    """
    grabs the description of the shift code
    :return: string
    """
    # Parses through the description and pulls out
    # necessary information needed to send the message
    des = build_soup().item.description.text.split('<br>')
    des_list = []
    for item in des:
        des_list.append(item)

    # grabs info from the description from web page
    expires = des_list[5].split(':', 1)
    shift_code_reward = des_list[2].split(':')
    vip_code_reward = des_list[1].split(':')
    game_or_type = des_list[0].split(':')

    # if the type is a shift code returns a shift code description
    if game_or_type[1] == ' Borderlands 3':
        string = f'New Shift Code!!!\nReward: {shift_code_reward[1]}\n'\
            f'Expires: {expires[1]}\nShift Code: '
        return string

    # if the type is a vip code returns vip code description
    elif game_or_type[1] == ' VIP Vault':
        string = f'New VIP Code!!!\nReward: {vip_code_reward[1]}'
        return string

    return ''


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
    main functionality
    :return: None
    """
    text = description()
    code = shift_code()
    with open('shiftcode.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for rows in csv_reader:
            csvfile.readlines()
            if rows[0].strip() == code.strip():
                break
            if rows[0].strip() != code:
                send_to_telegram(BRODERLANDS_BOT, text)
                send_to_telegram(BRODERLANDS_BOT, code)
                with open('shiftcode.csv', 'w') as csv_writer:
                    rows[0] = csv_writer.write(code.strip())
                    break


if __name__ == '__main__':
    main()
