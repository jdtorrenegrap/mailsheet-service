from fastapi import APIRouter, Request
from src.service.oauth2_google import OAuth2Google

login_router = APIRouter()
oauth_google = OAuth2Google()

@login_router.get("/login")
async def login(request: Request):
    return await oauth_google.login(request)

@login_router.get("/auth")
async def auth(request: Request):
    return await oauth_google.auth(request)

@login_router.get("/logout")
async def logout(request: Request):
    return await oauth_google.logout(request)