import requests
import settings

FB_PAGE_TOKEN = settings.FB_PAGE_TOKEN


def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }
    # Setup the query string with your PAGE TOKEN
    # qs = 'access_token=' + FB_PAGE_TOKEN
    # Send POST request to messenger
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages",
                         params={"access_token": FB_PAGE_TOKEN},
                         json=data,
                         headers={'Content-type': 'application/json'})

    # print resp.content
    return resp.content

fb_message(1407266826015412, "test123")