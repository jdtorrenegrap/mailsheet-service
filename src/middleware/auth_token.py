from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from src.core.config import Settings
import jwt

SECRET_KEY = Settings.SECRET_KEY
ALGORITHM = Settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Esto es  para la autenticación de JWT en las rutas
# que requieren autenticación. El token se espera en el header de la solicitud.
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
        return payload
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado. Por favor inicia sesión nuevamente."
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido. Acceso denegado."
        )
