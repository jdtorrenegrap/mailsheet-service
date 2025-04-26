from fastapi import APIRouter, HTTPException
from src.controller.email_automation_controller import process_combined_data
from src.model.email_automation_model import CombinedData

email_router = APIRouter()

@email_router.post("/send-email")
async def send_email(combined_data: CombinedData):
    try:
        process_combined_data(combined_data)
        return {"message": "Correo enviado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 