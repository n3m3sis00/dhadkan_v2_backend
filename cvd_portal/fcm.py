import requests
# import os
import json

url = 'https://fcm.googleapis.com/fcm/send'


def send_message(_to, _from, message):
    body = {'to': _to, 'data': {"message": message}}
    body = json.dumps(body).encode('utf8')
    headers = {
        'content-type': 'application/json',
        'Authorization': 'key=' + 'AAAAQkMDkEA:APA91bFDkuxSwOQIKmr95_vhWwkpwO5SX4jlSUWaKTY3gxUMiT5qxN4-saBZYd-rWZL5UmNj8tl7vN9yKq32sMVzqOoRbAQUJV1xdUHllpM41JRHOpDPnRJkg-7dFpH6ZpqqaC9mwgas'
        }
    r = requests.post(url, data=body, headers=headers)
    print(r.text)
