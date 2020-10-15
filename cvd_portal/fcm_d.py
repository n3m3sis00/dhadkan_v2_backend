import requests
# import os
import json
import firebase_admin
from firebase_admin import credentials
from oauth2client.service_account import ServiceAccountCredentials


url = 'https://fcm.googleapis.com/v1/projects/my-dhadkan/messages:send'
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

def _get_access_token():
    """Retrieve a valid access token that can be used to authorize requests.

        :return: Access token.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
                          '/app/cvd_portal/my-dhadkan-firebase.json', SCOPES)
    access_token_info = credentials.get_access_token()
    return access_token_info.access_token

def send_message(_to, _from, message):
    body = {"message":{'token': _to, 'notification': {"title":"Dhadkan", "body": message}}}
    body = json.dumps(body).encode('utf8')
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + _get_access_token()
        }
    r = requests.post(url, data=body, headers=headers)
    print(r.text)

    return "Message Sent"




