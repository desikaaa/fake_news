import os
from dotenv import load_dotenv

load_dotenv()

ENV_MODE = os.getenv("ENV_MODE", "local").lower()

class Config:
    ENV = ENV_MODE
    DEBUG = ENV_MODE == "local"