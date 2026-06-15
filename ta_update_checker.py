import re
import requests
import smtplib
from email.message import EmailMessage
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

# ----------------------------
# Configuracion
# ----------------------------

URL = "https://help.fieldsystems.trimble.com/trimble-access-release-notes/es/home.htm"
STATE_FILE = Path("last_version.txt")

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587

# email
MAIL_USER = "mail"
MAIL_PASSWORD = "pass"
MAIL_TO = ["mail1@ejemplo.com", "mail2@ejemplo.com"]
# ----------------------------
# Funcion de Email
# ----------------------------

def send_email(version):
    msg = EmailMessage()
    msg["Subject"] = f"Nueva versión de Trimble Access disponible: {version}"
    msg["From"] = MAIL_USER
    msg["To"] = MAIL_TO

    msg.set_content(
        f"""
Se ha detectado una nueva versión de Trimble Access.

Versión: {version}

Release Notes:
{URL}

Hora de detección:
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Este mensaje ha sido generado automáticamente.
"""
    )

    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(MAIL_USER, MAIL_PASSWORD)
        smtp.send_message(msg, from_addr=MAIL_USER, to_addrs=MAIL_TO)


# ----------------------------
# Chequear ultima version
# ----------------------------

def get_latest_version():
    headers = {
        "User-Agent": "TrimbleReleaseMonitor/1.0"
    }

    r = requests.get(
        URL,
        headers=headers,
        timeout=15
    )
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    matches = [m.strip() for m in re.findall(r"\b20\d{2}\.\d+\b", text)]

    if not matches:
        raise RuntimeError(
            "No se pudo determinar la última versión."
        )

    latest = max(matches, key=lambda v: tuple(map(int, v.split("."))))

    return latest


# ----------------------------
# Logica principal
# ----------------------------

try:
    latest = get_latest_version()

    previous = (
        STATE_FILE.read_text().strip()
        if STATE_FILE.exists()
        else None
    )

    # Inicializar (Crea .txt de ultima version)
    if previous is None:
        STATE_FILE.write_text(latest)
        print(
            f"[{datetime.now()}] "
            f"Inicializado con la versión {latest}"
        )

    # Nueva version
    elif latest != previous:
        send_email(latest)
        STATE_FILE.write_text(latest)
        print(
            f"[{datetime.now()}] "
            f"Nueva versión detectada: {latest}"
        )

    # Sin cambios
    else:
        print(
            f"[{datetime.now()}] "
            f"Sin cambios. Versión actual: {latest}"
        )

except Exception as e:
    print(
        f"[{datetime.now()}] ERROR: {e}"
    )