import os.path

API_KEY = "13j7vr127iem66cw"
# text = 'きみがよ'

p = "curl 'https://api.voicetext.jp/v1/tts' \
     -o 'test.wav' \
     -u '{API_KEY}:' \
     -d 'text=さいとうそうまはよいぞ' \
     -d 'speaker=hikari'"
req = os.system(p)
print(req)
