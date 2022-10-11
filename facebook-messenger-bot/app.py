import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAARJC5uL8NcBANCxZAuLDVAWJezmKDLZAGpIeQKPw70vuo0FzspuCF2umOlTlqWN62TVzzLkVjXzv4MyhnOuien0hZBsjav0CMMuZBQkqR4ZClMmXpgf3JpmghGh7a63ZAOTgH2RGZB3UrCD6rvU2ZAK0ZBEdn3xszSPXWUw2X8BNoVDS2PPrH6hbQZCYZC4EoFS7gZD"
bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
    # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello worl", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    response = None

                    entity, value, Intents = wit_response(messaging_text)

                    if Intents == 'Flight_Book':
                        response = "Ok, so you want to fly to {0}. Here are the best fight schedules to {0} in recent future".format(str(value))
                    elif Intents == 'Hotel_Book':
                        response = "Ok, trying to find and book best hotel rooms in {0}".format(str(value))
                    elif Intents == 'tourist_place':
                        response = "Ok, so you want to tour in {0}. Here are top destination in {0}".format(str(value))
                    elif entity == None and value == None:
                        response = "Ok, specify where is your destination".format(str(value))

                    if response == None:
                        response = "I dont understand what you are trying to say!"

                    bot.send_text_message(sender_id, response)

    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug=True, port=8000)