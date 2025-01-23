import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import base64
from io import BytesIO

from model.email_automation_model import CombinedData

class EmailController:
    def __init__(self, smtp_server, smtp_port, smtp_email, smtp_password, sender_email, subject, message):
        # servidor smtp
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_email = smtp_email
        self.smtp_password = smtp_password
        # configuracion de correo
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
            

    def send_emails(self, column_x, column_y):
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
                smtp.starttls() # Start TLS for security
                smtp.login(self.smtp_email, self.smtp_password) # Login to SMTP server
                
                # Itera sobre las filas de recipients_df
                for index, row in self.recipients_df.iterrows():
                    column_name = row[column_x]
                    column_email = row[column_y]

                    if isinstance(column_email, str) and '@' in column_email and '.' in column_email:
                        message = self.message.replace("[destinatario]", column_name)
                        receiver_email = column_email
                        msg = MIMEMultipart()
                        msg['From'] = self.sender_email
                        msg['To'] = receiver_email
                        msg['Subject'] = self.subject
                        msg.attach(MIMEText(message, 'plain'))
                        smtp.sendmail(self.sender_email, receiver_email, msg.as_string())
                        print(f'Email sent successfully: {receiver_email}')

        except smtplib.SMTPAuthenticationError:
            print('El servidor no aceptó la combinación de username/password.')
            raise ValueError(f"El servidor no aceptó la combinación de username/password.")
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
    menssage_email = combined_data.email_data

    # Crear una instancia de la clase EmailAutomation con los datos proporcionados
    email_automation = EmailController(
        config_server.smtp_server,
        config_server.port,
        config_server.email,
        config_server.password,
        config_server.email,
        menssage_email.subject,
        menssage_email.message
    )

    # Cargar el archivo Excel con los datos de los destinatarios
    try:
        email_automation.load_excel_file(menssage_email.excel_file, menssage_email.sheet_name)
    except ValueError as e:
        raise ValueError(f"No se pudo cargar el archivo Excel: {e}")

    # Validar que las columnas especificadas existan en el archivo Excel
    if menssage_email.column_x not in email_automation.recipients_df.columns:
        raise ValueError(f"No coincide el nombre de la columna Nombre: {menssage_email.column_x}")
    if menssage_email.column_y not in email_automation.recipients_df.columns:
        raise ValueError(f"No coincide el nombre de la columna Correos: {menssage_email.column_y}")

    # Enviar los correos electrónicos a los destinatarios especificados
    try:
        email_automation.send_emails(menssage_email.column_x, menssage_email.column_y)
    except ValueError as e:
        raise ValueError(f"Error al enviar el mensaje: {e}")