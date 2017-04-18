import speech_recognition as sr

from src import settings

# Record Audio
WIT_TOKEN = settings.WIT_TOKEN

class Speech(object):

    def __init__(self):
        self.r = sr.Recognizer()

    def recognize_google(self):
        response = ''
        r = self.r
        #r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            response = r.recognize_google(audio)
            print "You said: " + response
        except sr.UnknownValueError:
            print "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            print "Could not request results from Google Speech Recognition service; {0}".format(e)

        return response

    def recognize_wit(self):
        response = ''
        r = self.r
        #r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            response = r.recognize_wit(audio, WIT_TOKEN)
            print "You said: " + response
        except sr.UnknownValueError:
            print "Wit Speech Recognition could not understand audio"
        except sr.RequestError as e:
            print "Could not request results from Wit Speech Recognition service; {0}".format(e)

        return response


#s = Speech()
#s.recognize()