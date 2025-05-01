from fastapi import Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from src.middleware.token import TokenJwt
from src.core.config import Settings

class OAuth2Google:

    def __init__(self):
        self.oauth = OAuth()
        self.oauth.register(
            name='google',
            client_id=Settings.CLIENTE_ID,
            client_secret=Settings.CLIENTE_SECRET,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile',
                'redirect_uri': 'http://127.0.0.1:8000/auth/auth'
            }
        )
    
    # Iniciar login con Google
    async def login(self, request: Request):
        redirect_uri = request.url_for('auth')
        return await self.oauth.google.authorize_redirect(request, redirect_uri)
    
    # Ruta de callback (Google nos redirige aquí)
    async def auth(self, request: Request):
        token = await self.oauth.google.authorize_access_token(request)
        user = token.get('userinfo')

        if user:
            jwt_token = TokenJwt.create_access_token(data=user)
            return {"access_token": jwt_token,}

        return {"error": "Authentication failed."}
    
    # Cerrar sesión
    async def logout(self, request: Request):
        request.session.clear()
        return RedirectResponse("http://localhost:8000/auth/login")