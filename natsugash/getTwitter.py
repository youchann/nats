from requests_oauthlib import OAuth1Session
import natsugash.config as config
import json, urllib

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

def get_tweets (name):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {
        'count': 20,
        'screen_name': name,
        'exclude_replies': True,
        'include_rts': False
    }
    res = twitter.get(url, params = params)
    timelines = json.loads(res.text)
    return timelines

def assort_tweets (timelines):
    tweets = {}
    for line in timelines:
        text = line['text']
        if (text.find('https') != -1):
            text = text[:text.find('https')]
        try:
            image = line['extended_entities']['media'][0]['media_url']
            tweets[text] = image
        except KeyError:
            tweets[text] = "画像なしツイート"

    return tweets

def get_tweets_for_main (name):
    tweets = assort_tweets (get_tweets (name))
    return tweets
