import logging
import sys

import wit_speech
from speech import Speech

# Set default logging for the module. Client applications can use a custom
# logging config to override defaults specified here
logging.getLogger(__name__).setLevel(logging.INFO)
logging.getLogger(__name__).propagate = False
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logging.getLogger(__name__).addHandler(handler)