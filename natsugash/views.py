from flask import request, redirect, url_for, render_template, flash, session
from natsugash import app, getTwitter, voicetext
import os, glob


app.secret_key = 'secretkeypacpac'

# Root
@app.route('/')
def show_index():

    if (glob.glob('natsugash/static/voicefiles/*.wav')):
        voicefiles = glob.glob('natsugash/static/voicefiles/*.wav')
        for voicefile in voicefiles:
            os.remove(voicefile)

    oauth_url = getTwitter.oath_twitter()
    return render_template('oauth.html', title="認証", oauth_url = oauth_url)

@app.route('/paci')
def show_paci():
    access_token = getTwitter.get_access_token()
    if access_token:
        session['access_token'] = access_token
        getTweets = getTwitter.get_tweets(access_token)
        if getTweets:
            tweets = getTwitter.assort_tweets(getTweets)
            session['tweets'] = tweets
            return render_template('mainpage.html', tweets=tweets, title="ついーとぱっく")
        else:
            return render_template('errorpage.html')
    else:
        return render_template('errorpage.html')

# delpac
@app.route('/delpac', methods=['POST'])
def show_del_tweets():
    if request.method == 'POST':
        voiceTweets = {}
        delTweets = request.form.getlist('delTweets')
        getTwitter.del_tweets(delTweets, session['access_token'])
        for k, v in session['tweets'].items():
            if v['id'] in delTweets:
                voiceTweets[k] = v
        print(voiceTweets)
        voicetext.make_voicefile(voiceTweets)

    return render_template('delpac.html', delTweets=voiceTweets)


# To Main
@app.route('/main', methods=['POST'])
def show_main():
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = 'no name'

    if (glob.glob('natsugash/static/voicefiles/*.wav')):
        voicefiles = glob.glob('natsugash/static/voicefiles/*.wav')
        for voicefile in voicefiles:
            os.remove(voicefile)

    getTweets = getTwitter.get_tweets(name)

    if getTweets:
        tweets = getTwitter.assort_tweets(getTweets)
        voicetext.make_voicefile(tweets)
        return render_template('mainpage.html', tweets=tweets, title="ついーとぱっく")
    else:
        return render_template('errorpage.html')


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
