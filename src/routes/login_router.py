from fastapi import APIRouter, HTTPException, Request
from src.service.oauth2_google import OAuth2Google

login_router = APIRouter()
oauth_google = OAuth2Google()

@login_router.get("/login")
async def login(request: Request):
    try:
        return await oauth_google.login(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@login_router.get("/auth")
async def auth(request: Request):
    try:
        return await oauth_google.auth(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@login_router.get("/logout")
async def logout(request: Request):
    try:
        return await oauth_google.logout(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))