import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    
    CLIENTE_ID = os.getenv("CLIENT_ID")
    CLIENTE_SECRET = os.getenv("CLIENT_SECRET")

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    SECRET_KEY_COOKIE = os.getenv("SECRET_KEY_COOKIE")