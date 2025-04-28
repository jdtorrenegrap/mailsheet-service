import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import base64
from io import BytesIO

from src.model.email_automation_model import CombinedData

class EmailController:
    def __init__(self, smtp_server, smtp_port, smtp_email, smtp_password, sender_email, subject, message):
        # servidor smtp
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_email = smtp_email
        self.smtp_password = smtp_password
        # configuración de correo
        self.sender_email = sender_email
        self.subject = subject
        self.message = message

    def load_excel_file(self, excel_file, sheet_name):
        try:
            excel_bytes = base64.b64decode(excel_file)
            excel_io = BytesIO(excel_bytes)
            self.recipients_df = pd.read_excel(excel_io, sheet_name=sheet_name)            
        except Exception as e:
            raise ValueError(f"No coincide el nombre de la hoja: {e}")
            
    def send_emails(self, recipient_column, subject_column):
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
                smtp.starttls() # Start TLS for security
                smtp.login(self.smtp_email, self.smtp_password) # Login to SMTP server
                
                # Itera sobre las filas de recipients_df
                for index, row in self.recipients_df.iterrows():
                    column_name = row[recipient_column]
                    column_email = row[subject_column]

                    # Verifica si el valor de la columna es un correo electrónico válido
                    if not column_name or not column_email:
                        print(f"Skipping row {index}: missing name or email.")
                        continue
                    if not (isinstance(column_email, str) and "@" in column_email and "." in column_email):
                        print(f"Skipping row {index}: invalid email format.")
                        continue

                    

                    message = self.message.replace("[destinatario]", str(column_name))
                    receiver_email = column_email
                    
                    msg = MIMEMultipart()
                    msg['From'] = self.sender_email
                    msg['To'] = receiver_email
                    msg['Subject'] = self.subject
                    msg.attach(MIMEText(message, 'plain'))
                    try:
                        smtp.sendmail(self.sender_email, receiver_email, msg.as_string())
                        print(f'Email sent successfully: {receiver_email}')
                    except Exception as inner_e:
                        print(f"Failed to send email to {receiver_email}: {inner_e}")

        except smtplib.SMTPAuthenticationError:
            print('El servidor no aceptó la combinación de username/password.')
            raise ValueError("El servidor no aceptó la combinación de username/password.")
        except smtplib.SMTPConnectError:
            print('Se produjo un error durante el establecimiento de conexión con el servidor.')
            raise ValueError("Se produjo un error durante el establecimiento de conexión con el servidor.")
        except smtplib.SMTPDataError:
            print('El servidor respondió con un código de error inesperado (que no sea el rechazo de un destinatario).')
        except smtplib.SMTPException as e:
            print(f'No se encontró ningún método de autenticación adecuado. {e}')
        except FileNotFoundError:
            print('El archivo Excel especificado no se encontró.')
        except KeyError as e:
            print(f'La columna especificada en el archivo Excel no se encontró: {e}')
        except Exception as e:
            print(f'Se produjo un error inesperado: {e}')
            print(f"No es un correo {column_email}")
            raise ValueError(f"No es un correo {column_email}")

def process_combined_data(combined_data: CombinedData):
    # Extraer los datos de configuración y los datos del correo electrónico del objeto combinado
    config_server = combined_data.smtp_config
    email_data = combined_data.email_data

    # Crear una instancia de la clase EmailController con los datos proporcionados
    email_automation = EmailController(
        config_server.smtp_server,
        config_server.port,
        config_server.email,
        config_server.password,
        config_server.email,
        email_data.subject,
        email_data.body  # ahora se usa 'body' en lugar de 'message'
    )

    # Cargar el archivo Excel con los datos de los destinatarios
    try:
        email_automation.load_excel_file(email_data.excel_file, email_data.sheet_name)
    except ValueError as e:
        raise ValueError(f"No se pudo cargar el archivo Excel: {e}")

    # Validar que las columnas especificadas existan en el archivo Excel
    if email_data.recipient_column not in email_automation.recipients_df.columns:
        raise ValueError(f"No coincide el nombre de la columna Nombre: {email_data.recipient_column}")
    if email_data.subject_column not in email_automation.recipients_df.columns:
        raise ValueError(f"No coincide el nombre de la columna Correos: {email_data.subject_column}")

    # Enviar los correos electrónicos a los destinatarios especificados
    try:
        email_automation.send_emails(email_data.recipient_column, email_data.subject_column)
    except ValueError as e:
        raise ValueError(f"Error al enviar el mensaje: {e}")