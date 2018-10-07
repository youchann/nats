from flask import request, redirect, url_for, render_template, flash, session
from natsugash import app, getTwitter, voicetext
import natsugash.config as config
import os
import glob
import pyrebase

firebase = pyrebase.initialize_app(config.FIREBASE_CONFIG)
db = firebase.database()
app.secret_key = '09u34gqoijalkefeqwjio4'

# Root
@app.route('/')
def show_index():

    if (glob.glob('natsugash/static/voicefiles/*.wav')):
        voicefiles = glob.glob('natsugash/static/voicefiles/*.wav')
        for voicefile in voicefiles:
            os.remove(voicefile)

    oauth_url = getTwitter.oath_twitter()
    return render_template('oauth.html', title="認証", oauth_url=oauth_url)


@app.route('/paci')
def show_paci():
    access_token = getTwitter.get_access_token()
    session['access_token'] = access_token

    if session.get('access_token'):
        getTweets = getTwitter.get_tweets(session.get('access_token'))
        if getTweets:
            tweets = getTwitter.assort_tweets(getTweets)
            session['tweets'] = tweets
            return render_template('mainpage.html', tweets=tweets, title="ついーとぱっく")
        else:
            return render_template('errorpage.html')
    else:
        return render_template('errorpage.html')

# select
@app.route('/selectTweets', methods=['POST'])
def show_select_tweets():
    if request.method == 'POST':
        delTweets = {}
        selectTweets = request.form.getlist('select_tweets')
        for k, v in session['tweets'].items():
            if v['id'] in selectTweets:
                delTweets[k] = v
        session['delTweets'] = delTweets
    return render_template('selectTweets.html', delTweets=delTweets)

# delpac
@app.route('/delpac')
def show_del_tweets():
    voiceTweets = {}
    delTweets = session.get('delTweets')
    getTwitter.del_tweets(delTweets, session['access_token'])

    for k, v in delTweets.items():
        voiceTweets[k] = v

    db.child("tweets").push(delTweets)
    session.pop('delTweets', None)
    session.pop('access_token', None)
    session.pop('tweets', None)
    return render_template('delpac.html')

# cssがキャッシュから読まれない為の関数

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
