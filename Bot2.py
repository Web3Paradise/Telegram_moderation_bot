from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a dictionary to store banned users
banned_users = {}

# Define a dictionary to store muted users
muted_users = {}

# Define start function
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am your moderation bot. How can I help you?')

# Define echo function
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

# Define function to handle /ban command
def ban(update: Update, context: CallbackContext) -> None:
    user = update.message.reply_to_message.from_user
    banned_users[user.id] = user.name
    update.message.reply_text(f'{user.name} has been banned.')
    context.bot.kick_chat_member(update.message.chat_id, user.id)

# Define function to handle /unban command
def unban(update: Update, context: CallbackContext) -> None:
    user = update.message.reply_to_message.from_user
    if user.id in banned_users:
        del banned_users[user.id]
    update.message.reply_text(f'{user.name} has been unbanned.')
    context.bot.unban_chat_member(update.message.chat_id, user.id)

# Define function to handle /mute command
def mute(update: Update, context: CallbackContext) -> None:
    user = update.message.reply_to_message.from_user
    muted_users[user.id] = user.name
    update.message.reply_text(f'{user.name} has been muted.')
    context.bot.restrict_chat_member(update.message.chat_id, user.id, can_send_messages=False)

# Define function to handle /unmute command
def unmute(update: Update, context: CallbackContext) -> None:
    user = update.message.reply_to_message.from_user
    if user.id in muted_users:
        del muted_users[user.id]
    update.message.reply_text(f'{user.name} has been unmuted.')
    context.bot.restrict_chat_member(update.message.chat_id, user.id, can_send_messages=True)

# Define function to handle text messages
def text_message(update: Update, context: CallbackContext) -> None:
    # Auto-moderation: Check for inappropriate language
    if "bad_word" in update.message.text:
        update.message.reply_text("Please refrain from using inappropriate language.")
        return

    # Auto-moderation: Check for spam
    if len(update.message.text) > 100:
        update.message.reply_text("Please refrain from sending long messages.")
        return

    # Keyword alerts
    if "important_keyword" in update.message.text:
        context.bot.send_message(chat_id=update.message.chat_id, text="Hey, someone mentioned an important keyword!")

    # Welcome message for new users
    if update.message.new_chat_members:
        for new_member in update.message.new_chat_members:
            update.message.reply_text(f"Welcome {new_member.first_name} to the group!")

# Define function to handle /banlist command
def banlist(update: Update, context: CallbackContext) -> None:
    if banned_users:
        update.message.reply_text("List of banned users:\n" + "\n".join([f"{user_id} - {user_name}" for user_id, user_name in banned_users.items()]))
    else:
        update.message.reply_text("No users are banned.")

# Define function to handle /mutelist command
def mutelist(update: Update, context: CallbackContext) -> None:
    if muted_users:
        update.message.reply_text("List of muted users:\n" + "\n".join([f"{user_id} - {user_name}" for user_id, user_name in muted_users.items()]))
    else:
        update.message.reply_text("No users are muted.")

# Define main function
def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ban", ban))
    dp.add_handler(CommandHandler("unban", unban))
    dp.add_handler(CommandHandler("mute", mute))
    dp.add_handler(CommandHandler("unmute", unmute))
    dp.add_handler(CommandHandler("banlist", banlist))
    dp.add_handler(CommandHandler("mutelist", mutelist))

    # on non command i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

# Call the main function to run the bot
if __name__ == '__main__':
    main()
