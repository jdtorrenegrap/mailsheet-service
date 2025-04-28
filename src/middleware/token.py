import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from src.core.config import Settings 

SECRET_KEY = Settings.SECRET_KEY
ALGORITHM = Settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Settings.ACCESS_TOKEN_EXPIRE_MINUTES

class TokenJwt:
    
    @classmethod
    def create_access_token(self, data: dict):
        expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": data["email"],
            "name": data["name"],
            "picture": data["picture"],
            "exp": expiration,
            "iat": datetime.utcnow(),
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token