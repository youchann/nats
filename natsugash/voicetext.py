import natsugash.config as config
import os.path, re

API_KEY = config.VOICETEXT_API_KEY

def make_voicefile (tweets) :
    for k, v in tweets.items():
        # text = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "" ,v['text'])

        p = "curl 'https://api.voicetext.jp/v1/tts' \
            -o 'natsugash/static/voicefiles/{0}.wav' \
            -d 'text={1}' \
            -u '{2}:' \
            -d 'speed=130' \
            -d 'speaker=hikari'".format(k, v['text'], API_KEY)
        os.system(p)
