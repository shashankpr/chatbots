import requests
import settings

FB_PAGE_TOKEN = settings.FB_PAGE_TOKEN

def getFB_profile(sender_id):
    resp = requests.get("https://graph.facebook.com/v2.6/" + sender_id,
                        params={"access_token": FB_PAGE_TOKEN})
    #print resp.content
    print resp.json()['first_name']


sender_id = '1407266826015412'

getFB_profile(sender_id)