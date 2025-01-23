from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.email_router import email_router


app = FastAPI()
app.include_router(router=email_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Permitir solicitudes desde Streamlit
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los headers
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)