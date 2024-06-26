API endpoint and credtentials are stored in the env variable
use pip install python-dotenv to install lib https://pypi.org/project/python-dotenv/

######Example######

import os
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = "https://thisisa/example/v1/"
USERNAME = "example"
PASSWORD = "3x4mp1e"