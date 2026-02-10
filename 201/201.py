import smtplib
import requests
import logging
from email.mime.text import MIMEText
from datetime import datetime
from enum import Enum

# ---------------- CONFIG ---------------- #

ADMIN_EMAIL = "admin@example.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "alert@example.com"
SMTP_PASS = "APP_PASSWORD"

TELEGRAM_BOT_TOKEN = "BOT_TOKEN"
TELEGRAM_CHAT_ID = "CHAT_ID"

logging.basicConfig(
    filename="security.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class Severity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AlertManager:

    @staticmethod
    def send_email(subject: str, message: str):
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = ADMIN_EMAIL

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

    @staticmethod
    def send_telegram(message: str):
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        requests.post(url, json=payload, timeout=5)

    @staticmethod
    def alert(severity: Severity, title: str, details: str):
        timestamp = datetime.utcnow().isoformat()

        full_message = f"""
🚨 SECURITY ALERT 🚨

Severity : {severity.value}
Title    : {title}
Time     : {timestamp}

Details:
{details}
"""

        logging.warning(full_message)

        # always telegram
        AlertManager.send_telegram(full_message)

        # email only for high risk
        if severity in {Severity.HIGH, Severity.CRITICAL}:
            AlertManager.send_email(
                subject=f"[{severity.value}] {title}",
                message=full_message
            )


class SuspiciousActivityDetector:

    FAILED_LOGIN_THRESHOLD = 5

    def __init__(self):
        self.failed_logins = {}

    def login_failed(self, ip_address: str):
        self.failed_logins[ip_address] = self.failed_logins.get(ip_address, 0) + 1

        if self.failed_logins[ip_address] >= self.FAILED_LOGIN_THRESHOLD:
            AlertManager.alert(
                severity=Severity.HIGH,
                title="Multiple Failed Login Attempts",
                details=f"IP {ip_address} exceeded failed login limit."
            )

    def access_forbidden_resource(self, user_id: str, resource: str):
        AlertManager.alert(
            severity=Severity.CRITICAL,
            title="Unauthorized Resource Access",
            details=f"User {user_id} tried to access {resource}"
        )


# ---------------- EXAMPLE USAGE ---------------- #

detector = SuspiciousActivityDetector()

detector.login_failed("192.168.1.10")
detector.login_failed("192.168.1.10")
detector.login_failed("192.168.1.10")
detector.login_failed("192.168.1.10")
detector.login_failed("192.168.1.10")

detector.access_forbidden_resource(
    user_id="user_42",
    resource="/admin/panel"
)
