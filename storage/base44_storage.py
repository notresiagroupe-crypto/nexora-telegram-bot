# storage/base44_storage.py
# ══════════════════════════════════════════
# Sauvegarde des prospects dans Base44 CRM
# ══════════════════════════════════════════

import requests
import json
from datetime import datetime
from config.settings import BASE44_APP_ID

BASE44_API = "https://api.base44.com/api/apps"

def get_headers():
    return {
        "Content-Type": "application/json",
        "app-id": BASE44_APP_ID
    }


def save_prospect(prospect):
    """Sauvegarde un prospect dans Base44"""
    try:
        data = {
            "name": prospect.get("name", "Inconnu"),
            "sector": prospect.get("sector", ""),
            "source": prospect.get("source", ""),
            "email": prospect.get("email", ""),
            "phone": prospect.get("phone", ""),
            "website": prospect.get("website", ""),
            "instagram": prospect.get("instagram_handle", ""),
            "linkedin": prospect.get("linkedin_url", ""),
            "malt": prospect.get("malt_url", ""),
            "city": prospect.get("city", "Bordeaux"),
            "status": prospect.get("status", "Nouveau"),
            "email_sent": prospect.get("email_sent", False),
            "notes": prospect.get("notes", ""),
            "dm_message": prospect.get("dm_message", ""),
            "created_at": datetime.now().isoformat()
        }
        
        resp = requests.post(
            f"{BASE44_API}/{BASE44_APP_ID}/entities/Prospect",
            headers=get_headers(),
            json=data,
            timeout=10
        )
        
        if resp.status_code in [200, 201]:
            return True
        else:
            print(f"   [Base44] Erreur save: {resp.status_code} — {resp.text[:100]}")
            return False
    
    except Exception as e:
        print(f"   [Base44] Exception: {e}")
        return False


def save_all_prospects(prospects):
    """Sauvegarde une liste de prospects"""
    saved = 0
    for p in prospects:
        if save_prospect(p):
            saved += 1
    print(f"   💾 {saved}/{len(prospects)} prospects sauvegardés dans Base44")
    return saved


def get_prospects_stats():
    """Récupère les stats du CRM"""
    try:
        resp = requests.get(
            f"{BASE44_API}/{BASE44_APP_ID}/entities/Prospect",
            headers=get_headers(),
            timeout=10
        )
        if resp.status_code == 200:
            prospects = resp.json()
            total = len(prospects)
            emailed = sum(1 for p in prospects if p.get("email_sent"))
            replied = sum(1 for p in prospects if p.get("status") == "Répondu")
            signed = sum(1 for p in prospects if p.get("status") == "Signé")
            return {
                "total": total,
                "emailed": emailed,
                "replied": replied,
                "signed": signed,
                "conversion_rate": f"{(signed/total*100):.1f}%" if total > 0 else "0%"
            }
    except Exception as e:
        print(f"   [Base44] Stats error: {e}")
    return {"total": 0, "emailed": 0, "replied": 0, "signed": 0, "conversion_rate": "0%"}
