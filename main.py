"""
Borderlands Web Scraper
"""
import requests
import urllib

from bs4 import BeautifulSoup as bs


def code_parser():
    get_page = requests.get('https://shift.orcicorn.com/shift-code/')
    soup = bs(get_page.text, 'html.parser')

    shift_list = []
    for code in soup.find_all('article'):
        code.get('href')
        shift = code.text.split('\n')
        shift_list.append({
            'Code': shift[0],
            'Date': shift[1]
        })
    return shift_list


def send_to_telegram():
    code = requests.get('https://api.telegram.org/bot924108836:AAHZykalHR8INIwplZERIwibUtDnUUdQN-8/'
                        'sendMessage?chat_id=-296659970&text={}'.format(code_parser()))
    return code


def main():
    send_to_telegram()


if __name__ == '__main__':
    main()



