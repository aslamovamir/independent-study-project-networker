import smtplib
from email.message import EmailMessage

_EMAIL_SERVER_SECRET_USERNAME = "networkeremailserver@gmail.com"
_EMAIL_SERVER_SECRET_APP_PASSWORD = "ikbfdabbziutojmg"
_EMAIL_SERVER_SECRET_PLATFORM = "smtp.gmail.com"
_EMAIL_SERVER_SECRET_PLATFORM_NUMBER = 587


class EmailServer:

    def SendEmail(self: bool, subject: str, fromEmail: str, toEmail: str, messageContent: str):
        email_server = smtplib.SMTP(_EMAIL_SERVER_SECRET_PLATFORM, _EMAIL_SERVER_SECRET_PLATFORM_NUMBER)
        email_server.starttls()
        email_server.login(_EMAIL_SERVER_SECRET_USERNAME, _EMAIL_SERVER_SECRET_APP_PASSWORD)
        message = EmailMessage()
        message['Subject'] = subject
        message['From'] = fromEmail
        if self: message['To'] = _EMAIL_SERVER_SECRET_USERNAME
        else: message['To'] = toEmail
        message.set_content(messageContent)
        email_server.send_message(message)