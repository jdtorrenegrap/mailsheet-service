from pydantic import BaseModel

class SmtpConfig(BaseModel):
    smtp_server: str
    port: int
    email: str
    password: str

class EmailData(BaseModel):
    subject: str
    body: str
    excel_file: str
    sheet_name: str
    recipient_column: str
    subject_column: str

class CombinedData(BaseModel):
    smtp_config: SmtpConfig
    email_data: EmailData