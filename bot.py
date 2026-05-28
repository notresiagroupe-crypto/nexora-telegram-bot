import os, asyncio, logging, smtplib
from datetime import datetime
from email.mime.text import MIMEText
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_TOKEN", "")
GMAIL = os.getenv("GMAIL_EMAIL", "zambolionel043@gmail.com")
GMAIL_PWD = os.getenv("GMAIL_APP_PASSWORD", "").replace(" ", "")  # strip spaces

def menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 Lancer la prospection", callback_data="run")],
        [InlineKeyboardButton("📊 Stats CRM", callback_data="stats")],
        [InlineKeyboardButton("📧 Tester email", callback_data="email")],
        [InlineKeyboardButton("📋 Rapport maintenant", callback_data="report")],
        [InlineKeyboardButton("ℹ️ Statut système", callback_data="status")],
    ])

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 *NEXORA Prospection Bot*\n\n"
        "Système de prospection automatique.\n"
        "Rapport quotidien à 7h00 → zambolionel043@gmail.com\n\n"
        "Que veux-tu faire ?",
        parse_mode="Markdown",
        reply_markup=menu_kb()
    )

async def status_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    await q.edit_message_text(
        f"ℹ️ *Statut système*\n\n🕐 {now}\n"
        f"✅ Bot actif\n{'✅' if GMAIL_PWD else '❌'} Gmail configuré\n"
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

        text = (f"✅ *Prospection terminée !*\n\n"
                f"📧 Emails envoyés : {sent}\n"
                f"📸 Instagram : {len(insta_p)}\n"
                f"💼 LinkedIn : {len(linkedin_p)}\n"
                f"🧑‍💻 Malt : {len(malt_p)}\n"
                f"📬 Rapport envoyé sur Gmail")
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
                f"📧 Emails : {s.get('emailed',0)}\n"
                f"💬 Réponses : {s.get('replied',0)}\n"
                f"✍️ Signés : {s.get('signed',0)}\n"
                f"📈 Taux : {s.get('conversion_rate','0%')}")
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
            s.login(GMAIL, GMAIL_PWD)
            s.sendmail(GMAIL, GMAIL, msg.as_string())
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
    await q.edit_message_text(
        "🚀 *NEXORA Prospection Bot*\n\nQue veux-tu faire ?",
        parse_mode="Markdown", reply_markup=menu_kb())

def main():
    print(f"🤖 NEXORA Bot démarré — {datetime.now().strftime('%d/%m %H:%M')}")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(status_cb, pattern="^status$"))
    app.add_handler(CallbackQueryHandler(run_cb, pattern="^run$"))
    app.add_handler(CallbackQueryHandler(stats_cb, pattern="^stats$"))
    app.add_handler(CallbackQueryHandler(email_cb, pattern="^email$"))
    app.add_handler(CallbackQueryHandler(report_cb, pattern="^report$"))
    app.add_handler(CallbackQueryHandler(menu_cb, pattern="^menu$"))
    # drop_pending_updates = ignore old messages from previous sessions
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
