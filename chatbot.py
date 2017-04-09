#!/usr/bin/env python
# coding:utf-8

# Messenger API integration example
# We assume you have:
# * a Wit.ai bot setup (https://wit.ai/docs/quickstart)
# * a Messenger Platform setup (https://developers.facebook.com/docs/messenger-platform/quickstart)
# You need to `pip install the following dependencies: requests, bottle.
#
# 1. pip install requests bottle
# 2. You can run this example on a cloud service provider like Heroku, Google Cloud Platform or AWS.
#    Note that webhooks must have a valid SSL certificate, signed by a certificate authority and won't work on your localhost.
# 3. Set your environment variables e.g. WIT_TOKEN=your_wit_token
#                                        FB_PAGE_TOKEN=your_page_token
#                                        FB_VERIFY_TOKEN=your_verify_token
# 4. Run your server e.g. python examples/messenger.py {PORT}
# 5. Subscribe your page to the Webhooks using verify_token and `https://<your_host>/webhook` as callback URL.
# 6. Talk to your bot on Messenger!

import os
import requests
import logging
import settings
from sys import argv

from wit import Wit
from flask import Flask, request


# Import APIs & Services
import weather
import worldtime

logging.basicConfig(level=logging.DEBUG)

# Wit.ai API parameters
WIT_TOKEN = settings.WIT_TOKEN

# Messenger API parameters
FB_PAGE_TOKEN = settings.FB_PAGE_TOKEN

# A user secret to verify webhook get request.
FB_VERIFY_TOKEN = settings.FB_VERIFY_TOKEN


# Setup Flask Server

app = Flask(__name__)


# Facebook Messenger GET Webhook
@app.route('/', methods=['GET'])
def messenger_webhook():
    """
    A webhook to return a challenge
    """
    verify_token = request.args.get('hub.verify_token')
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
                        logging.info("Audio URL : {}".format(audio_url))

                        speech_response = speech_to_wit(audio_url=audio_url)
                        logging.info(" Response from WIT : {}".format(speech_response))
                        try:
                            client.run_actions(session_id=fb_id, message=speech_response)
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
                        client.run_actions(session_id=fb_id, message=text)
                    except:
                        # Delete messages else it keeps looping on error
                        del data
    else:
        # Returned another event
        return 'Received Different Event'
    return 'OK'


def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }
    # Setup the query string with your PAGE TOKEN
    #qs = 'access_token=' + FB_PAGE_TOKEN
    # Send POST request to messenger
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages",
                         params={"access_token": FB_PAGE_TOKEN},
                         json=data,
                         headers={'Content-type': 'application/json'})
    return resp.content

def speech_to_wit(audio_url):
    """

    :param audio_url: 
    :return: response as per Wit.AI API docs
    """

    # Download the URL

    r = requests.get(audio_url)
    with open('audio.wav', 'wb') as f:
        f.write(r.content)

    logging.debug("Audio file received")

    response = None
    header = {'Content-Type': 'audio/mpeg3'}
    with open('audio.wav', 'rb') as f:
        response = client.speech(f, None, header)

    return response

def first_entity_value(entities, entity):
    """
    Returns first entity value
    """
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def send(request, response):
    """
    Sender function
    """
    # We use the fb_id as equal to session_id
    fb_id = request['session_id']
    text = response['text']
    # send message
    fb_message(fb_id, text)

def merge(request):
    context = request['context']
    entities = request['entities']
    print entities
    loc = first_entity_value(entities, 'location')
    if loc:
        context['weatherLocation'] = loc
        context['timeLocation'] = loc
    return context

### Services and APIs

def getWeather(request):
    context = request['context']
    entities = request['entities']
    #loc = first_entity_value(entities, 'loc')
    del context['timeLocation']
    loc = context['weatherLocation']
    if loc:
        # This is where we use a weather service api to get the weather.
        try:
            context['forecast'] = weather.inWeather(loc)
            if context.get('missingLocation') is not None:
                del context['missingLocation']
        except:
            context['default'] = True
            del context['weatherLocation']

            # Delete session ID to stop looping
            del request['session_id']
    else:
        context['missingLocation'] = True
        if context.get('forecast') is not None:
            del context['forecast']
    return context

def getName(request):
    context = request['context']

    # Get user name from the Messenger API
    sender_id = request['session_id']
    resp = requests.get("https://graph.facebook.com/v2.6/" + sender_id,
                        params={"access_token": FB_PAGE_TOKEN})

    sender_name = resp.json()['first_name']
    context['sender_name'] = sender_name
    return context

def getTime(request):
    context = request['context']
    entities = request['entities']
    del context['weatherLocation']
    loc = context['timeLocation']
    if loc:
        try:
            context['country_time'] = worldtime.world_time(loc)
            if context.get('missingCountry') is not None:
                del context['missingCountry']
        except:
            context['default'] = True
            del context['timeLocation']

            # Delete session ID to stop looping
            del request['session_id']
    else:
        context['missingCountry'] = True
        if context.get('country_time') is not None:
            del context['country_time']

    return context

# Setup Actions
actions = {
    'send': send,
    'merge': merge,
    'getWeather': getWeather,
    'getName' : getName,
    'getTime' : getTime,
}

# Setup Wit Client
client = Wit(access_token=WIT_TOKEN, actions=actions)

if __name__ == '__main__':
    # Run Server
    app.run()
