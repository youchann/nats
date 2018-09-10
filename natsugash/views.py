from flask import request, redirect, url_for, render_template, flash
from natsugash import app, getTwitter, voicetext
import os, glob


# Root
@app.route('/')
def show_index():
    print('index', glob.glob('natsugash/static/voicefiles/*.wav'))

    return render_template('index.html', title="nats_gash")


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
            
    tweets = getTwitter.get_tweets_for_main(name)
    voicetext.make_voicefile(tweets)
    print(glob.glob('natsugash/static/voicefiles/*.wav'))
    return render_template('mainpage.html', tweets=tweets, title="mainpage")

# To Score
@app.route('/score')
def show_score():
    return render_template('score.html')


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
