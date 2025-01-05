from datetime import datetime
from sqlalchemy.orm import Session
from smtplib import SMTP
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
# send_email.py
# load_dotenv()

# smtp_password = os.getenv("APP_CONFIG__SMTP_PASSWORD")

def send_email(to_email, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = "mangowillgoodboy@gmail.com"
    from_password = "ftgtlqcwosgfjtqe" # Используйте токен или секретный пароль приложения

    try:
        # Настройка SMTP соединения
        with SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, from_password)

            # Формирование письма
            msg = MIMEText(body, "plain")
            msg["Subject"] = subject
            msg["From"] = from_email
            msg["To"] = to_email

            # Отправка письма
            server.send_message(msg)
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

