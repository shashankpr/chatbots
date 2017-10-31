import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

WIT_TOKEN = os.environ.get("WIT_TOKEN")
FB_PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN")
FB_VERIFY_TOKEN = os.environ.get("FB_VERIFY_TOKEN")