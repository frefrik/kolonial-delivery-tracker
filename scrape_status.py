import os
import json
from dotenv import load_dotenv
from pprint import pprint
from src.kolonial import Kolonial

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
JSON_PATH = "delivery.json"

k = Kolonial(USERNAME, PASSWORD)

status = k.delivery_tracker()
pprint(status)

k.quit()

with open(JSON_PATH, "w") as fp:
    json.dump(status, fp)
