from flask import request, redirect, url_for, render_template, flash, session
from natsugash import app, getTwitter
import natsugash.config as config
import os, pyrebase, json, pprint
import collections as cl

firebase = pyrebase.initialize_app(config.FIREBASE_CONFIG)
db = firebase.database()
app.secret_key = config.SECRET_KEY

# Root
@app.route('/')
def show_index():
    if os.path.isfile('assorted_tweets'):
        os.remove('assorted_tweets.json')
    oauth_url = getTwitter.oath_twitter()
    if oauth_url:
        return render_template('oauth.html', title="ツイートパック", oauth_url=oauth_url)
    else:
        return render_template('errorpage.html', title="エラーページ")


@app.route('/paci')
def show_paci():
    access_token = getTwitter.get_access_token()
    if not session.get('access_token'):
        session['access_token'] = access_token
    if session.get('access_token'):
        getTweets = getTwitter.get_tweets(session.get('access_token'))
        if getTweets:
            tweets = getTwitter.assort_tweets(getTweets)
            fw = open('assorted_tweets.json','w')
            json.dump(tweets,fw,indent=2)
            return render_template('mainpage.html', tweets=tweets, title="ついーとぱっく")
        else:
            return render_template('errorpage.html')
    else:
        return render_template('errorpage.html')

# select
@app.route('/selectTweets', methods=["POST"])
def show_select_tweets():
    tweets = cl.OrderedDict()
    delTweets = cl.OrderedDict()
    selectTweetsList = request.form.getlist('select_tweets')

    with open('assorted_tweets.json') as f:
        tweets = json.load(f)

    for k, v in tweets.items():
        if k in selectTweetsList:
            delTweets[k] = v
    session['delTweets'] = delTweets
    return render_template('selectTweets.html', delTweets=delTweets)

# delpac
@app.route('/delpac')
def show_del_tweets():
    delTweets = session.get('delTweets')
    getTwitter.del_tweets(delTweets, session['access_token'])

    db.child("tweets").push(delTweets)
    session.clear()
    return render_template('delpac.html')


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
