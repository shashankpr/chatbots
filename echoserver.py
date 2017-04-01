from flask import Flask, request
from wit import Wit
import warnings

import messenger
import chatbot

app = Flask(__name__)

FACEBOOK_TOKEN = 'EAACyYurnCYEBANLpIzLGAYA38fGeIXwS0v0q4LiZC7eH45LLnGMNe43ePXRYYDqWthXuW1qRJ5IZBxV3Ipek5ZCe3iMs0hZCZAN4BAOLZB41pHUTT0sZBVxEZAZCsiYckz1PDgAJVqzQMMhVAZCHzcKY49rtjwIO5lKeM8nUZBGTxGWCwZDZD'
FB_VERIFY_TOKEN = 'mischief_managed'

@app.route('/', methods=['GET'])
def handle_verification():
    print "Handling Verification: ->"
    if request.args.get('hub.verify_token', '') == FB_VERIFY_TOKEN:
        print "Verification successful!"
        return request.args.get('hub.challenge', '')
    else:
        print "Verification failed!"
        return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def webhook():
    print "Handling Messages"
    payload = request.get_data()
    print payload
    for sender, message in messenger.messaging_events(payload):
        print "Incoming from %s: %s" % (sender, message)

        client = chatbot.set_action(sender, message)
        client.run_actions(sender, message)
        #response = bot.respond_to(message)

        print "Outgoing to %s: %s" % (sender, message)
        messenger.send_message(FACEBOOK_TOKEN, sender, message)
    return "ok"


if __name__ == '__main__':

    #gbot = chatbot
    app.run()
