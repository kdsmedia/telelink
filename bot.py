from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Konfigurasi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token bot yang diberikan oleh BotFather
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# ID grup atau channel yang pengguna harus bergabung
GROUP_IDS = list(map(int, os.getenv('GROUP_IDS', 'group_id_1,group_id_2,group_id_3,group_id_4,group_id_5').split(',')))
# Link yang akan diberikan kepada pengguna setelah mereka bergabung dengan semua grup atau channel
SECRET_LINK = os.getenv('SECRET_LINK', 'https://your-secret-link.com')
# Link undangan untuk grup atau channel
INVITE_LINKS = os.getenv('INVITE_LINKS', 'invite_link_1,invite_link_2,invite_link_3,invite_link_4,invite_link_5').split(',')

def check_membership(user_id, context):
    joined_groups = 0
    for group_id in GROUP_IDS:
        try:
            member = context.bot.get_chat_member(group_id, user_id)
            if member.status in ['member', 'administrator', 'creator']:
                joined_groups += 1
        except:
            pass
    return joined_groups == len(GROUP_IDS)

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    args = context.args
    if args:
        param = args[0]  # Mengambil parameter setelah '/start'
        if param.startswith("get_"):
            if check_membership(user.id, context):
                update.message.reply_text(f'Ini link Anda: {SECRET_LINK}')
            else:
                keyboard_buttons = [
                    [InlineKeyboardButton("JOIN", url=INVITE_LINKS[0])],
                    [InlineKeyboardButton("JOIN", url=INVITE_LINKS[1])],
                    [InlineKeyboardButton("JOIN", url=INVITE_LINKS[2])],
                    [InlineKeyboardButton("JOIN", url=INVITE_LINKS[3])],
                    [InlineKeyboardButton("JOIN", url=INVITE_LINKS[4])],
                    [InlineKeyboardButton("LANJUTKAN", callback_data='check')]
                ]
                keyboard = InlineKeyboardMarkup(keyboard_buttons)
                update.message.reply_text('WAJIB JOIN SEBELUM MELANJUTKAN. Setelah bergabung, klik tombol "LANJUTKAN".', reply_markup=keyboard)
        else:
            update.message.reply_text('Parameter tidak dikenali.')
    else:
        update.message.reply_text('Gunakan parameter setelah /start untuk melanjutkan.')

def ulangi(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = query.from_user
    query.answer()
    
    if check_membership(user.id, context):
        query.edit_message_text(f'Ini link Anda: {SECRET_LINK}')
    else:
        query.edit_message_text('WAJIB JOIN SEBELUM MELANJUTKAN. Setelah bergabung, klik tombol "LANJUTKAN".')

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(ulangi, pattern='check'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
