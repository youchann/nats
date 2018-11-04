from flask import Flask, render_template, redirect, url_for, request, session
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
import json, urllib, re, pprint, emoji
import natsugash.config as config
import collections as cl

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
oauth_callback = config.OAUTH_CALLBACK_LOCAL

def oath_twitter ():
    session.clear()
    twitter = OAuth1Session(CK, CS)
    res = twitter.post(
        'https://api.twitter.com/oauth/request_token',
        params={'oauth_callback': oauth_callback}
    )
    if res.status_code == 200:
        request_token = dict(parse_qsl(res.content.decode("utf-8")))
        authenticate_url = "https://api.twitter.com/oauth/authorize"
        authenticate_endpoint = '%s?oauth_token=%s' % (authenticate_url, request_token['oauth_token'])
        return authenticate_endpoint
    else:
        return False

def get_access_token ():
    if request.args.get('oauth_token') and request.args.get('oauth_verifier'):
        oauth_token = request.args.get('oauth_token')
        oauth_verifier = request.args.get('oauth_verifier')
        twitter = OAuth1Session(
            CK,
            CS,
            oauth_token,
            oauth_verifier,
        )

        response = twitter.post(
            'https://api.twitter.com/oauth/access_token',
            params={'oauth_verifier': oauth_verifier}
        )

        access_token = dict(parse_qsl(response.content.decode("utf-8")))
        return access_token
    else:
        return False

def get_tweets (access_token):
    twitter = OAuth1Session(
        CK,
        CS,
        access_token['oauth_token'],
        access_token['oauth_token_secret']
    )

    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {
        'count': 100,
        'exclude_replies': False,
        'include_rts': False
    }
    res = twitter.get(url, params = params)

    if res.status_code == 200:
        timelines = json.loads(res.text)
        return timelines
    elif res.status_code == 404:
        return False

def del_tweets (delTweets, access_token):
    twitter = OAuth1Session(
        CK,
        CS,
        access_token['oauth_token'],
        access_token['oauth_token_secret']
    )
    for k,v in delTweets.items():
        twitter.post("https://api.twitter.com/1.1/statuses/destroy/{0}.json".format(k))


# def remove_emoji(src_str):
#     return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)

def assort_tweets (timelines):
    tweets = cl.OrderedDict()
    for line in timelines:
        tweet_id = line['id_str']
        text = line['text']
        # removed_emoji_text = remove_emoji(text)
        text = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "" ,text)
        if (len(text) >= 1 and len(text) <= 139):
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
                        media_type = "video"
                        media_src.append(media['video_info']['variants'][0]['url'])

            tweets[tweet_id] = {
                'text' : text,
                'photo_num' : photo_num,
                'media_type' : media_type,
                'media_src' : media_src,
            }
        else:
            continue
    return tweets
