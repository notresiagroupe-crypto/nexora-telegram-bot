import os, asyncio, logging, smtplib, requests, re
from datetime import datetime
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, CallbackQueryHandler,
                          MessageHandler, filters, ContextTypes, ConversationHandler)

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_TOKEN", "")
GMAIL = os.getenv("GMAIL_EMAIL", "zambolionel043@gmail.com")
GMAIL_PWD = os.getenv("GMAIL_APP_PASSWORD", "").replace(" ", "")

ANALYSE = 1  # état conversation

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

def menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 Lancer la prospection", callback_data="run")],
        [InlineKeyboardButton("🔎 Analyser un prospect", callback_data="analyse")],
        [InlineKeyboardButton("📊 Stats CRM", callback_data="stats"),
         InlineKeyboardButton("📧 Tester email", callback_data="email")],
        [InlineKeyboardButton("📋 Rapport maintenant", callback_data="report"),
         InlineKeyboardButton("ℹ️ Statut", callback_data="status")],
    ])

# ─── Analyse de site ──────────────────────
def analyse_site(url):
    """Analyse un site web et retourne ses points faibles"""
    if not url.startswith("http"):
        url = "https://" + url
    
    problems = []
    strengths = []
    score = 100
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = resp.text.lower()
        
        # SEO
        title = soup.find("title")
        if not title or len(title.text) < 10:
            problems.append("❌ Pas de titre SEO optimisé")
            score -= 15
        else:
            strengths.append("✅ Titre présent")
            
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if not meta_desc:
            problems.append("❌ Pas de meta description (invisible sur Google)")
            score -= 15
            
        # Mobile
        viewport = soup.find("meta", attrs={"name": "viewport"})
        if not viewport:
            problems.append("❌ Site non adapté mobile (perd 60% des visiteurs)")
            score -= 20
        else:
            strengths.append("✅ Compatible mobile")
            
        # Contact
        contact_patterns = ["contact", "formulaire", "form", "mailto:", "tel:"]
        has_contact = any(p in text for p in contact_patterns)
        if not has_contact:
            problems.append("❌ Pas de formulaire de contact visible")
            score -= 15
        else:
            strengths.append("✅ Contact présent")
            
        # Google Analytics / tracking
        if "google-analytics" not in text and "gtag" not in text and "ga.js" not in text:
            problems.append("❌ Pas de suivi analytique (Google Analytics manquant)")
            score -= 10
            
        # HTTPS
        if not url.startswith("https"):
            problems.append("❌ Site non sécurisé (HTTP au lieu de HTTPS)")
            score -= 15
        else:
            strengths.append("✅ HTTPS sécurisé")
            
        # Réservation/booking
        booking_patterns = ["réserver", "reservation", "booking", "rendez-vous", "rdv", "calendly"]
        if not any(p in text for p in booking_patterns):
            problems.append("❌ Pas de système de réservation en ligne")
            score -= 10
            
        # Réseaux sociaux
        social_patterns = ["instagram", "facebook", "linkedin", "tiktok"]
        has_social = any(p in text for p in social_patterns)
        if not has_social:
            problems.append("❌ Pas de liens réseaux sociaux")
            score -= 5
            
        # Vitesse (heuristique)
        if len(resp.content) > 3_000_000:
            problems.append("❌ Site trop lourd (temps de chargement lent)")
            score -= 10
            
        site_name = title.text.strip()[:40] if title else url
        
    except Exception as e:
        return None, str(e), url
    
    return {
        "url": url,
        "name": site_name,
        "score": max(0, score),
        "problems": problems[:5],
        "strengths": strengths[:3]
    }, None, url


