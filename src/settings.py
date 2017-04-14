import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

WIT_TOKEN = os.environ.get("WIT_TOKEN")
FB_PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN")
OWM_API_TOKEN = os.environ.get("OWM_API_TOKEN")
FB_VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN")
GOOGLE_MAPS_TOKEN = os.environ.get("GOOGLE_MAPS_TOKEN")