import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Your bot token obtained from BotFather
bot_token = '6494550350:AAETENK33De_V5ovXlzWE3vovWPzTN2QL5E'

# Create an Updater for your bot
updater = Updater(token=bot_token, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Define a function to handle the /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! I am your bot. Send me a message, and I will reply.')

# Define a function to echo back user messages
def echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)

# Register command and message handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Start the bot
def main():
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