def generate_pitch(analysis):
    """Génère un message de prospection basé sur l'analyse"""
    name = analysis["name"]
    problems = analysis["problems"]
    score = analysis["score"]
    
    if not problems:
        return f"Ce site est déjà bien optimisé (score: {score}/100). Proposer des services avancés (IA, automatisation)."
    
    main_problem = problems[0].replace("❌ ", "")
    
    pitch = f"""Bonjour,

J'ai analysé le site {name} et j'ai identifié {len(problems)} point(s) à améliorer qui vous font perdre des clients.

Le plus urgent : {main_problem}.

En tant qu'agence web & IA à Bordeaux, je peux régler ça rapidement :
"""
    
    for p in problems[:3]:
        fix = p.replace("❌ ", "").replace("Pas de ", "Mise en place d'un ").replace("Site non ", "Correction : site ")
        pitch += f"→ {fix}\n"
    
    pitch += f"""
Résultat attendu : +30% de contacts en moins d'un mois.

Je vous propose 30 min d'échange gratuit cette semaine ?

Lionel — NEXORA Studio
{analysis['url']}"""
    
    return pitch


# ─── Handlers ─────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 *NEXORA Prospection Bot*\n\n"
        "Système de prospection automatique.\n"
        "Rapport quotidien à 7h00 → zambolionel043@gmail.com",
        parse_mode="Markdown", reply_markup=menu_kb())

async def analyse_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    await q.edit_message_text(
        "🔎 *Analyseur de Prospect*\n\n"
        "Envoie-moi l'URL ou le nom du site à analyser.\n\n"
        "Exemples :\n"
        "• `https://restaurant-bordeaux.fr`\n"
        "• `www.salon-beaute-bordeaux.com`",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Annuler", callback_data="menu")]]))
    return ANALYSE

async def analyse_url(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("⏳ Analyse en cours...")
    
    loop = asyncio.get_event_loop()
    result, error, clean_url = await loop.run_in_executor(None, lambda: analyse_site(url))
    
    if error or not result:
        await update.message.reply_text(
            f"❌ Impossible d'analyser ce site.\n`{error}`\n\nVérifie l'URL et réessaie.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Menu", callback_data="menu")]]))
        return ConversationHandler.END
    
    # Résumé de l'analyse
    score = result["score"]
    emoji = "🟢" if score >= 70 else ("🟡" if score >= 40 else "🔴")
    
    analysis_text = (
        f"🔎 *Analyse : {result['name']}*\n"
        f"{emoji} Score : {score}/100\n\n"
    )
    
    if result["strengths"]:
        analysis_text += "*Points forts :*\n"
        analysis_text += "\n".join(result["strengths"]) + "\n\n"
    
    if result["problems"]:
        analysis_text += "*Problèmes détectés :*\n"
        analysis_text += "\n".join(result["problems"]) + "\n\n"
    
    pitch = generate_pitch(result)
    analysis_text += f"*📝 Message de prospection généré :*\n\n`{pitch}`"
    
    await update.message.reply_text(
        analysis_text[:4000],
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔎 Analyser un autre", callback_data="analyse")],
            [InlineKeyboardButton("◀️ Menu", callback_data="menu")]
        ]))
    return ConversationHandler.END

async def analyse_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    await q.edit_message_text("🚀 *NEXORA Prospection Bot*\n\nQue veux-tu faire ?",
        parse_mode="Markdown", reply_markup=menu_kb())
    return ConversationHandler.END

