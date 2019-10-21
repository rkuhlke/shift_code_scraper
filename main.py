"""
Borderlands Web Scraper
"""
import requests
import time

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
    :TODO: compare old shift code to new shift code
    :return: string
    """
    code = build_soup().item.title.text

    return code


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
    des_type = des_list[0].split(':')
    expires = des_list[6].split(':', 1)
    expire_time = expires[1].split('T')
    exact_time = expire_time[1].split('-')
    reward = des_list[1].split(':')
    game = des_list[2].split(':')

    # if the type is a shift code returns a shift code description
    if des_type[1] == ' SHiFT Code' and game[1] == ' Borderlands 3':
        string = f'New Shift Code!!!\nReward: {reward[1]}'\
            f'Expires: {expire_time[0]} at {exact_time[0]}\nShift Code: '
        return string

    # if the type is a vip code returns vip code description
    elif des_type[1] == ' VIP Code':
        string = f'New VIP Code!!!\nReward: {reward[1]}'
        return string

    return ''


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

    compare_list = [1]

    # runs infinitely if codes are the same
    while True:
        # grabs code and puts it into a list
        code_list = [code]

        # if code is ever different
        # new code will be sent to telegram
        if code_list != compare_list:
            send_to_telegram(TEST, text)
            send_to_telegram(TEST, code_list[0])

            # this makes it so the two lists become the same
            compare_list[0] = code_list[0]

            # reruns the program to see if anything updates
            shift_code()
        else:
            print('hi')
            # waits an hour before running again
            time.sleep(3600)

            # continues the loop
            continue


if __name__ == '__main__':
    main()
