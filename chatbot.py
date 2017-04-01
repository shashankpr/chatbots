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
from sys import argv
from wit import Wit
import messenger
#from bottle import Bottle, request, debug
from flask import Flask, request

# Wit.ai parameters
#WIT_TOKEN = os.environ.get('WIT_TOKEN')

WIT_TOKEN = 'GLEQMX7YW4IR4TM5S5B2TUBPWJTCFDQQ'
# Messenger API parameters
#FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN')
FB_PAGE_TOKEN = 'EAACyYurnCYEBANLpIzLGAYA38fGeIXwS0v0q4LiZC7eH45LLnGMNe43ePXRYYDqWthXuW1qRJ5IZBxV3Ipek5ZCe3iMs0hZCZAN4BAOLZB41pHUTT0sZBVxEZAZCsiYckz1PDgAJVqzQMMhVAZCHzcKY49rtjwIO5lKeM8nUZBGTxGWCwZDZD'
# A user secret to verify webhook get request.
FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')

# Setup Flask Server
#debug(True)
#app = Flask(__name__)

messageToSend = "Hi There !! I am Jarvis and I'm awesome"
done = False

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

def say(sender_id, context, response):
    global messageToSend
    messageToSend = str(response)
    global done
    done = True

def send(request, response):
    """
    Sender function
    """
    # We use the fb_id as equal to session_id
    fb_id = request['session_id']
    text = response['text']
    # send message
    messenger.send_message(FB_PAGE_TOKEN, fb_id, text)

def merge(context, entities):
    loc = first_entity_value(entities, 'location')
    if loc:
        context['loc'] = loc
    return context


def fetch_weather(context):
    loc = context['loc']
    #loc = first_entity_value(entities, 'location')
    if loc:
        # This is where we could use a weather service api to get the weather.
        context['forecast'] = 'sunny'
        if context.get('missingLocation') is not None:
            del context['missingLocation']
    else:
        context['missingLocation'] = True
        if context.get('forecast') is not None:
            del context['forecast']
    return context


    # Setup Actions
actions = {
    'say'  : say,
    'send' : send,
    'merge': merge,
    'fetch-weather': fetch_weather,
    }

    # Setup Wit Client
def getWit():
    client = Wit(access_token=WIT_TOKEN, actions=actions)

    return client


# if __name__ == '__main__':
#     # Run Server
#     app.run(host='0.0.0.0', port=argv[1])