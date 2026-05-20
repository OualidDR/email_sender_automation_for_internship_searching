import pandas as pd
import smtplib
import os
import time
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

sender_email = os.getenv("EMAIL_USER")
app_password = os.getenv("EMAIL_PASSWORD")

# =========================
# LOAD CSV
# =========================

df = pd.read_csv("data/database.csv")

# =========================
# EMAIL CONTENT
# =========================

subject = "Demande de stage de 2 mois – Étudiant ENSIAS"

body = """
Bonjour,

Je suis étudiant en 2ème année à l’ENSIAS (Data Engineering).

Je suis actuellement à la recherche d’un stage de 2 mois afin de développer mes compétences et renforcer mon expérience professionnelle.

Veuillez trouver ci-joint mon CV.

Cordialement,
Votre Nom
"""

cv_path = "CV.pdf"

# =========================
# SMTP SETUP
# =========================

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender_email, app_password)

# =========================
# SEND EMAILS
# =========================

for recipient in df["email"]:

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # attach CV
    with open(cv_path, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype="pdf")
        attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=os.path.basename(cv_path)
        )
        msg.attach(attachment)

    try:
        server.sendmail(sender_email, recipient, msg.as_string())
        print(f"Sent to {recipient}")
        time.sleep(2)

    except Exception as e:
        print(f"Failed {recipient}: {e}")

server.quit()