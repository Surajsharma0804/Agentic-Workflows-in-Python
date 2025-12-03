"""Email sending plugin."""
from ..base import PluginBase
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailPlugin(PluginBase):
    """Email sending via SMTP."""
    
    name = "email"
    
    def __init__(self, params: dict, audit=None):
        super().__init__(params, audit=audit)
        self.smtp_host = params.get("smtp_host")
        self.smtp_port = params.get("smtp_port", 587)
        self.smtp_username = params.get("smtp_username")
        self.smtp_password = params.get("smtp_password")
        self.from_email = params.get("from_email")
        self.to_email = params.get("to_email")
        self.subject = params.get("subject")
        self.body = params.get("body")
        self.html = params.get("html", False)
    
    def plan(self) -> list:
        return [{"action": "send_email", "to": self.to_email, "subject": self.subject}]
    
    def execute(self) -> dict:
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self.subject
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            
            if self.html:
                part = MIMEText(self.body, 'html')
            else:
                part = MIMEText(self.body, 'plain')
            
            msg.attach(part)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            if self.audit:
                self.audit.record({
                    "plugin": self.name,
                    "to": self.to_email,
                    "subject": self.subject
                })
            
            return {"status": "ok", "message": "Email sent"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
