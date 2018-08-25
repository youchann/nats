from flask import request, redirect, url_for, render_template, flash
from requests_oauthlib import OAuth1Session
from natsugash import app
import natsugash.config as config
import json, os

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

@app.route('/')
def show_index():
    return render_template('index.html', title="nats_gash")

@app.route('/main', methods=['POST'])
def show_main():
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = 'no name'

    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {
        'count': 30,
        'screen_name': name,
        'exclude_replies': True,
        'include_rts': False
    }
    res = twitter.get(url, params = params)
    timelines = json.loads(res.text)
    tweets = []
    for line in timelines:
        text = line['text']
        tweets.append(text)
    return render_template('mainpage.html', tweets=tweets, title="mainpage")

@app.route('/score')
def show_score():
    return render_template('score.html')

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
