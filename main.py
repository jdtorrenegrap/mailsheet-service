from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.login_router import login_router
from src.routes.email_router import email_router
from starlette.middleware.sessions import SessionMiddleware  # Importa si vas a usar sesiones

def create_app() -> FastAPI:
    app = FastAPI()

    # Middleware para sesiones (si usas OAuth con cookies)
    app.add_middleware(SessionMiddleware, secret_key="tu_secreto_super_seguro")
    
    # Middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
        allow_credentials=True,
        allow_methods=["*"],  # Permitir todos los métodos
        allow_headers=["*"],  # Permitir todos los headers
    )

    # Routers
    app.include_router(email_router, prefix="/email", tags=["email"])
    app.include_router(login_router, prefix="/auth", tags=["auth"])

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
