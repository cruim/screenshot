import time
import requests
import keyboard
import error_log

APP_STATE = False


def get_app_state():
    try:
        global APP_STATE
        data = ({'token': '348169607'})
        req = requests.post(url='http://cru.im/current-state', json=data)
        responce = req.text
        if responce == 'Bot is off' and not APP_STATE:
            time.sleep(30)
            get_app_state()
        elif responce == 'Bot is on' and not APP_STATE:
            APP_STATE = True
            keyboard.hotkey('ctrlleft', 'l')
        elif responce == 'Bot is off' and APP_STATE:
            APP_STATE = False
            keyboard.hotkey('ctrlleft', 'l')
    except Exception as e:
        error_log.error_log('remote_control', str(e))