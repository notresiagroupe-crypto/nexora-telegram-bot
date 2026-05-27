# 🚀 NEXORA Studio — Système de Prospection Automatique

## Ce que ça fait
- 🔍 **Google** → Trouve restaurants, instituts beauté, boutiques à Bordeaux
- 📧 **Email auto** → Envoie des messages personnalisés aux prospects
- 📸 **Instagram** → Liste les comptes à contacter + DMs prêts
- 💼 **LinkedIn** → Trouve les gérants + messages de connexion prêts
- 🧑‍💻 **Malt** → Trouve les missions disponibles
- 💾 **Base44 CRM** → Sauvegarde tout automatiquement
- 📊 **Rapport 7h00** → Email récap chaque matin

---

## Setup en 5 minutes sur Replit

### 1. Importe le projet
```
Replit → + New Repl → Import from GitHub
→ notresiagroupe-crypto/nexora (ou upload les fichiers)
```

### 2. Configure le .env
Dans Replit → **Secrets** (icône cadenas) → Ajoute :
```
GMAIL_EMAIL = zambolionel043@gmail.com
GMAIL_APP_PASSWORD = [ton mot de passe app Gmail]
```

**Créer le mot de passe Gmail :**
1. myaccount.google.com
2. Sécurité → Validation en 2 étapes (activer si pas fait)
3. Mots de passe des applications → Créer pour "Mail"
4. Copie les 16 caractères → colle dans Replit Secrets

### 3. Configure le keep-alive
Dans Replit → `.replit` → ajoute :
```toml
[deployment]
run = ["python", "main.py", "--daemon"]
```

Puis sur **UptimeRobot.com** → ajoute ton URL Replit en monitoring toutes les 5 min.

### 4. Lance !
```bash
# Test rapide (un cycle)
python main.py

# Mode 24/7 (rapport à 7h00 chaque jour)
python main.py --daemon

# Juste le rapport
python main.py --report
```

---

## Résultats attendus
| Canal | Prospects/jour | Taux de réponse |
|-------|---------------|-----------------|
| Email Google | 15-20 | 5-8% |
| Instagram DM | 10-15 (manuel) | 10-15% |
| LinkedIn | 5-8 (manuel) | 8-12% |
| Malt | 3-5 | 20-30% |

---

## ⚠️ Limites légales
- Les emails sont envoyés aux adresses publiques des sites web
- Chaque email inclut une option "STOP" (conformité RGPD)
- Instagram et LinkedIn : les messages sont générés mais envoyés manuellement depuis Base44
- Limite : 20 emails/jour max pour éviter le spam

## Accès CRM
**Base44 Dashboard** : https://app.base44.com/apps/69cfbd6c4ad311d1ec530908
(Double-clic sur le logo en bas de nexorastudio.netlify.app)
