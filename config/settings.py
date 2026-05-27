# config/settings.py
import os

# ══════════════════════════════════════════
# NEXORA Studio — Prospection Automatique
# Configuration centrale
# ══════════════════════════════════════════

# Identité NEXORA
NEXORA_NAME = "Lionel"
NEXORA_AGENCY = "NEXORA Studio"
NEXORA_EMAIL = "zambolionel043@gmail.com"
NEXORA_WEBSITE = "https://notresiagroupe-crypto.github.io/nexora/"
NEXORA_INSTAGRAM = "@id_lionel"
NEXORA_PHONE = ""  # Ajouter si souhaité

# Cible géographique
TARGET_CITY = "Bordeaux"
TARGET_REGION = "Gironde"

# Secteurs cibles
TARGET_SECTORS = {
    "restaurant": {
        "keywords": ["restaurant", "brasserie", "bistrot", "café", "traiteur", "pizzeria", "sushi", "burger", "food"],
        "pain_points": "visibilité en ligne, réservations, menu digital",
        "offer": "site web + menu en ligne + système de réservation"
    },
    "beaute": {
        "keywords": ["salon coiffure", "institut beauté", "esthétique", "nail art", "spa", "barbier", "onglerie"],
        "pain_points": "prise de rendez-vous, visibilité locale, présence Instagram",
        "offer": "site web + système de RDV en ligne + gestion Instagram IA"
    },
    "boutique": {
        "keywords": ["boutique", "magasin", "prêt-à-porter", "mode", "décoration", "concept store", "épicerie fine"],
        "pain_points": "ventes en ligne, catalogue digital, concurrence Amazon",
        "offer": "site e-commerce + automatisation catalogue + stratégie digitale"
    }
}

# Gmail SMTP (à configurer dans .env)
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL", NEXORA_EMAIL)
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")  # Mot de passe d'application Gmail

# Base44 API
BASE44_API_KEY = os.getenv("BASE44_API_KEY", "")
BASE44_APP_ID = "69cfbd6c4ad311d1ec530908"

# Limites quotidiennes (pour éviter les bans)
MAX_PROSPECTS_PER_DAY = 30
MAX_EMAILS_PER_DAY = 20
MAX_INSTAGRAM_DMS = 15
MAX_LINKEDIN_MSGS = 10

# Heure du rapport quotidien
REPORT_HOUR = 7  # 7h00 du matin

# Délai entre actions (secondes)
DELAY_BETWEEN_REQUESTS = 3
DELAY_BETWEEN_EMAILS = 10
