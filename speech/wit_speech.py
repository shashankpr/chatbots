import logging
import sys
import uuid
from os import system

from wit import Wit

sys.path.insert(0, '/Users/Shashank/Workspace_dev/Git/chatbots/')

from src import settings
from src.services import weather
from src.services import worldtime
# import pyttsx

from speech import Speech

logging.basicConfig(level=logging.DEBUG)

# Wit.ai API parameters
WIT_TOKEN = settings.WIT_TOKEN


# Generate random Session ID

def generate_session_id():
    session_id = uuid.uuid4()
    return session_id


def get_speech_to_text():
    s = Speech()
    speech_response = s.recognize_google()
    return speech_response


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
    print response['text']

    # Include Speech Output
    # Works only in Mac currently
    # Comment it out if not needed
    response_text = response['text']
    say_resp = 'say ' + response_text
    system(say_resp)

    # The Following lines use PyTTSx
    # Throws error on Mac currently.

    # engine = pyttsx.init()
    # engine.say(response_text)
    # engine.runAndWait()


def merge(request):
    context = request['context']
    entities = request['entities']
    print entities
    loc = first_entity_value(entities, 'location')
    if loc:
        context['weatherLocation'] = loc
        context['timeLocation'] = loc
    return context


def getWeather(request):
    context = request['context']
    entities = request['entities']
    # loc = first_entity_value(entities, 'loc')
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
    # context = {}
    entities = request['entities']

    user_name = first_entity_value(entities, 'contact')
    if user_name:
        context['user_name'] = user_name
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
    'getName': getName,
    'getTime': getTime,
}

session_id = generate_session_id()
speech_to_text = get_speech_to_text()
# Setup Wit Client
client = Wit(access_token=WIT_TOKEN, actions=actions)

try:
    client.run_actions(session_id=session_id, message=speech_to_text, max_steps=8)
except (KeyboardInterrupt, EOFError):
    exit()

    # client.interactive()
