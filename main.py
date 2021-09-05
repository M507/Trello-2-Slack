import os, json, requests
from dotenv import load_dotenv
load_dotenv()

# Required tokens
ROOT_DIR = os.environ.get('ROOT_DIR')
TRELLO_APP_TOKEN = os.environ.get('TRELLO_APP_TOKEN')
TRELLO_APP_KEY = os.environ.get('TRELLO_APP_KEY')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
TODAYS_LIST_ID = os.environ.get('TODAYS_LIST_ID') 

"""
If you don't know the ID of your "today's list", use the listed functions below. 
"""

TRELLO_APP_USERNAME = os.environ.get('TRELLO_APP_USERNAME')
COMPLETED_LIST_ID = os.environ.get('COMPLETED_LIST_ID')
BOARD_ID = os.environ.get('BOARD_ID')

from slack import * 

def get_member():
    url = f"https://api.trello.com/1/members/{TRELLO_APP_USERNAME}"
    querystring = {"key": TRELLO_APP_KEY, "token": TRELLO_APP_TOKEN}
    response = requests.request("GET", url, params=querystring)
    data = json.loads(response.text)
    return(data)

def get_member_id():
    data = get_member()
    return(data['id'])

def get_all_boards(USER_ID):
    url = f"https://api.trello.com/1/members/{USER_ID}/boards"
    querystring = {"key": TRELLO_APP_KEY, "token": TRELLO_APP_TOKEN}
    response = requests.request("GET", url, params=querystring)
    data = json.loads(response.text)
    return data

def get_all_lists_in_board(BOARD_ID):
    url = f"https://api.trello.com/1/boards/{BOARD_ID}/lists"
    querystring = {"key": TRELLO_APP_KEY, "token": TRELLO_APP_TOKEN}
    response = requests.request("GET", url, params=querystring)
    data = json.loads(response.text)
    return(data)

def get_cards_in_list(ID):
    url = f"https://api.trello.com/1/lists/{ID}/cards"
    querystring = {"key": TRELLO_APP_KEY, "token": TRELLO_APP_TOKEN}
    response = requests.request("GET", url, params=querystring)
    data = json.loads(response.text)
    return(data)

def get_todays_cards(TODAYS_LIST_ID):
    return get_cards_in_list(TODAYS_LIST_ID)

def setup(STORAGE):
    os.mkdir(STORAGE)

def send_slack_reminder(data):
    message = "Yo! It's the end of the day and you haven't completed "+ str(len(data)) + " tasks! come on!!"
    slack_notify(message)

def main():
    STORAGE=ROOT_DIR+"/Storage"
    TODAY_SNAPSHOT=STORAGE+"/today_snapshot.data"
    if os.path.isdir(STORAGE) == False:
        setup(STORAGE)
    
    if os.path.isfile(TODAY_SNAPSHOT) == False:
        dont_compare = 1

    today_data = get_todays_cards(TODAYS_LIST_ID)
    if len(today_data) > 0:
        send_slack_reminder(today_data)

if __name__ == "__main__":
    main()