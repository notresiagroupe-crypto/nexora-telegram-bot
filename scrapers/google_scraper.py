# scrapers/google_scraper.py
# ══════════════════════════════════════════
# Recherche automatique de prospects
# via Google Search
# ══════════════════════════════════════════

import requests
import time
import re
import json
from bs4 import BeautifulSoup
from config.settings import TARGET_SECTORS, TARGET_CITY, DELAY_BETWEEN_REQUESTS

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

def search_google(query, num_results=10):
    """Recherche Google et retourne les URLs trouvées"""
    results = []
    try:
        url = f"https://www.google.fr/search?q={requests.utils.quote(query)}&num={num_results}&hl=fr"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        
        for g in soup.find_all("div", class_="g"):
            link = g.find("a")
            title_el = g.find("h3")
            if link and title_el:
                href = link.get("href", "")
                title = title_el.text.strip()
                if href.startswith("http") and "google" not in href:
                    results.append({"url": href, "title": title})
        
        time.sleep(DELAY_BETWEEN_REQUESTS)
    except Exception as e:
        print(f"[Google] Erreur: {e}")
    
    return results


def extract_contact_from_website(url):
    """Extrait email, téléphone et nom depuis un site web"""
    contact = {
        "email": None,
        "phone": None,
        "address": None,
        "name": None
    }
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()
        
        # Email
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        # Filtre les emails génériques
        bad_emails = ["example", "test", "noreply", "wordpress", "jquery", "schema"]
        clean_emails = [e for e in emails if not any(b in e.lower() for b in bad_emails)]
        if clean_emails:
            contact["email"] = clean_emails[0]
        
        # Téléphone (format français)
        phones = re.findall(r'(?:(?:\+33|0033|0)[1-9](?:[.\-\s]?\d{2}){4})', text)
        if phones:
            contact["phone"] = phones[0].replace(" ", "").replace(".", "").replace("-", "")
        
        # Titre de la page = nom du business
        title = soup.find("title")
        if title:
            contact["name"] = title.text.strip()[:60]
        
        # Adresse (cherche la balise adresse ou schema)
        address_tag = soup.find("address")
        if address_tag:
            contact["address"] = address_tag.text.strip()[:100]
        
        time.sleep(1)
    except Exception as e:
        print(f"[Extract] Erreur sur {url}: {e}")
    
    return contact


def find_prospects_by_sector(sector, limit=10):
    """Trouve des prospects pour un secteur donné"""
    prospects = []
    sector_config = TARGET_SECTORS.get(sector, {})
    keywords = sector_config.get("keywords", [sector])
    
    print(f"\n🔍 Recherche de prospects — Secteur: {sector}")
    
    for keyword in keywords[:3]:  # Top 3 keywords par secteur
        query = f"{keyword} {TARGET_CITY} site contact"
        print(f"   Recherche: {query}")
        
        results = search_google(query, num_results=5)
        
        for result in results:
            url = result["url"]
            title = result["title"]
            
            # Évite les annuaires et grands groupes
            skip_domains = ["pages-jaunes", "tripadvisor", "facebook", "instagram",
                          "google", "yelp", "lafourchette", "opentable", "linkedin"]
            if any(d in url.lower() for d in skip_domains):
                continue
            
            print(f"   ✓ Trouvé: {title[:40]} — {url[:50]}")
            contact = extract_contact_from_website(url)
            
            prospect = {
                "name": contact["name"] or title,
                "website": url,
                "sector": sector,
                "email": contact["email"],
                "phone": contact["phone"],
                "address": contact["address"],
                "city": TARGET_CITY,
                "source": "Google",
                "keyword": keyword,
                "status": "Nouveau",
                "notes": f"Trouvé via: {query}"
            }
            
            # N'ajoute que si email trouvé
            if contact["email"]:
                prospects.append(prospect)
                print(f"   📧 Email trouvé: {contact['email']}")
            
            if len(prospects) >= limit:
                break
        
        if len(prospects) >= limit:
            break
    
    print(f"   → {len(prospects)} prospects avec email trouvés\n")
    return prospects


def find_all_prospects(limit_per_sector=8):
    """Lance la recherche sur tous les secteurs"""
    all_prospects = []
    
    for sector in TARGET_SECTORS.keys():
        prospects = find_prospects_by_sector(sector, limit=limit_per_sector)
        all_prospects.extend(prospects)
    
    # Déduplique par email
    seen_emails = set()
    unique = []
    for p in all_prospects:
        if p["email"] and p["email"] not in seen_emails:
            seen_emails.add(p["email"])
            unique.append(p)
    
    print(f"✅ Total prospects uniques trouvés: {len(unique)}")
    return unique
