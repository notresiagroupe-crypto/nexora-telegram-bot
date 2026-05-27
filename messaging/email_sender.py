# messaging/email_sender.py
# ══════════════════════════════════════════
# Envoi automatique d'emails aux prospects
# via Gmail SMTP
# ══════════════════════════════════════════

import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import GMAIL_EMAIL, GMAIL_APP_PASSWORD, DELAY_BETWEEN_EMAILS
from messaging.templates import get_email_template


def send_email(to_email, subject, body, from_name="Lionel — NEXORA Studio"):
    """Envoie un email via Gmail SMTP"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{from_name} <{GMAIL_EMAIL}>"
        msg["To"] = to_email
        msg["Reply-To"] = GMAIL_EMAIL

        # Version texte
        part1 = MIMEText(body, "plain", "utf-8")
        
        # Version HTML (mise en forme)
        html_body = body.replace("\n", "<br>").replace("✅", "✓").replace("🍽️", "").replace("💅", "").replace("🛍️", "").replace("🚀", "")
        html = f"""
        <html><body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#333">
        <div style="border-left:4px solid #f0c040;padding-left:20px">
        {html_body}
        </div>
        <hr style="margin-top:30px;border:none;border-top:1px solid #eee">
        <p style="font-size:12px;color:#999">
        Vous recevez ce message car votre établissement apparaît dans nos recherches locales.<br>
        Pour ne plus recevoir nos messages, répondez simplement "STOP".
        </p>
        </body></html>
        """
        part2 = MIMEText(html, "html", "utf-8")
        
        msg.attach(part1)
        msg.attach(part2)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_EMAIL, to_email, msg.as_string())
        
        print(f"   ✉️ Email envoyé → {to_email}")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur email {to_email}: {e}")
        return False


def send_prospection_emails(prospects, max_emails=20):
    """Envoie les emails de prospection à une liste de prospects"""
    sent = 0
    failed = 0
    results = []

    print(f"\n📤 Envoi des emails de prospection ({min(len(prospects), max_emails)} max)...")

    for prospect in prospects[:max_emails]:
        email = prospect.get("email")
        if not email:
            continue

        sector = prospect.get("sector", "restaurant")
        name = prospect.get("name", "votre établissement")
        city = prospect.get("city", "Bordeaux")

        template = get_email_template(sector, name, city)
        subject = template["subject"]
        body = template["body"]

        success = send_email(email, subject, body)
        
        result = {
            **prospect,
            "email_sent": success,
            "email_status": "Envoyé" if success else "Échec"
        }
        results.append(result)

        if success:
            sent += 1
        else:
            failed += 1

        # Pause entre emails
        if success:
            time.sleep(DELAY_BETWEEN_EMAILS)

    print(f"\n   ✅ Emails envoyés: {sent}")
    print(f"   ❌ Échecs: {failed}")
    
    return results, sent, failed
