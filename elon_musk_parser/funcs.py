
import requests
import pandas as pd
import time
from selenium import webdriver

# Не использовал проксирования тк денег нет
def get_tokens_from_cookies():
    print('Получение токенов')
    X_Csrf_Token = ''  # "a37421a1ca6b6ba184403199509ea09d"
    X_Guest_Token = ''  # "1671486568211554304"

    # Настройки для Chrome
    options = webdriver.ChromeOptions()

    # Указываем путь к исполняемому файлу драйвера Chrome и передаем настройки
    driver = webdriver.Chrome(
        executable_path='/usr/local/bin/chromedriver',
        options=options
    )

    # Перейти на веб-сайт
    driver.get("https://twitter.com")

    # Получение всех cookie
    # Из куки надо вытащить  X_Guest_Token и X_Csrf_Token
    cookies = driver.get_cookies()

    # Вывод содержимого всех cookie
    for cookie in cookies:
        if cookie['name'] == 'gt':
            # print('gt ',cookie['value'])
            X_Guest_Token = str(cookie['value'])
        if cookie['name'] == 'ct0':
            # print('ct0 ',cookie['value'])
            X_Csrf_Token = str(cookie['value'])

    # Закрытие браузера
    driver.quit()

    return X_Guest_Token, X_Csrf_Token


def get_tweets(X_Guest_Token, X_Csrf_Token):
    print('Идет анализ твиттов')
    url = "https://twitter.com/i/api/graphql/Uuw5X2n3tuGE_SatnXUqLA/" \
          "UserTweets?variables=%7B%22userId%22%3A%2244196397%22%2C%22count" \
          "%22%3A20%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromote" \
          "EligibilityTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2" \
          "Timeline%22%3Atrue%7D&features=%7B%22rweb_lists_timeline_redesign_enabled" \
          "%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue" \
          "%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_t" \
          "weet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_na" \
          "vigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_ima" \
          "ge_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled" \
          "%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_" \
          "translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_every" \
          "where_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%" \
          "2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_f" \
          "etch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visi" \
          "bility_results_prefer_gql_limited_actions_policy_enabled%22%3Afalse%2C%22longform_notetwe" \
          "ets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%2" \
          "2%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cs;q=0.6",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "Referer": "https://twitter.com/elonmusk",
        "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Csrf-Token": X_Csrf_Token,
        "X-Guest-Token": X_Guest_Token,
        "X-Twitter-Active-User": "yes",
        "X-Twitter-Client-Language": "ru"
    }
    try:
        # Отправляем запрос
        response = requests.get(url, headers=headers)
        print('status: ',response.status_code)
        if response.status_code == 200:
            is_ok = True
        else:
            is_ok = False
        content = response.json()
        data = pd.DataFrame(content)

    except Exception as ex:
        print(ex)
        print('Следует поменять X_Csrf_Token и X_Guest_Token')

    if is_ok:
        tweets = []
        try:
            tmp = data['data']['user']['result']["timeline_v2"]['timeline']["instructions"][1]['entries']
        except Exception as ex:
            print(ex)
            print('Не получилось проанализировать твиты')

        for i in tmp:

            try:
                tweet = i['content']['itemContent']['tweet_results']['result']['legacy']['full_text']
                retweeted = False
                tweet_user_id = 'elonmusk'
                if tweet[0] == 'R' and tweet[1] == 'T' and tweet[3] == '@':
                    retweeted = True
                    tmp = tweet.split(' @')
                    tmp = tmp[1].split(':')
                    tweet_user_id = tmp[0]

                conversation_id = i['content']['itemContent']['tweet_results']['result']['legacy'][
                    'conversation_id_str']
                logs = {'tweet': tweet, 'conversation_id': conversation_id, "tweet_user_id": tweet_user_id,
                        'retweeted': retweeted, 'users_commented': []}
                tweets.append(logs)

            except Exception as ex:
                print(ex)

        for a in tweets:
            time.sleep(2)
            tweet_id = a['conversation_id']
            tweet_user_id = a['tweet_user_id']

            url2 = f"https://twitter.com/i/api/graphql/VWFGPVAGkZMGRKGe3GFFnA/" \
                   f"TweetDetail?variables=%7B%22focalTweetId%22%3A%22{tweet_id}" \
                   f"%22%2C%22referrer%22%3A%22profile%22%2C%22rux_context%22%3A%" \
                   f"22HHwWgIC-oYrQ7rEuAAAA%22%2C%22with_rux_injections%22%3Atrue%" \
                   f"2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3A" \
                   f"true%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%2" \
                   f"2withBirdwatchNotes%22%3Afalse%2C%22withVoice%22%3Atrue%2C%22wit" \
                   f"hV2Timeline%22%3Atrue%7D&features=%7B%22rweb_lists_timeline_redes" \
                   f"ign_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directiv" \
                   f"e_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C" \
                   f"%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22r" \
                   f"esponsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22resp" \
                   f"onsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afal" \
                   f"se%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22respons" \
                   f"ive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_" \
                   f"rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywher" \
                   f"e_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22" \
                   f"%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_o" \
                   f"f_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_mis" \
                   f"info%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_ac" \
                   f"tions_policy_enabled%22%3Afalse%2C%22longform_notetweets_rich_text_read" \
                   f"_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3At" \
                   f"rue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
            headers2 = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cs;q=0.6",
                "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                "Referer": f"https://twitter.com/{tweet_user_id}/status/{tweet_id}?cxt=HHwWgMDSme_Ngq8uAAAA",
                # ?cxt=HHwWgMDSme_Ngq8uAAAA
                "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "\"macOS\"",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "X-Csrf-Token": X_Csrf_Token,
                "X-Guest-Token": X_Guest_Token,
                "X-Twitter-Active-User": "yes",
                "X-Twitter-Client-Language": "ru"
            }

            # Отправляем запрос
            response2 = requests.get(url2, headers=headers2)
            # print(response2)
            content2 = response2.json()
            data2 = pd.DataFrame(content2)

            try:
                users = []
                try:
                    data2 = data2['data']["threaded_conversation_with_injections_v2"]['instructions'][0]['entries']
                except Exception as ex:
                    print(ex)
                    print('Ошибка в получении данных в реплаях на твит, проверь состояние запроса')
                # print(data2)
                for i in data2:
                    try:
                        user = \
                            i['content']['items'][0]['item']['itemContent']['tweet_results']['result']['core'][
                                'user_results'][
                                'result']['legacy']['screen_name']
                        # print(user)
                        if len(users) < 3:
                            users.append(user)
                        else:
                            break

                    except:
                        pass
                a['users_commented'] = users
            except Exception as ex:
                print(ex)

    return tweets


def write_in_logs(tweets):
    # Открываем файл для записи (если файл не существует, он будет создан)
    file = open("logs.txt", "w")

    count = 1
    for i in tweets:
        text_with_users = ''
        if not i['retweeted']:
            for user in i['users_commented']:
                text_with_users += 'https://twitter.com/' + user + '\n'
            # Записываем данные в файл
            text = i['tweet']
            file.write(f'{count}) {text} \nCommented by:\n{text_with_users}\n')
        else:
            text = i['tweet']
            file.write(f'{count}) {text}\n')
        count += 1
        if count == 11:
            break

    # Закрываем файл
    file.close()
