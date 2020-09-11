import requests
import json
from collections import Counter

def main():
    
    try:
        credentials = json.load(open('credentials.json'))
    except FileNotFoundError:
        print("'credentials.json' is missing. Copy credentials_template.json to" +
                "credentials.json and change the appropiet values")
        return

    cards = get_cards_by_name(credentials)
    auto_cards = get_auto_cards()

    for instance in auto_cards["weekly"]:
        if instance["name"] in cards.keys():
            for i in range(0, instance["ocurrenses"] - cards[instance["name"]]):
                add_card(credentials, instance["name"])
        else:
            for i in range(0, instance["ocurrenses"]):
                add_card(credentials, instance["name"])


def add_card(credentials, name):
    url = "https://api.trello.com/1/cards"

    query = {
        'key': credentials["key"],
        'token': credentials["token"],
        'idList': credentials["idList"],
        'name': name
    }

    response = requests.request(
        "POST",
        url,
        params=query
    )


def get_cards(credentials):
    
    url = f"https://api.trello.com/1/lists/{credentials['idList']}/cards"

    query = {
        'key': credentials["key"],
        'token': credentials["token"],
    } 

    response = requests.request(
        "GET",
        url,
        params=query
    )
 
    return json.loads(response.text)


def get_cards_by_name(credentials):
    cards = get_cards(credentials)
    return Counter([instance["name"] for instance in cards])
    

def get_auto_cards():
    return json.load(open("cards.json"))


if __name__ == "__main__":
    main()
