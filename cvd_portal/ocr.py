import sys
import requests
import os
from dhadkan.settings import BASE_DIR

def ocr_space_file(filename, overlay=True, api_key='helloworld', language='eng'):


    payload = {
               'apikey': '3047397b1388957',
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    test_file =  r.json()

    return test_file['ParsedResults'][0]['ParsedText'].replace("\r", "").split("\n")

def ocr_space_file_():
    data = ocr_space_file(filename = os.path.join(BASE_DIR, "photo.jpeg"))
    return data


