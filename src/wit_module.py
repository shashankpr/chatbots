import logging
import sys
from os import path

import requests
from wit import Wit

import messenger
import settings

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# API Services
from services.weather import CallWeather
from services.worldtime import CallGoogleTime


class CallWit(object):
    def __init__(self):
        # Wit.ai API parameters
        self.WIT_TOKEN = settings.WIT_TOKEN

        # Messenger API parameters
        self.FB_PAGE_TOKEN = settings.FB_PAGE_TOKEN

        # Setup Actions
        actions = {
            'send': self.send_fb,
            'merge': self.merge,
            'getWeather': self.getWeather,
            'getName': self.getName,
            'getTime': self.getTime,
        }

        # Setup Wit Client
        self.client = Wit(access_token=self.WIT_TOKEN, actions=actions)

    def speech_to_wit(self, audio_url):
        """
        To Handle Audio files in Messenger
        
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
            response = self.client.speech(f, None, header)

        return response

    def first_entity_value(self, entities, entity):
        """
        Returns first entity value
        """
        if entity not in entities:
            return None
        val = entities[entity][0]['value']
        if not val:
            return None
        return val['value'] if isinstance(val, dict) else val

    def send_fb(self, request, response):
        """
        Sender function
        """
        # We use the fb_id as equal to session_id
        fb_id = request['session_id']
        text = response['text']
        # send message
        messenger.fb_message(fb_id, text)

    def send(self, request, response):
        """
        Sender Function
        :param request: 
        :param response: 
        :return: 
        """
        # We use the fb_id as equal to session_id
        fb_id = request['session_id']
        text = response['text']
        print text

    def merge(self, request):
        context = request['context']
        entities = request['entities']

        loc = self.first_entity_value(entities, 'location')
        if loc:
            context['weatherLocation'] = loc
            context['timeLocation'] = loc
        return context

    # Services and APIs

    def getWeather(self, request):
        context = request['context']
        entities = request['entities']
        # loc = first_entity_value(entities, 'loc')
        del context['timeLocation']
        loc = context['weatherLocation']

        # Initialize Weather API class
        weather_obj = CallWeather(location=loc)
        if loc:
            # This is where we use a weather service api to get the weather.
            try:
                context['forecast'] = weather_obj.inWeather()
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

    def getName(self, request):
        context = request['context']

        # Get user name from the Messenger API
        sender_id = request['session_id']
        resp = requests.get("https://graph.facebook.com/v2.6/" + sender_id,
                            params={"access_token": self.FB_PAGE_TOKEN})

        sender_name = resp.json()['first_name']
        context['sender_name'] = sender_name
        return context

    def getTime(self, request):
        context = request['context']
        entities = request['entities']
        del context['weatherLocation']
        loc = context['timeLocation']

        # Initialize Time API class
        world_time_obj = CallGoogleTime(location=loc)
        if loc:
            try:
                context['country_time'] = world_time_obj.world_time()
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

    def wit_interactive(self):

        actions = {
            'send': self.send,
            'merge': self.merge,
            'getWeather': self.getWeather,
            'getName': self.getName,
            'getTime': self.getTime,
        }
        client = Wit(access_token=self.WIT_TOKEN, actions=actions)
        client.interactive()