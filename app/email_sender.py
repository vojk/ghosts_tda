from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(receiver_email, receiver_lastname, receiver_username, receiver_password):
    load_dotenv('app/.env')
    # Create a multipart message
    message = MIMEMultipart()
    print(os.environ.get('SMTP_USERNAME'))
    message["From"] = os.environ.get('SMTP_USERNAME')
    message["To"] = receiver_email
    message["Subject"] = "Přihlašovací údaje do služby záznamník pro programátory"
    body = """<html lang="cs">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed&display=swap" rel="stylesheet">
</head>
<body>
<div style="margin: 2rem">
    <div style="font-family: 'Roboto Condensed', sans-serif;">
        <div>
            <p style="margin: 0">Dobrý den, """ + receiver_lastname + """,</p>
            <p style="margin: 0">posíláme Vám Vaše přihlašovací údaje do aplikace "Záznamník pro programátory":</p>
            <p><span style="font-weight: 700">E-mail:</span> """ + receiver_email + """</p>
            <p><span style="font-weight: 700">Uživatelské jméno:</span> """ + receiver_username + """</p>
            <p><span style="font-weight: 700">Heslo:</span> """ + receiver_password + """</p>
        </div>

        <div>
            <p style="margin: 0">Pokud tento e-mail Vám přišel a nenáleží Vám, tak ho prosím ignorujte.</p>
            <p style="margin: 0">Prosíme, na tento e-mail neodpovídat.</p>
        </div>
    </div>

    <div style="font-family: 'Roboto Condensed', sans-serif;">
        <p style="font-weight: 100; color: gray; font-size: 0.8rem; margin-top: 1.5rem">&copy; Ghosts 2023</p>
    </div>
</div>
</body>
</html>"""

    # Add body to the message
    message.attach(MIMEText(body, "html"))

    # Connect to SMTP server and send email
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(os.environ.get('SMTP_USERNAME'), os.environ.get('SMTP_PASSWORD'))
        server.send_message(message)
