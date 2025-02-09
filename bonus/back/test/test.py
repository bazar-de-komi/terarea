import base64

# Le message MIME brut (sans signature)
raw_message = """From: "Me" <noreply.terarea@gmail.com>
To: "Recipient" <kulius999@gmail.com>
Subject: Test Email
MIME-Version: 1.0
Content-Type: text/plain; charset="UTF-8"

Hello, this is a test email!"""

# Encoder en base64
base64_bytes = base64.urlsafe_b64encode(raw_message.encode("utf-8"))
base64_message = base64_bytes.decode("utf-8")

print(base64_message)
