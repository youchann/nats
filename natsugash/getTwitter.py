from flask import Flask, render_template, redirect, url_for, request, session
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
import natsugash.config as config
import json, urllib, re
import pprint, emoji

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
# AT = config.ACCESS_TOKEN
# ATS = config.ACCESS_TOKEN_SECRET
oauth_callback = config.OAUTH_CALLBACK

tweets = {}

def oath_twitter ():
    session.pop('delTweets', None)
    session.pop('access_token', None)
    session.pop('tweets', None)
    twitter = OAuth1Session(CK, CS)
    response = twitter.post(
        'https://api.twitter.com/oauth/request_token',
        params={'oauth_callback': oauth_callback}
    )
    request_token = dict(parse_qsl(response.content.decode("utf-8")))
    print('request_token', request_token)
    authenticate_url = "https://api.twitter.com/oauth/authorize"
    authenticate_endpoint = '%s?oauth_token=%s' % (authenticate_url, request_token['oauth_token'])
    return authenticate_endpoint

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
        'count': 50,
        'exclude_replies': True,
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
    print('del_tweets', delTweets)
    for k,v in delTweets.items():
        twitter.post("https://api.twitter.com/1.1/statuses/destroy/{0}.json".format(v['id']))


def remove_emoji(src_str):
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)

def assort_tweets (timelines):
    tweets = {}
    for line in timelines:

        tweet_id = line['id_str']
        voice_id = 'voice' + line['id_str']
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
                        media_type = "video"
                        media_src.append(media['video_info']['variants'][0]['url'])

            tweets[voice_id] = {
                'id': tweet_id,
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
