import requests
# import os
import json

url = 'https://fcm.googleapis.com/fcm/send'


def send_message(_to, _from, message):
    body = {'to': _to, 'data': {"message": message}}
    body = json.dumps(body).encode('utf8')
    headers = {
        'content-type': 'application/json',
        'Authorization': 'key=' + 'AAAA39boiz4:APA91bHyAqRkcItZ28W4TGvt3_pO8caR2l8C-0CNTEyTPupShbHvHuQTzEeXgmY8nFm_ET3TlWQpeqyui3TIBg-ObIF0boNaaGv5w55feJCw5avwtdnLIMlGSRD6oOng_1Bd1InaielO'
        }
    r = requests.post(url, data=body, headers=headers)
    print(r.text)
