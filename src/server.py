import logging
from flask import Flask, request

import settings
from wit_module import CallWit

app = Flask(__name__)

FB_VERIFY_TOKEN = settings.FB_VERIFY_TOKEN

# Intialize Wit Class
witObject = CallWit()


# Facebook Messenger GET Webhook
@app.route('/', methods=['GET'])
def messenger_webhook():
    """
    A webhook to return a challenge
    """
    verify_token = request.args.get('hub.verify_token')
    print verify_token
    # check whether the verify tokens match
    if verify_token == FB_VERIFY_TOKEN:
        # respond with the challenge to confirm
        challenge = request.args.get('hub.challenge')
        return challenge
    else:
        return 'Invalid Request or Verification Token'


# Facebook Messenger POST Webhook
@app.route('/', methods=['POST'])
def messenger_post():
    """
    Handler for webhook (currently for postback and messages)
    """
    data = request.json
    if data['object'] == 'page':
        for entry in data['entry']:
            # get all the messages
            print entry
            messages = entry['messaging']
            if messages[0]:
                # Get the first message
                message = messages[0]
                # Yay! We got a new message!
                # We retrieve the Facebook user ID of the sender
                fb_id = message['sender']['id']
                # We retrieve the message content
                # Check for message type - Text or Audio
                try:
                    # Check if it's Audio type
                    msg_type = message['message']['attachments'][0]['type']
                    if msg_type == 'audio':
                        audio_url = message['message']['attachments'][0]['payload']['url']
                        # logging.info("Audio URL : {}".format(audio_url))

                        speech_response = witObject.speech_to_wit(audio_url=audio_url)
                        # logging.info(" Response from WIT : {}".format(speech_response))
                        try:
                            # witObject.client.run_actions(session_id=fb_id, message=speech_response)
                            witObject.handle_message(session_id=fb_id, user_query=speech_response)
                        except:
                            # Delete messages else it keeps looping on error
                            del data
                    else:
                        logging.debug("Not Audio Type")
                except:
                    text = message['message']['text']
                    logging.debug("Message Received: %s  -- %s" % (text, fb_id))
                    # Let's forward the message to the Wit.ai Bot Engine
                    # We handle the response in the function send()
                    try:
                        # Using Wit's new /message api endpoint
                        witObject.handle_message(session_id=fb_id, user_query=text)
                        # witObject.client.run_actions(session_id=fb_id, message=text)
                        # resp = witObject.client.message(msg=text)
                    except:
                        # Delete messages else it keeps looping on error
                        del data
    else:
        # Returned another event
        return 'Received Different Event'
    return 'OK'

if __name__ == '__main__':
    # Run Server
    app.run(debug=True)
