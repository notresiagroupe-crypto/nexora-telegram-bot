# scrapers/instagram_scraper.py
# ══════════════════════════════════════════
# Recherche prospects Instagram & LinkedIn
# + génération des messages DM
# ══════════════════════════════════════════

import requests
import time
import json
from bs4 import BeautifulSoup
from config.settings import TARGET_SECTORS, TARGET_CITY, DELAY_BETWEEN_REQUESTS
from messaging.templates import get_instagram_dm, get_linkedin_message, get_malt_message

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    "Accept-Language": "fr-FR,fr;q=0.9",
}


def find_instagram_prospects():
    """
    Trouve des prospects Instagram via Google
    (recherche de comptes Instagram de PME locales)
    """
    prospects = []
    
    print("\n📸 Recherche prospects Instagram...")
    
    searches = [
        f"site:instagram.com restaurant {TARGET_CITY}",
        f"site:instagram.com salon coiffure {TARGET_CITY}",
        f"site:instagram.com boutique mode {TARGET_CITY}",
        f"site:instagram.com institut beauté {TARGET_CITY}",
        f"site:instagram.com food {TARGET_CITY}",
    ]
    
    for query in searches:
        try:
            url = f"https://www.google.fr/search?q={requests.utils.quote(query)}&num=8&hl=fr"
            resp = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            
            for g in soup.find_all("div", class_="g"):
                link = g.find("a")
                title_el = g.find("h3")
                if link and title_el:
                    href = link.get("href", "")
                    title = title_el.text.strip()
                    if "instagram.com" in href and "/p/" not in href:
                        # Extrait le handle Instagram
                        handle = href.split("instagram.com/")[-1].strip("/").split("/")[0].split("?")[0]
                        if handle and len(handle) > 2 and "." not in handle:
                            # Détecte le secteur
                            sector = "restaurant"
                            for s, config in TARGET_SECTORS.items():
                                if any(kw in title.lower() for kw in config["keywords"]):
                                    sector = s
                                    break
                            
                            prospect = {
                                "name": title,
                                "instagram_handle": f"@{handle}",
                                "instagram_url": f"https://instagram.com/{handle}",
                                "sector": sector,
                                "source": "Instagram",
                                "city": TARGET_CITY,
                                "status": "À contacter",
                                "dm_message": get_instagram_dm(sector, title)
                            }
                            
                            # Évite les doublons
                            if not any(p["instagram_handle"] == prospect["instagram_handle"] for p in prospects):
                                prospects.append(prospect)
                                print(f"   ✓ {prospect['instagram_handle']} — {title[:40]}")
            
            time.sleep(DELAY_BETWEEN_REQUESTS)
        
        except Exception as e:
            print(f"   [Instagram] Erreur: {e}")
    
    print(f"   → {len(prospects)} comptes Instagram trouvés\n")
    return prospects


def find_linkedin_prospects():
    """
    Trouve des gérants/directeurs de PME sur LinkedIn
    via Google (site:linkedin.com)
    """
    prospects = []
    
    print("\n💼 Recherche prospects LinkedIn...")
    
    searches = [
        f"site:linkedin.com/in gérant restaurant {TARGET_CITY}",
        f"site:linkedin.com/in directeur boutique {TARGET_CITY}",
        f"site:linkedin.com/in fondatrice salon beauté {TARGET_CITY}",
        f"site:linkedin.com/in entrepreneur {TARGET_CITY} PME",
        f"site:linkedin.com/company restaurant {TARGET_CITY}",
    ]
    
    for query in searches:
        try:
            url = f"https://www.google.fr/search?q={requests.utils.quote(query)}&num=5&hl=fr"
            resp = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            
            for g in soup.find_all("div", class_="g"):
                link = g.find("a")
                title_el = g.find("h3")
                desc_el = g.find("div", class_="VwiC3b")
                
                if link and title_el and "linkedin.com" in link.get("href", ""):
                    href = link.get("href", "")
                    title = title_el.text.strip()
                    desc = desc_el.text.strip() if desc_el else ""
                    
                    # Extrait prénom depuis le titre
                    first_name = title.split()[0] if title else "Bonjour"
                    
                    sector = "boutique"
                    for s, config in TARGET_SECTORS.items():
                        if any(kw in (title + desc).lower() for kw in config["keywords"]):
                            sector = s
                            break
                    
                    prospect = {
                        "name": title,
                        "linkedin_url": href,
                        "sector": sector,
                        "source": "LinkedIn",
                        "city": TARGET_CITY,
                        "status": "À contacter",
                        "connection_message": get_linkedin_message(sector, first_name, title)
                    }
                    
                    if not any(p.get("linkedin_url") == href for p in prospects):
                        prospects.append(prospect)
                        print(f"   ✓ {title[:50]}")
            
            time.sleep(DELAY_BETWEEN_REQUESTS + 1)
        
        except Exception as e:
            print(f"   [LinkedIn] Erreur: {e}")
    
    print(f"   → {len(prospects)} profils LinkedIn trouvés\n")
    return prospects


def find_malt_prospects():
    """
    Trouve des missions disponibles sur Malt
    via scraping de la liste des projets
    """
    prospects = []
    
    print("\n🧑‍💻 Recherche missions Malt...")
    
    searches = [
        "site:malt.fr mission développeur web react",
        "site:malt.fr mission automatisation IA python",
        "site:malt.fr mission création site wordpress",
        "site:malt.fr mission développeur fullstack",
    ]
    
    for query in searches:
        try:
            url = f"https://www.google.fr/search?q={requests.utils.quote(query)}&num=5&hl=fr"
            resp = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            
            for g in soup.find_all("div", class_="g"):
                link = g.find("a")
                title_el = g.find("h3")
                desc_el = g.find("div", class_="VwiC3b")
                
                if link and title_el and "malt.fr" in link.get("href", ""):
                    href = link.get("href", "")
                    title = title_el.text.strip()
                    desc = desc_el.text.strip() if desc_el else ""
                    
                    prospect = {
                        "name": title,
                        "malt_url": href,
                        "description": desc[:200],
                        "source": "Malt",
                        "status": "À contacter",
                        "dm_message": get_malt_message("", desc[:100])
                    }
                    
                    if not any(p.get("malt_url") == href for p in prospects):
                        prospects.append(prospect)
                        print(f"   ✓ {title[:50]}")
            
            time.sleep(DELAY_BETWEEN_REQUESTS)
        
        except Exception as e:
            print(f"   [Malt] Erreur: {e}")
    
    print(f"   → {len(prospects)} missions Malt trouvées\n")
    return prospects
