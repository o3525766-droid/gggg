import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest

# Bot token
TOKEN = "8619512674:AAFe2ziiohaUoNfuubxXMLpp_kpCWVSQUvA"

# Uzbek alphabet and common words for detection
UZBEK_CHARS = set("ʻ'ʼg'o'g'G'O'Q'quvсчяуеолзжхцваинфртпмшщджэюбьъйё")
UZBEK_WORDS = [
    "salom", "qalay", "nimadir", "bor", "yo'q", "ha", "mayli", "rahmat", 
    "men", "sen", "u", "biz", "siz", "ular", "nima", "qachon", "qayer",
    "qanday", "kim", "nega", "qanday", "qaysi", "qancha", "qachon", "hozir",
    "kecha", "ertaga", "bugun", "shanba", "yakshanba", "dushanba", "seshanba",
    "chorshanba", "payshanba", "juma", "yil", "oy", "hafta", "kun", "soat",
    "daqiqa", "soniya", "ikki", "uch", "to'rt", "besh", "olti", "yetti", "sakkiz",
    "to'qqiz", "o'n", "yigirma", "ottiz", "qirq", "ellik", "oltmish", "yetmish",
    "sakson", "to'qson", "yuz", "ming", "million", "milliard", "kitob", "qalam",
    "maktab", "universitet", "o'qituvchi", "talaba", "doktor", "muhandis",
    "dasturchi", "ishchi", "boshliq", "ra'is", "prezident", "vazir", "deputat",
    "senator", "deputat", "mayor", "gubernator", "politsiya", "harbiy", "askar",
    "ofitser", "general", "admiral", "kapitan", "leytenant", "serjant", "jangchi",
    "tarix", "geografiya", "matematika", "fizika", "kimyo", "biologiya", "tilshunoslik",
    "adabiyot", "san'at", "musiqa", "rasm", "haykaltaroshlik", "arxitektura", "teatr",
    "kino", "televidenie", "radio", "internet", "kompyuter", "telefon", "planshet",
    "noutbuk", "mashina", "avtomobil", "avtobus", "tramvay", "trolleybus", "metro",
    "poyezd", "samolyot", "kemalar", "velosiped", "motosikl", "skuter", "sayr",
    "dam olish", "sport", "futbol", "basketbol", "voleybol", "tennis", "golf",
    "shaxmat", "kriket", "regbi", "xokkey", "gimnastika", "yugurish", "suzish",
    "sakrash", "otish", "arqon tortish", "qisqa", "uzun", "keng", "tor", "baland",
    "past", "kichik", "katta", "og'ir", "engil", "qizil", "ko'k", "yashil", "sariq",
    "oq", "qora", "jigarrang", "kulrang", "pushti", "binafsha", "to'q sariq", "och",
    "qorong'i", "yorug'", "quyosh", "oy", "yulduz", "bulut", "yomg'ir", "qor",
    "muz", "shamol", "tornado", "dengiz", "okean", "daryo", "ko'l", "havza",
    "fontan", "quduq", "buloq", "chashma", "tog'", "tepalik", "vadi", "cho'l",
    "sahro", "o'rmon", "dasht", "step", "tundra", "torf", "botqoq", "zamin",
    "tuproq", "qum", "tosh", "jins", "kon", "foydali qazilma", "neft", "gaz",
    "ko'mir", "oltin", "kumush", "mis", "temir", "qalay", "rux", "qo'rg'oshin",
    "alyuminiy", "magniy", "kaliy", "kalsiy", "natriy", "forsfor", "oltingugurt",
    "xlor", "yod", "brom", "ftor", "vodorod", "kislorod", "azot", "uglerod"
]

# Dictionary to track warnings: {user_id: {group_id: warning_count}}
warnings = {}

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def is_uzbek(text):
    """Check if text contains Uzbek language characters or words"""
    if not text:
        return False
    
    text_lower = text.lower()
    
    # Check for Uzbek specific characters
    for char in text_lower:
        if char in UZBEK_CHARS:
            return True
    
    # Check for Uzbek words
    words = text_lower.split()
    for word in words:
        if word in UZBEK_WORDS:
            return True
    
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "Assalomu alaykum! Men grupalarda o'zbek tilidagi xabarlarni o'chiraman. "
        "3 marta o'zbek tilida yozsangiz, gruhdan chqarib yuboraman."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "Bu bot grupalarda o'zbek tilidagi xabarlarni moderatsiya qiladi.\n"
        "Agar kimdir o'zbek tilida yozsa, xabari o'chiriladi va ogohlantiriladi.\n"
        "3 ta ogohlantirishdan so'ng, foydalanuvchi gruhdan chqariladi."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    message = update.message
    
    # Only process messages in groups
    if not message.chat or message.chat.type not in ['group', 'supergroup']:
        return
    
    # Check if the message is in Uzbek
    if message.text and is_uzbek(message.text):
        user_id = message.from_user.id
        group_id = message.chat.id
        user_name = message.from_user.first_name
        
        # Initialize warning tracking for this user
        if user_id not in warnings:
            warnings[user_id] = {}
        if group_id not in warnings[user_id]:
            warnings[user_id][group_id] = 0
        
        # Increment warning count
        warnings[user_id][group_id] += 1
        warning_count = warnings[user_id][group_id]
        
        try:
            # Delete the message
            await message.delete()
            
            if warning_count < 3:
                # Send warning
                warning_msg = (
                    f"⚠️ {user_name}, o'zbek tilida yozish taqiqlanadi!\n"
                    f"Ogohlantirish: {warning_count}/3\n"
                    f"3 marta ogohlantirilsangiz, gruhdan chqarilasiz."
                )
                await context.bot.send_message(chat_id=group_id, text=warning_msg)
            else:
                # Kick the user
                try:
                    await context.bot.ban_chat_member(chat_id=group_id, user_id=user_id)
                    kick_msg = (
                        f"🚫 {user_name} 3 marta o'zbek tilida yozgani uchun "
                        f"gruhdan chqarildi!"
                    )
                    await context.bot.send_message(chat_id=group_id, text=kick_msg)
                    
                    # Reset warnings for this user in this group
                    warnings[user_id][group_id] = 0
                except BadRequest as e:
                    logger.error(f"Could not kick user: {e}")
                    await context.bot.send_message(
                        chat_id=group_id,
                        text=f"❌ Foydalanuvchini chqarib bo'lmadi: {str(e)}"
                    )
        except BadRequest as e:
            logger.error(f"Could not delete message: {e}")

async def reset_warnings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reset warnings for a user (admin only)"""
    if not update.message.reply_to_message:
        await update.message.reply_text("Iltimos, ogohlantirishni qayta tiklash uchun foydalanuvchi xabariga javob bering.")
        return
    
    user_id = update.message.reply_to_message.from_user.id
    group_id = update.message.chat.id
    
    if user_id in warnings and group_id in warnings[user_id]:
        warnings[user_id][group_id] = 0
        await update.message.reply_text(f"✅ Foydalanuvchining ogohlantirishlari qayta tiklandi.")
    else:
        await update.message.reply_text("Bu foydalanuvchi uchun ogohlantirish yo'q.")

def main():
    """Start the bot"""
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reset", reset_warnings))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    application.run_polling()
    logger.info("Bot ishga tushdi...")

if __name__ == '__main__':
    main()
