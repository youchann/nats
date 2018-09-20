from flask import Flask, render_template, redirect, url_for
from requests_oauthlib import OAuth1Session
import natsugash.config as config
import json, urllib, re
import pprint, emoji

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

def get_tweets (name):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {
        'count': 15,
        'screen_name': name,
        'exclude_replies': True,
        'include_rts': False
    }
    res = twitter.get(url, params = params)

    if res.status_code == 200:
        timelines = json.loads(res.text)
        return timelines
    else:
        print('fail to access')
        return redirect(url_for('/'))


def remove_emoji(src_str):
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)

def assort_tweets (timelines):
    tweets = {}

    for line in timelines:
        if line['user']['protected']:
            print(line['user']['protected'])
            render_template('index.html')

        tweet_id = 'voice' + line['id_str']
        text = line['text']
        removed_text_num = len(remove_emoji(text))
        text = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "" ,text)
        if (removed_text_num > 0 and len(text) >= 1 and len(text) <= 139):
            photo_num = 0
            media_type = "none"
            media_src = [""]

            if ('extended_entities' in line):
                for media in line['extended_entities']['media']:
                    if (media['type'] == "photo"):
                        media_type = "photo"
                        photo_num += 1
                        media_src.append(media['media_url'])

                    elif (media['type'] == "video"):
                        pprint.pprint(media)
                        media_type = "video"
                        media_src.append(media['video_info']['variants'][2]['url'])

            tweets[tweet_id] = {
                'text' : text,
                'photo_num' : photo_num,
                'media_type' : media_type,
                'media_src' : media_src,
            }
        continue
    return tweets

# def get_tweets_for_main (name):
#     tweets = assort_tweets (get_tweets (name))
#     return tweets
