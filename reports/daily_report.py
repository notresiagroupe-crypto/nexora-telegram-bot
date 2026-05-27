# reports/daily_report.py
# ══════════════════════════════════════════
# Rapport quotidien envoyé à 7h00
# ══════════════════════════════════════════

import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import GMAIL_EMAIL, GMAIL_APP_PASSWORD, NEXORA_AGENCY


def send_daily_report(stats, new_prospects, instagram_prospects, linkedin_prospects, malt_prospects):
    """Génère et envoie le rapport quotidien"""
    
    today = datetime.now().strftime("%d/%m/%Y")
    
    # ── Construit le rapport ──────────────────────
    report_lines = []
    
    report_lines.append(f"🚀 NEXORA Studio — Rapport Prospection du {today}")
    report_lines.append("=" * 50)
    report_lines.append("")
    
    # Stats globales CRM
    report_lines.append("📊 TABLEAU DE BORD CRM")
    report_lines.append(f"   Total prospects : {stats.get('total', 0)}")
    report_lines.append(f"   Emails envoyés  : {stats.get('emailed', 0)}")
    report_lines.append(f"   Réponses reçues : {stats.get('replied', 0)}")
    report_lines.append(f"   Contrats signés : {stats.get('signed', 0)}")
    report_lines.append(f"   Taux conversion : {stats.get('conversion_rate', '0%')}")
    report_lines.append("")
    
    # Prospects trouvés aujourd'hui
    report_lines.append(f"🆕 NOUVEAUX PROSPECTS AUJOURD'HUI ({len(new_prospects)})")
    if new_prospects:
        for p in new_prospects[:10]:
            email_icon = "✉️" if p.get("email_sent") else "⏳"
            report_lines.append(f"   {email_icon} {p.get('name', '?')[:35]} | {p.get('sector', '')} | {p.get('email', 'no email')}")
    else:
        report_lines.append("   Aucun nouveau prospect aujourd'hui")
    report_lines.append("")
    
    # Instagram
    report_lines.append(f"📸 PROSPECTS INSTAGRAM ({len(instagram_prospects)})")
    if instagram_prospects:
        for p in instagram_prospects[:8]:
            report_lines.append(f"   → {p.get('instagram_handle', '')} | {p.get('name', '')[:30]}")
        report_lines.append("")
        report_lines.append("   💡 Messages DM prêts dans le CRM Base44")
    else:
        report_lines.append("   Aucun trouvé aujourd'hui")
    report_lines.append("")
    
    # LinkedIn
    report_lines.append(f"💼 PROSPECTS LINKEDIN ({len(linkedin_prospects)})")
    if linkedin_prospects:
        for p in linkedin_prospects[:5]:
            report_lines.append(f"   → {p.get('name', '')[:40]}")
            report_lines.append(f"     {p.get('linkedin_url', '')[:60]}")
    else:
        report_lines.append("   Aucun trouvé aujourd'hui")
    report_lines.append("")
    
    # Malt
    report_lines.append(f"🧑‍💻 MISSIONS MALT ({len(malt_prospects)})")
    if malt_prospects:
        for p in malt_prospects[:5]:
            report_lines.append(f"   → {p.get('name', '')[:50]}")
    else:
        report_lines.append("   Aucune mission trouvée aujourd'hui")
    report_lines.append("")
    
    # Actions prioritaires
    report_lines.append("⚡ ACTIONS PRIORITAIRES AUJOURD'HUI")
    
    if instagram_prospects:
        report_lines.append(f"   1. Envoyer les {len(instagram_prospects)} DMs Instagram depuis Base44")
    if linkedin_prospects:
        report_lines.append(f"   2. Envoyer les {len(linkedin_prospects)} messages LinkedIn")
    if malt_prospects:
        report_lines.append(f"   3. Postuler aux {len(malt_prospects)} missions Malt")
    
    report_lines.append("")
    report_lines.append("=" * 50)
    report_lines.append(f"🎯 Accès CRM : https://app.base44.com/apps/69cfbd6c4ad311d1ec530908")
    report_lines.append(f"🌐 Site NEXORA : https://notresiagroupe-crypto.github.io/nexora/")
    report_lines.append("")
    report_lines.append("Bonne journée Lionel ! 💪")
    
    report_text = "\n".join(report_lines)
    
    # ── Envoie l'email ──────────────────────────
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📊 NEXORA — Rapport Prospection {today} | {len(new_prospects)} nouveaux prospects"
        msg["From"] = f"NEXORA Bot <{GMAIL_EMAIL}>"
        msg["To"] = GMAIL_EMAIL
        
        # HTML version
        html_lines = report_text.replace("\n", "<br>").replace("  ", "&nbsp;&nbsp;")
        html = f"""
        <html><body style="font-family:monospace;background:#0f0f13;color:#eeeef2;padding:24px;max-width:600px">
        <div style="background:#18181f;border:1px solid #2a2a35;border-radius:12px;padding:20px;border-top:3px solid #f0c040">
        <pre style="color:#eeeef2;font-size:13px;line-height:1.7;margin:0;white-space:pre-wrap">{report_text}</pre>
        </div>
        </body></html>
        """
        
        msg.attach(MIMEText(report_text, "plain", "utf-8"))
        msg.attach(MIMEText(html, "html", "utf-8"))
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_EMAIL, GMAIL_EMAIL, msg.as_string())
        
        print(f"\n📬 Rapport quotidien envoyé à {GMAIL_EMAIL}")
        return True
    
    except Exception as e:
        print(f"\n❌ Erreur envoi rapport: {e}")
        # Affiche quand même dans la console
        print("\n" + report_text)
        return False