# ─── Autres callbacks ──────────────────────
async def status_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    await q.edit_message_text(
        f"ℹ️ *Statut système*\n\n🕐 {now}\n✅ Bot actif\n"
        f"{'✅' if GMAIL_PWD else '❌'} Gmail configuré\n"
        f"✅ Secteurs : Restaurant · Beauté · Boutique\n✅ Zone : Bordeaux",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Menu", callback_data="menu")]]))

async def run_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    await q.edit_message_text("⏳ *Prospection en cours...*\nCela peut prendre quelques minutes.", parse_mode="Markdown")
    try:
        from scrapers.google_scraper import find_all_prospects
        from scrapers.instagram_scraper import find_instagram_prospects, find_linkedin_prospects, find_malt_prospects
        from messaging.email_sender import send_prospection_emails
        from storage.base44_storage import save_all_prospects, get_prospects_stats
        from reports.daily_report import send_daily_report
        loop = asyncio.get_event_loop()
        google_p = await loop.run_in_executor(None, lambda: find_all_prospects(limit_per_sector=5))
        _, sent, _ = await loop.run_in_executor(None, lambda: send_prospection_emails(google_p, max_emails=10))
        insta_p = await loop.run_in_executor(None, find_instagram_prospects)
        linkedin_p = await loop.run_in_executor(None, find_linkedin_prospects)
        malt_p = await loop.run_in_executor(None, find_malt_prospects)
        await loop.run_in_executor(None, lambda: save_all_prospects(google_p + insta_p + linkedin_p + malt_p))
        stats = await loop.run_in_executor(None, get_prospects_stats)
        await loop.run_in_executor(None, lambda: send_daily_report(stats, google_p, insta_p, linkedin_p, malt_p))
        text = (f"✅ *Prospection terminée !*\n\n📧 Emails : {sent}\n"
                f"📸 Instagram : {len(insta_p)}\n💼 LinkedIn : {len(linkedin_p)}\n"
                f"🧑‍💻 Malt : {len(malt_p)}\n📬 Rapport envoyé sur Gmail")
    except Exception as e:
        text = f"❌ Erreur : {str(e)[:200]}"
    await ctx.bot.send_message(q.message.chat_id, text, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Menu", callback_data="menu")]]))

async def stats_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    try:
        from storage.base44_storage import get_prospects_stats
        s = get_prospects_stats()
        text = (f"📊 *Stats CRM*\n\n👥 Total : {s.get('total',0)}\n"
                f"📧 Emails : {s.get('emailed',0)}\n💬 Réponses : {s.get('replied',0)}\n"
                f"✍️ Signés : {s.get('signed',0)}\n📈 Taux : {s.get('conversion_rate','0%')}")
    except Exception as e:
        text = f"❌ {str(e)[:100]}"
    await q.edit_message_text(text, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Menu", callback_data="menu")]]))

async def email_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    try:
        msg = MIMEText("✅ Test NEXORA Bot - Système opérationnel !")
        msg["Subject"] = "✅ NEXORA Bot - Test OK"
        msg["From"] = GMAIL; msg["To"] = GMAIL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(GMAIL, GMAIL_PWD); s.sendmail(GMAIL, GMAIL, msg.as_string())
        text = "✅ *Email envoyé !*\nVérifie zambolionel043@gmail.com"
    except Exception as e:
        text = f"❌ Erreur email : {str(e)[:200]}"
    await q.edit_message_text(text, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Menu", callback_data="menu")]]))

async def report_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    try:
        from storage.base44_storage import get_prospects_stats
        from reports.daily_report import send_daily_report
        send_daily_report(get_prospects_stats(), [], [], [], [])
        text = "✅ *Rapport envoyé !*\nVérifie zambolionel043@gmail.com"
    except Exception as e:
        text = f"❌ {str(e)[:200]}"
    await q.edit_message_text(text, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Menu", callback_data="menu")]]))

async def menu_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    await q.edit_message_text("🚀 *NEXORA Prospection Bot*\n\nQue veux-tu faire ?",
        parse_mode="Markdown", reply_markup=menu_kb())

def main():
    print(f"🤖 NEXORA Bot démarré — {datetime.now().strftime('%d/%m %H:%M')}")
    app = Application.builder().token(TOKEN).build()

    # Conversation analyser
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(analyse_start, pattern="^analyse$")],
        states={ANALYSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, analyse_url)]},
        fallbacks=[CallbackQueryHandler(analyse_cancel, pattern="^menu$")],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(status_cb, pattern="^status$"))
    app.add_handler(CallbackQueryHandler(run_cb, pattern="^run$"))
    app.add_handler(CallbackQueryHandler(stats_cb, pattern="^stats$"))
    app.add_handler(CallbackQueryHandler(email_cb, pattern="^email$"))
    app.add_handler(CallbackQueryHandler(report_cb, pattern="^report$"))
    app.add_handler(CallbackQueryHandler(menu_cb, pattern="^menu$"))
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
