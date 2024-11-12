import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

api_endpoint = os.environ["API_ENDPOINT"]
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

session = requests.Session()
session.auth = HTTPBasicAuth(username, password)
