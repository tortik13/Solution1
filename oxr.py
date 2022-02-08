import os
from dotenv import load_dotenv

path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(path):
    load_dotenv(path)

    APP_KEY = os.environ.get('APP_KEY')