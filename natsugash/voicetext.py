import natsugash.config as config
import os.path

API_KEY = config.VOICETEXT_API_KEY

def make_voicefile (tweets) :
    for tweet in tweets:
        print(tweet)
        # p = "curl 'https://api.voicetext.jp/v1/tts' \
        #     -o 'natsugash/voicefiles/{0}.wav' \
        #     -u '{1}:' \
        #     -d 'text={0}' \
        #     -d 'speaker=hikari'".format(tweet, API_KEY)
        # os.system(p)
