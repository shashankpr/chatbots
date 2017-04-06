import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

WIT_TOKEN = os.environ.get("WIT_TOKEN")
FB_PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN")
OWM_API_TOKEN = os.environ.get("OWM_API_TOKEN")
FB_VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN")