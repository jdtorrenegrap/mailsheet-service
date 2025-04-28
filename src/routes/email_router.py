from fastapi import APIRouter, Depends, HTTPException
from src.service.email_automation_controller import process_combined_data
from src.model.email_automation_model import CombinedData
from src.middleware.auth_token import get_current_user

email_router = APIRouter()

@email_router.post("/send-email")
async def send_email(combined_data: CombinedData, current_user: dict = Depends(get_current_user)):
    user_email = current_user.get("sub")
    if not user_email:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")
    
    try:
        process_combined_data(combined_data)
        return {"message": "Correo enviado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 