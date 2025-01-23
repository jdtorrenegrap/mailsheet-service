from pydantic import BaseModel

class SmtpConfig(BaseModel):
    smtp_server: str
    port: int
    email: str
    password: str

class EmailData(BaseModel):
    subject: str
    message: str
    excel_file: str
    sheet_name: str
    column_x: str
    column_y: str

class CombinedData(BaseModel):
    smtp_config: SmtpConfig
    email_data: EmailData