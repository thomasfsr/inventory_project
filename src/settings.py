import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()
        for key, value in os.environ.items():
            setattr(self, key, value)