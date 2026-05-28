# messaging/templates.py
# ══════════════════════════════════════════
# Templates de messages personnalisés
# par secteur d'activité
# ══════════════════════════════════════════

from config.settings import NEXORA_NAME, NEXORA_AGENCY, NEXORA_WEBSITE, NEXORA_INSTAGRAM

def get_email_template(sector, business_name, city="Bordeaux"):
    templates = {
        "restaurant": {
            "subject": f"Votre restaurant {business_name} mérite plus de clients 🍽️",
            "body": f"""Bonjour,

Je suis {NEXORA_NAME}, fondateur de {NEXORA_AGENCY}, agence web et IA à {city}.

En faisant une recherche sur les restaurants de {city}, j'ai remarqué que {business_name} n'apparaît pas en première page Google — ce qui représente des dizaines de couverts perdus chaque semaine.

Ce qu'on peut faire pour vous en moins de 2 semaines :
✅ Site web moderne avec menu digital et photos
✅ Système de réservation en ligne (fini les appels manqués)
✅ Fiche Google Maps optimisée → +40% de clics en moyenne
✅ Menu QR Code pour vos tables

Le tout à partir de 500€, sans abonnement caché.

Je vous propose 30 min d'échange gratuit cette semaine pour voir si on peut vous aider.

Bonne journée,
{NEXORA_NAME} — {NEXORA_AGENCY}
{NEXORA_WEBSITE}
{NEXORA_INSTAGRAM}"""
        },
        "beaute": {
            "subject": f"{business_name} — Doublez vos réservations avec un site moderne 💅",
            "body": f"""Bonjour,

Je suis {NEXORA_NAME} de {NEXORA_AGENCY}, agence digitale à {city}.

J'ai vu que {business_name} est actif sur Instagram — super contenu ! Mais sans site web ou système de RDV en ligne, vous perdez probablement 30 à 40% de vos clients potentiels qui cherchent sur Google.

Ce qu'on peut mettre en place rapidement :
✅ Site vitrine élégant avec vos prestations et tarifs
✅ Réservation en ligne 24h/24 (Calendly ou Système custom)
✅ Automatisation de vos posts Instagram avec l'IA
✅ Rappel SMS automatique → -80% de no-shows

À partir de 500€ · Livraison en 10 jours · Satisfaction garantie.

Un appel rapide cette semaine pour en discuter ?

{NEXORA_NAME} — {NEXORA_AGENCY}
{NEXORA_WEBSITE}"""
        },
        "boutique": {
            "subject": f"Vendez en ligne 24h/24 — Projet pour {business_name} 🛍️",
            "body": f"""Bonjour,

{NEXORA_NAME}, fondateur de {NEXORA_AGENCY} à {city}.

Votre boutique {business_name} a un beau potentiel digital que vous n'exploitez peut-être pas encore. Avec un site e-commerce bien fait, vos clients peuvent commander depuis chez eux — même la nuit.

Ce qu'on construit pour vous :
✅ Boutique en ligne avec votre catalogue complet
✅ Paiement sécurisé (CB, PayPal, Apple Pay)
✅ Gestion des stocks simplifiée
✅ Automatisation des descriptions produits avec l'IA

Résultat moyen de nos clients : +25% de CA le premier trimestre.

Intéressé(e) pour un devis gratuit ?

{NEXORA_NAME} — {NEXORA_AGENCY}
{NEXORA_WEBSITE}
{NEXORA_INSTAGRAM}"""
        }
    }
    return templates.get(sector, templates["restaurant"])


def get_instagram_dm(sector, business_name):
    templates = {
        "restaurant": f"""Bonjour ! 👋 

Belle page pour {business_name} ! Votre contenu food donne vraiment envie 🍽️

Je suis Lionel de NEXORA Studio — on aide les restaurants à avoir plus de clients grâce au web et à l'IA.

Est-ce que vous avez un site avec réservation en ligne ? Si non, je peux vous montrer ce qu'on a fait pour d'autres restos à Bordeaux 🙌

Dispo pour en parler cette semaine ?""",

        "beaute": f"""Bonjour ! ✨

Vos réalisations sur {business_name} sont vraiment top, j'adore votre feed !

Je suis Lionel de NEXORA Studio — j'aide les instituts beauté à automatiser leurs RDV et à gagner des clients sur Google.

Vous avez un site web avec prise de RDV en ligne ? Je peux vous envoyer quelques idées gratuitement si vous voulez 💅

Bonne journée !""",

        "boutique": f"""Bonjour ! 🛍️

J'ai découvert {business_name} sur Instagram — super concept et beau style !

Je suis Lionel, je crée des sites e-commerce pour les boutiques bordelaises qui veulent vendre en ligne.

Est-ce que vous avez déjà une boutique en ligne ? Je serais ravi de vous partager ce qu'on a fait pour d'autres boutiques à Bordeaux 🚀"""
    }
    return templates.get(sector, templates["restaurant"])


def get_linkedin_message(sector, first_name, business_name):
    return f"""Bonjour {first_name},

J'ai découvert {business_name} et j'ai été impressionné par votre activité dans le secteur {sector} à Bordeaux.

Je suis Lionel Manga, fondateur de NEXORA Studio — on aide les PME bordelaises à développer leur présence digitale avec des sites web premium et l'automatisation IA.

Je serais ravi d'échanger 15 min pour voir si on peut vous apporter de la valeur.

Bonne journée,
Lionel"""


def get_malt_message(first_name, project_description=""):
    return f"""Bonjour {first_name} !

Je suis Lionel, développeur web et expert IA basé à Bordeaux (profil NEXORA Studio).

{("J'ai vu votre annonce concernant : " + project_description + ".") if project_description else "Je suis disponible pour de nouveaux projets web et automatisation IA."}

Mon stack : React, Next.js, Python, API IA (Claude, OpenAI), automatisation n8n/Make.

Disponible rapidement et livraison garantie dans les délais. Je vous envoie mon portfolio ?

Lionel"""
