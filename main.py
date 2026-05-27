# main.py
# ══════════════════════════════════════════
# NEXORA Studio — Système de Prospection
# Orchestrateur principal
# ══════════════════════════════════════════
# 
# SETUP REQUIS (variables .env) :
#   GMAIL_EMAIL=zambolionel043@gmail.com
#   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
#   (Activer mot de passe app Gmail :
#    myaccount.google.com > Sécurité > 
#    Mots de passe des applications)
#
# LANCEMENT :
#   python main.py          → Lance une prospection maintenant
#   python main.py --report → Rapport uniquement
#   python main.py --daemon → Mode démon (tourne 24/7)
# ══════════════════════════════════════════

import sys
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from config.settings import REPORT_HOUR, MAX_PROSPECTS_PER_DAY
from scrapers.google_scraper import find_all_prospects
from scrapers.instagram_scraper import find_instagram_prospects, find_linkedin_prospects, find_malt_prospects
from messaging.email_sender import send_prospection_emails
from storage.base44_storage import save_all_prospects, get_prospects_stats
from reports.daily_report import send_daily_report


def run_prospection():
    """Lance un cycle complet de prospection"""
    
    print("\n" + "="*60)
    print(f"🚀 NEXORA PROSPECTION — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("="*60)
    
    # ── 1. Recherche Google → Emails ─────────────────────────
    print("\n[1/5] Recherche prospects Google...")
    google_prospects = find_all_prospects(limit_per_sector=6)
    
    # ── 2. Envoi emails automatiques ─────────────────────────
    print("\n[2/5] Envoi emails de prospection...")
    if google_prospects:
        email_results, sent, failed = send_prospection_emails(
            google_prospects, 
            max_emails=MAX_PROSPECTS_PER_DAY
        )
    else:
        email_results, sent, failed = [], 0, 0
        print("   Aucun email à envoyer")
    
    # ── 3. Recherche Instagram ────────────────────────────────
    print("\n[3/5] Recherche prospects Instagram...")
    insta_prospects = find_instagram_prospects()
    
    # ── 4. Recherche LinkedIn + Malt ─────────────────────────
    print("\n[4/5] Recherche LinkedIn & Malt...")
    linkedin_prospects = find_linkedin_prospects()
    malt_prospects = find_malt_prospects()
    
    # ── 5. Sauvegarde dans Base44 ─────────────────────────────
    print("\n[5/5] Sauvegarde dans le CRM Base44...")
    all_to_save = email_results + insta_prospects + linkedin_prospects + malt_prospects
    save_all_prospects(all_to_save)
    
    # ── Rapport final ─────────────────────────────────────────
    stats = get_prospects_stats()
    
    print("\n" + "="*60)
    print(f"✅ CYCLE TERMINÉ")
    print(f"   Emails envoyés  : {sent}")
    print(f"   Instagram trouvés: {len(insta_prospects)}")
    print(f"   LinkedIn trouvés : {len(linkedin_prospects)}")
    print(f"   Missions Malt   : {len(malt_prospects)}")
    print(f"   Total CRM       : {stats.get('total', 0)} prospects")
    print("="*60 + "\n")
    
    return google_prospects, insta_prospects, linkedin_prospects, malt_prospects, stats


def run_daily_report():
    """Envoie le rapport quotidien (appelé à 7h00)"""
    print(f"\n📊 Génération rapport quotidien — {datetime.now().strftime('%H:%M')}")
    google_p, insta_p, linkedin_p, malt_p, stats = run_prospection()
    send_daily_report(stats, google_p, insta_p, linkedin_p, malt_p)


def keep_alive():
    """Ping pour garder Replit actif"""
    print(f"💓 Keep-alive — {datetime.now().strftime('%H:%M:%S')}")


if __name__ == "__main__":
    args = sys.argv[1:]
    
    if "--report" in args:
        # Rapport uniquement
        stats = get_prospects_stats()
        send_daily_report(stats, [], [], [], [])
    
    elif "--daemon" in args:
        # Mode démon — tourne en continu
        print(f"\n⚡ Mode démon activé")
        print(f"   Prospection quotidienne à {REPORT_HOUR}h00")
        print(f"   Keep-alive toutes les 5 minutes\n")
        
        # Schedule quotidien
        schedule.every().day.at(f"{REPORT_HOUR:02d}:00").do(run_daily_report)
        
        # Keep-alive Replit (toutes les 5 min)
        schedule.every(5).minutes.do(keep_alive)
        
        # Lance une première fois immédiatement
        print("🔄 Premier cycle au démarrage...")
        run_daily_report()
        
        # Boucle infinie
        while True:
            schedule.run_pending()
            time.sleep(30)
    
    else:
        # Mode manuel — un seul cycle
        google_p, insta_p, linkedin_p, malt_p, stats = run_prospection()
        send_daily_report(stats, google_p, insta_p, linkedin_p, malt_p)
