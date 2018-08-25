import os.path

API_KEY = "13j7vr127iem66cw"
text = "斎藤そうまは、良いぞ。"
# p = "curl 'https://api.voicetext.jp/v1/tts' \
#      -o 'test.wav' \
#      -u '％s:' \
#      -d 'text=斎藤そうまは、良いぞ' \
#      -d 'speaker=hikari'" % API_KEY

p = "curl 'https://api.voicetext.jp/v1/tts' \
    -o 'test.wav' \
    -u '{0}:' \
    -d 'text={1}' \
    -d 'speaker=hikari'".format(API_KEY, text)

os.system(p)
