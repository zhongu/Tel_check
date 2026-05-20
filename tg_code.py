import base64
import json
import os

import requests

CAPTCHA_TIMEOUT = 20


def truecaptcha():
    print("[captcha] reading 1.jpg", flush=True)
    with open("1.jpg", "rb") as f:
        image_base64 = base64.b64encode(f.read())

    try:
        url = "https://api.apitruecaptcha.org/one/gettext"
        data = {
            "userid": os.environ["TRUECAPTCHA_USERID"],
            "apikey": os.environ["TRUECAPTCHA_APIKEY"],
            "data": str(image_base64, encoding="utf-8"),
        }
        print("[captcha] sending request to TrueCaptcha", flush=True)
        res = requests.post(url, data=json.dumps(data), timeout=CAPTCHA_TIMEOUT).text
        res = json.loads(res)
        res = res["result"]
        print("[captcha] result: {}".format(res), flush=True)
    except Exception as exc:
        print("[captcha] failed: {}: {}".format(type(exc).__name__, exc), flush=True)
        res = "failed"
    return res
