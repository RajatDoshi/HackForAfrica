import os, requests, uuid, json

endpoint = 'https://api.cognitive.microsofttranslator.com/'
subscription_key = '6ae6871172f54a368b3515a709e3fa0c'
location = 'canadacentral'

#Afrikaans = "af"
#Swahili = "sw"
#French = "fr"

def get_translation(text_input, language_output):
    base_url = endpoint
    path = '/translate?api-version=3.0'
    params = '&to=' + language_output
    constructed_url = base_url + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text' : text_input
    }]
    response = requests.post(constructed_url, headers=headers, json=body)
    output = response.json()
    return output[0]['translations'][0]['text']

