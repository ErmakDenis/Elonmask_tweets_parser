import requests
import pandas as pd
import time
from selenium import webdriver
from snscrape.modules import twitter
import binascii
import random
import requests
import pandas as pd
import time
from selenium import webdriver
from funcs import *


# def generate_token(size=16):
#     """Generate a random token with hexadecimal digits"""
#     data = random.getrandbits(size * 8).to_bytes(size, "big")
#     return binascii.hexlify(data).decode()
#
# csrf_token = generate_token()
#
# # twitter.GuestTokenManager
# #
# # X_Csrf_Token = "a37421a1ca6b6ba184403199509ea09d"
# headers = {
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cs;q=0.6",
#     "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
#     "Referer": "https://twitter.com/elonmusk",
#     "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": "\"macOS\"",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-origin",
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "X-Twitter-Active-User": "yes",
#     # "X-Csrf-Token": X_Csrf_Token,
#     "X-Twitter-Client-Language": "ru"
# }
#
# r = requests.post('https://api.twitter.com/1.1/guest/activate.json',headers=headers)
# # r = requests.post('https://twitter.com/i/csp_report?a=O5RXE%3D%3D%3D&ro=false',headers=headers)
#
# print(r.status_code)
# cookies = r.cookies
# # o = r.json()
# # Просмотреть значения cookies
# guest_id_cookie = cookies['guest_id'].split('v1%3A')
# print(guest_id_cookie)
# guest_id = guest_id_cookie[1]
# print(guest_id)
#
# X_Csrf_Token = csrf_token
# X_Guest_Token = guest_id
#
#
# headers = {
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cs;q=0.6",
#     "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
#     "Referer": "https://twitter.com/elonmusk",
#     "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": "\"macOS\"",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-origin",
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "X-Twitter-Active-User": "yes",
#     "X-Csrf-Token": X_Csrf_Token,
#     "X-Guest-Token": X_Guest_Token,
#     "X-Twitter-Client-Language": "ru"
# }
#
# r = requests.post('https://api.twitter.com/1.1/guest/activate.json',headers=headers)
#
# tweetss = get_tweets(X_Csrf_Token=X_Csrf_Token,X_Guest_Token=X_Guest_Token)
# print(tweetss)


#------------------------------------------------------------------------
#  Выше у меня показана попытка достать X_Guest_Token и X_Csrf_Token
# Получилось только получить X_Guest_Token с X_Csrf_Token пока не получилось разобраться
# ------------------------------------------------------------------------

if __name__ == '__main__':
    _X_Guest_Token, _X_Csrf_Token = get_tokens_from_cookies()
    _tweets = get_tweets(_X_Guest_Token, _X_Csrf_Token)
    write_in_logs(_tweets)
