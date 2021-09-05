import os, requests,json
from dotenv import load_dotenv
load_dotenv()

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

def slack_notify(text, WEBHOOK_URL = WEBHOOK_URL):
    slack_data = {'text': text}

    response = requests.post(
        WEBHOOK_URL, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    return 0