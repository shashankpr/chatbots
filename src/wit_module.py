import logging
import sys
from os import path
import random
import requests
from wit import Wit

import messenger
import settings

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# API Services
from services.weather import CallWeather
from services.worldtime import CallGoogleTime
from services.currency_conversion import CurrencyRates
from services import flux_api


class CallWit(object):
    def __init__(self):
        # Wit.ai API parameters
        self.WIT_TOKEN = settings.WIT_TOKEN

        # Messenger API parameters
        self.FB_PAGE_TOKEN = settings.FB_PAGE_TOKEN

        # Actions - Deprecated in new Wit API

        # # Setup Actions
        # actions = {
        #     'send': self.send_fb,
        #     'merge': self.merge,
        #     'getWeather': self.getWeather,
        #     'getName': self.getName,
        #     'getTime': self.getTime,
        #     'getConversion': self.get_currency_conversion,
        # }

        # Setup Wit Client
        self.client = Wit(access_token=self.WIT_TOKEN)

        self.default_msg = "Sorry mate ! I didn't get what you said..."
        self.welcome_msg = "Hey !! How can you help you today ? You can ask me about `Weather`, `Time` at a place and " \
                           "I can also do some currency conversions !! "

    def handle_message(self, session_id, user_query):
        wit_response = self.client.message(msg=user_query)
        logging.debug("Response from Wit : {}".format(wit_response))

        user_name = self.getName(session_id)
        entities = wit_response['entities']
        context_dict = self.merge(wit_response)

        # TODO account for confidence values
        greetings = self.first_entity_value(entities, 'greetings')
        light_toggle = self.first_entity_value(entities, 'on_off')
        intent = self.first_entity_value(entities=entities, entity='intent')
        logging.info("Intent obtained : {}".format(intent))

        if intent == 'getWeather':
            context = self.getWeather(context_dict)
            messenger.fb_message(session_id, self.weather_replies(user_name, context))

        elif intent == 'getTime':
            context = self.getTime(context_dict)
            messenger.fb_message(session_id, self.time_replies(user_name, context))

        elif intent == 'curConvert':
            context = self.get_currency_conversion(context_dict)
            messenger.fb_message(session_id, self.currency_replies(user_name, context))

        elif greetings == 'greetings':
            messenger.fb_message(session_id, self.welcome_msg)

        elif greetings == 'end':
            messenger.fb_message(session_id, "See you soon then !!!")

        elif light_toggle == 'on':
            messenger.fb_message(session_id, "Switching ON the light ...")
            self.turn_on_flux(session_id)

        elif light_toggle == 'off':
            messenger.fb_message(session_id, "Switching OFF the light ...")
            self.turn_off_flux(session_id)

        else:
            messenger.fb_message(session_id, self.default_msg)

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
        entity_val = entities[entity][0]['value']
        if not entity_val:
            return None
        return entity_val['value'] if isinstance(entity_val, dict) else entity_val

    def merge(self, request):
        try:
            context = request['context']
        except:
            context = {}
        entities = request['entities']

        loc = self.first_entity_value(entities, 'location')

        # Get context for currency conversion
        currency_source = self.first_entity_value(entities, 'source')
        currency_dest = self.first_entity_value(entities, 'destination')
        if currency_source and currency_dest:
            context['currencyNameSource'] = currency_source
            context['currencyNameDest'] = currency_dest

        elif loc:
            context['weatherLocation'] = loc
            context['timeLocation'] = loc

        return context

    # Services and APIs

    def getWeather(self, context):
        # context = request['context']
        # entities = request['entities']
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
                context['weather_default'] = True
                del context['weatherLocation']

                # Delete session ID to stop looping
                # del request['session_id']
        else:
            context['missingLocation'] = True
            if context.get('forecast') is not None:
                del context['forecast']
        return context

    def getName(self, session_id):
        # context = request['context']

        # Get user name from the Messenger API
        resp = requests.get("https://graph.facebook.com/v2.8/" + session_id,
                            params={"access_token": self.FB_PAGE_TOKEN})

        print resp
        sender_name = resp.json()['first_name']
        return sender_name

    def getTime(self, context):
        # context = request['context']
        # entities = request['entities']
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
                context['time_default'] = True
                del context['timeLocation']

                # Delete session ID to stop looping
                # del request['session_id']
        else:
            context['missingCountry'] = True
            if context.get('country_time') is not None:
                del context['country_time']

        return context

    def get_currency_conversion(self, context):

        # context = request['context']

        source_name = context['currencyNameSource']
        dest_name = context['currencyNameDest']

        currency_object = CurrencyRates()
        if source_name and dest_name:
            try:
                context['conversionVal'] = currency_object.get_conversion_rate(source_name, dest_name)
            except:
                context['cur_default'] = True
                del context['currencyNameSource']
                del context['currencyNameDest']
        else:
            context['cur_default'] = True
            del context['currencyNameSource']
            del context['currencyNameDest']
        return context

    def turn_on_flux(self, session_id):

        try:
            ipaddr = flux_api.scan_bulb()
            flux_api.switch_on(ipaddr)
            return
        except:
            messenger.fb_message(session_id, "The bulb doesn't seem to be online")
            return


    def turn_off_flux(self, session_id):

        try:
            ipaddr = flux_api.scan_bulb()
            flux_api.switch_off(ipaddr)
            return
        except:
            messenger.fb_message(session_id, "The bulb doesn't seem to be online")
            return


    #  Replies from Wit

    def weather_replies(self, user_name, context):
        response_template = random.choice(
            ['Hey {mention} ! Weather at {location} is {forecast}',
             'Yo {mention}! It is {forecast} at {location}',
             'Hi {mention} ! The weather is {weather} at {location}'
             ])

        return response_template.format(mention=user_name, location=context.get('weatherLocation'),
                                        forecast=context.get('forecast'))

    def time_replies(self, user_name, context):
        response_template = random.choice(
            ['Hey {mention} ! Time at {location} is {time}',
             'Yo {mention}! It is {time} at {location}',
             'The time is {time} at {location}...',
             'Uno momento please {mention} ... The time is {time} at {location} !!'
             ])

        return response_template.format(mention=user_name, location=context.get('timeLocation'),
                                        time=context.get('country_time'))

    def currency_replies(self, user_name, context):
        response_template = random.choice(
            ['Hey {mention} ! 1 {source_currency} is equal to {conversion_val} {dest_currency}',
             'Yo {mention} ! 1 {source_currency} is equal to {conversion_val} {dest_currency}',
             'Just a moment ... Hey {mention} ! 1 {source_currency} is equal to '
             '{conversion_val} {dest_currency}'
             ])

        return response_template.format(mention=user_name, source_currency=context.get('currencyNameSource'),
                                        dest_currency=context.get('currencyNameDest'),
                                        conversion_val=context.get('conversionVal'))

    def wit_interactive(self):

        client = Wit(access_token=self.WIT_TOKEN)
        client.interactive()


if __name__ == '__main__':
    c = CallWit()
    c.wit_interactive()
