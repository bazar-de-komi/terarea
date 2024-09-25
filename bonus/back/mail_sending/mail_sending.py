import os
import ssl
import dotenv
import smtplib
from email.message import EmailMessage

dotenv.load_dotenv()
API_KEY = os.getenv('APP_PASSWORD')
SENDER = "noreply.terarea@gmail.com"
RECEIVER = input("Destination e-mail:")

subject = "test email"
body = """
<h1>This is s a test e-mail.</h1>
"""

EM = EmailMessage()

EM['From'] = SENDER
EM['To'] = RECEIVER
EM['Subject'] = subject
EM.add_alternative(body, subtype="html")

CONTEXT = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=CONTEXT) as smtp:
        smtp.login(SENDER, API_KEY)
        smtp.sendmail(SENDER, RECEIVER, EM.as_string())
        print("Email sent successfully")
except Exception as e:
    print(f"An error occurred: {e}")
