import requests
from urllib.parse import urlparse
from requests.exceptions import HTTPError
import os
from dotenv import load_dotenv
import argparse


def shorten_link(headers, url):
    check_body = requests.get(url)
    check_body.raise_for_status()
    body = {
        "long_url": url,
    }
    
    response = requests.post("https://api-ssl.bitly.com/v4/shorten/", headers=headers, json=body)
    response.raise_for_status()
    return response.json()["id"]


def count_clicks(headers, bitlink):
    bit_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    clicks_count = requests.get(bit_url, headers=headers)
    return clicks_count.json()["total_clicks"]


def is_bitlink(headers, bitlink):
    bit_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    response = requests.get(bit_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    bitly_token = os.environ["BITLY_TOKEN"]
    headers = {
         "Authorization": f"Bearer {bitly_token}",
    }
    parser = argparse.ArgumentParser(description='Сокращает ссылки и выводит количество переходов по ней')
    parser.add_argument('link', help='Введите ссылку:')
    args = parser.parse_args()

    parse_link = urlparse(args.link)
    mybitlink = f"{parse_link.netloc}{parse_link.path}"
    try:
        if is_bitlink(headers, mybitlink):
            print(count_clicks(headers, mybitlink))
        else:
            print(shorten_link(headers, args.link))
    except HTTPError as e:
        print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    main()
