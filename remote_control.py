import time
import requests
import keyboard

APP_STATE = False


def get_app_state():
    global APP_STATE
    data = ({'token': '348169607'})
    req = requests.post(url='http://cru.im/current-state', json=data)
    if req.text == 'Bot is off' and not APP_STATE:
        time.sleep(10)
        get_app_state()
    elif req.text == 'Bot is on' and not APP_STATE:
        APP_STATE = True
        keyboard.press('p')
    elif req.text == 'Bot is off' and APP_STATE:
        APP_STATE = False
        keyboard.press('p')