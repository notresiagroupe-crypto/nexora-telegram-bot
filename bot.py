import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "8622529595:AAHhDpdwsFgTXwnerXPe1qqCEdz6h2obsxE")
LIONEL_CHAT_ID = os.getenv("LIONEL_CHAT_ID", "")  # Ton ID Telegram perso

# États conversation
SERVICE, BUDGET, DESCRIPTION, CONTACT = range(4)

# ─────────────────────────────────────────
# /start
# ─────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    keyboard = [
        [InlineKeyboardButton("🌐 Site Web", callback_data="svc_site"),
         InlineKeyboardButton("🤖 Automatisation IA", callback_data="svc_ia")],
        [InlineKeyboardButton("📱 Stratégie Digitale", callback_data="svc_digital"),
         InlineKeyboardButton("🔍 Prospection Auto", callback_data="svc_prosp")],
        [InlineKeyboardButton("💼 Voir le Portfolio", callback_data="portfolio")],
        [InlineKeyboardButton("💬 Parler à Lionel", callback_data="contact")],
    ]
    await update.message.reply_text(
        f"👋 Bonjour {name} !\n\n"
        f"Bienvenue chez *NEXORA Studio* — Agence Web & IA à Bordeaux.\n\n"
        f"Je suis le bot assistant de Lionel 🚀\n"
        f"Que puis-je faire pour vous ?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ─────────────────────────────────────────
# Portfolio
# ─────────────────────────────────────────
async def portfolio(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    keyboard = [
        [InlineKeyboardButton("🍽️ Restaurant Gastronomique", url="https://notresiagroupe-crypto.github.io/nexora/demos/restaurant.html")],
        [InlineKeyboardButton("✨ Institut Beauté", url="https://notresiagroupe-crypto.github.io/nexora/demos/beaute.html")],
        [InlineKeyboardButton("💪 Coach Sportif", url="https://notresiagroupe-crypto.github.io/nexora/demos/coach.html")],
        [InlineKeyboardButton("🔧 Artisan Plombier", url="https://notresiagroupe-crypto.github.io/nexora/demos/artisan.html")],
        [InlineKeyboardButton("📚 RévisionIA (App Web)", url="https://notresiagroupe-crypto.github.io/revi/")],
        [InlineKeyboardButton("🌐 Site NEXORA Complet", url="https://notresiagroupe-crypto.github.io/nexora/")],
        [InlineKeyboardButton("◀️ Retour", callback_data="back")],
    ]
    await q.edit_message_text(
        "💼 *Portfolio NEXORA Studio*\n\n"
        "Cliquez pour tester chaque site en live 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ─────────────────────────────────────────
# Services
# ─────────────────────────────────────────
SERVICES_INFO = {
    "svc_site": {
        "title": "🌐 Site Web & Landing Page",
        "desc": (
            "• Design moderne sur mesure\n"
            "• Mobile-first + SEO optimisé\n"
            "• Formulaire de contact intégré\n"
            "• Hébergement inclus 1 an\n"
            "• Livraison en 7-10 jours\n\n"
            "*À partir de 500€*"
        )
    },
    "svc_ia": {
        "title": "🤖 Automatisation IA",
        "desc": (
            "• Chatbot intelligent pour votre site\n"
            "• Automatisation emails/réponses\n"
            "• Workflows n8n / Make / Zapier\n"
            "• Agents IA sur mesure\n"
            "• Support et formation inclus\n\n"
            "*À partir de 800€*"
        )
    },
    "svc_digital": {
        "title": "📱 Stratégie Digitale",
        "desc": (
            "• Gestion Instagram & LinkedIn\n"
            "• Création de contenu avec IA\n"
            "• Publicité Meta/Google\n"
            "• Rapport mensuel de performance\n\n"
            "*À partir de 300€/mois*"
        )
    },
    "svc_prosp": {
        "title": "🔍 Prospection Automatique",
        "desc": (
            "• Recherche de leads automatique\n"
            "• Messages personnalisés par secteur\n"
            "• Multi-canaux : Google, Instagram,\n"
            "  LinkedIn, Malt\n"
            "• Rapport quotidien à 7h00\n"
            "• CRM intégré\n\n"
            "*À partir de 600€*"
        )
    }
}

async def service_detail(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    info = SERVICES_INFO.get(q.data, {})
    keyboard = [
        [InlineKeyboardButton("🚀 Demander un devis", callback_data=f"devis_{q.data}")],
        [InlineKeyboardButton("◀️ Retour", callback_data="back")],
    ]
    await q.edit_message_text(
        f"*{info['title']}*\n\n{info['desc']}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ─────────────────────────────────────────
# Devis (conversation)
# ─────────────────────────────────────────
async def start_devis(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    ctx.user_data["service"] = q.data.replace("devis_svc_", "")
    keyboard = [
        [InlineKeyboardButton("< 500€", callback_data="b_500"),
         InlineKeyboardButton("500€ - 1000€", callback_data="b_1000")],
        [InlineKeyboardButton("1000€ - 2000€", callback_data="b_2000"),
         InlineKeyboardButton("> 2000€", callback_data="b_plus")],
    ]
    await q.edit_message_text(
        "💰 *Quel est votre budget approximatif ?*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return BUDGET

async def budget_chosen(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    ctx.user_data["budget"] = q.data.replace("b_", "")
    await q.edit_message_text(
        "📝 *Décrivez votre projet en quelques lignes :*\n\n"
        "_Secteur d'activité, objectifs, délai souhaité..._",
        parse_mode="Markdown"
    )
    return DESCRIPTION

async def description_received(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["description"] = update.message.text
    await update.message.reply_text(
        "📞 *Votre email ou numéro de téléphone ?*\n\n"
        "_Lionel vous répondra dans les 24h_",
        parse_mode="Markdown"
    )
    return CONTACT

async def contact_received(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ctx.user_data["contact"] = update.message.text

    # Résumé pour l'utilisateur
    await update.message.reply_text(
        "✅ *Demande de devis envoyée !*\n\n"
        f"📋 Service : {ctx.user_data.get('service', '?')}\n"
        f"💰 Budget : {ctx.user_data.get('budget', '?')}€\n"
        f"📝 Projet : {ctx.user_data.get('description', '?')[:100]}\n\n"
        "Lionel vous contacte sous 24h. Merci ! 🙏\n\n"
        "🌐 nexorastudio.netlify.app",
        parse_mode="Markdown"
    )

    # Notification à Lionel
    if LIONEL_CHAT_ID:
        notif = (
            f"🚨 *NOUVEAU DEVIS*\n\n"
            f"👤 {user.full_name} (@{user.username or 'sans username'})\n"
            f"📋 Service : {ctx.user_data.get('service')}\n"
            f"💰 Budget : {ctx.user_data.get('budget')}€\n"
            f"📝 {ctx.user_data.get('description')}\n"
            f"📞 Contact : {ctx.user_data.get('contact')}"
        )
        await ctx.bot.send_message(chat_id=LIONEL_CHAT_ID, text=notif, parse_mode="Markdown")

    return ConversationHandler.END

# ─────────────────────────────────────────
# Contact direct
# ─────────────────────────────────────────
async def contact(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    keyboard = [
        [InlineKeyboardButton("✉️ Email", url="mailto:zambolionel043@gmail.com")],
        [InlineKeyboardButton("📸 Instagram", url="https://instagram.com/id_lionel")],
        [InlineKeyboardButton("💼 Malt", url="https://malt.fr/profile/lionelmanga")],
        [InlineKeyboardButton("◀️ Retour", callback_data="back")],
    ]
    await q.edit_message_text(
        "💬 *Contacter Lionel — NEXORA Studio*\n\n"
        "📍 Bordeaux, France\n"
        "⏱ Réponse sous 24h\n"
        "🎓 Consultation gratuite de 30 min",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ─────────────────────────────────────────
# Retour menu principal
# ─────────────────────────────────────────
async def back(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    keyboard = [
        [InlineKeyboardButton("🌐 Site Web", callback_data="svc_site"),
         InlineKeyboardButton("🤖 Automatisation IA", callback_data="svc_ia")],
        [InlineKeyboardButton("📱 Stratégie Digitale", callback_data="svc_digital"),
         InlineKeyboardButton("🔍 Prospection Auto", callback_data="svc_prosp")],
        [InlineKeyboardButton("💼 Voir le Portfolio", callback_data="portfolio")],
        [InlineKeyboardButton("💬 Parler à Lionel", callback_data="contact")],
    ]
    await q.edit_message_text(
        "🚀 *NEXORA Studio* — Que puis-je faire pour vous ?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Annulé. Tapez /start pour recommencer.")
    return ConversationHandler.END

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
def main():
    app = Application.builder().token(TOKEN).build()

    # Conversation devis
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_devis, pattern="^devis_")],
        states={
            BUDGET: [CallbackQueryHandler(budget_chosen, pattern="^b_")],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, description_received)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, contact_received)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(portfolio, pattern="^portfolio$"))
    app.add_handler(CallbackQueryHandler(contact, pattern="^contact$"))
    app.add_handler(CallbackQueryHandler(back, pattern="^back$"))
    app.add_handler(CallbackQueryHandler(service_detail, pattern="^svc_"))
    app.add_handler(conv)

    print("🤖 NEXORA Bot démarré...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
