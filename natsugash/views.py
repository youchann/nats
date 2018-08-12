from flask import request, redirect, url_for, render_template, flash
from natsugash import app
import json, natsugash.config, os
from requests_oauthlib import OAuth1Session

@app.route('/')
def show_index():
    return render_template('index.html')

@app.route('/main')
def show_main():
    return render_template('mainpage.html')

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
