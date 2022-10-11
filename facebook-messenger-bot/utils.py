from wit import Wit

wit_access_token = "27CKIZXSWU3T66YZVHYWLPZVQRGHJ6XN"
client = Wit(access_token=wit_access_token)

#message_text = "I want to fly to Dhaka"

def wit_response(message_text):
    resp = client.message(message_text)

    entity = None
    Intents = None
    value = None

    try:
        entity = list(resp['entities'])[0]
        Intents = list(resp['intents'])[0]['name']
        value = resp['entities'][entity][0]['resolved']['values'][0]['name']
    except:
        pass

    return (entity, value, Intents)