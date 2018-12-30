import json
import requests
from wxpy import *
bot = Bot(cache_path=True)

def auto_reply(text):
    url = "http://www.tuling123.com/openapi/api"
    api_key = "9d602fe417464cd18beb2083d064bee6"
    payload = {
        "key": api_key,
        "info": text,
    }
    r = requests.post(url, data=json.dumps(payload))
    result = json.loads(r.text)
    return "[不是本人] " + result["text"]


@bot.register()
def forward_message(msg):
    return auto_reply(msg.text)

embed()