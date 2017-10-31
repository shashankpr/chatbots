import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

OWM_API_TOKEN = os.environ.get("OWM_API_TOKEN")
GOOGLE_MAPS_TOKEN = os.environ.get("GOOGLE_MAPS_TOKEN")
CURRENCY_LAYER_TOKEN = os.environ.get("CURRENCY_LAYER_TOKEN")
