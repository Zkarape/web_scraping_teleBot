# from telegram import Update
# from config import my_token
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text(f'Hello {update.effective_user.first_name}')

# async def news_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

# app = ApplicationBuilder().token(my_token).build()

# app.add_handler(CommandHandler("start", start))

# app.run_polling()

import config
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from bs4 import BeautifulSoup
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# Define conversation states
SEARCH_KEYWORD = 0
# Replace this with your actual token
my_token = config.my_token

def search_website(query):
    url = "https://new.arlis.am/am/"
    params = {"q": query}

    response = requests.get(url, params=params, verify=False)
    # print("yeeeeyyyy")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Use BeautifulSoup to extract data from the HTML content
        # Modify this part based on the website's structure
        search_results = []
        for item in soup.find_all("div", class_="your-result-class"):
            title = item.find("h2").text
            description = item.find("p").text
            link = item.find("a")["href"]
            search_results.append({"title": title, "description": description, "link": link})
        # print("here it issss", search_results)
        return search_results
    else:
        return None

def start(update, context):
    update.message.reply_text("Welcome to the Web Scraper Bot!")
    show_search_window(update)
    return SEARCH_KEYWORD

def show_search_window(update):
    keyboard = [
        [InlineKeyboardButton("Submit", callback_data='submit')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Enter a keyword to search:", reply_markup=reply_markup)


def search_keyword(update, context):
    update.message.reply_text("Please enter the keyword you want to search for:")
    return SEARCH_KEYWORD
# def start(update: Update, context: CallbackContext):
#     update.message.reply_text(f'Hello {update.effective_user.first_name}')

def news_filter(update: Update, context: CallbackContext):
    user_input = update.message.text

    search_results = search_website(user_input)

    if search_results:
        message = ""
        for search_result in search_results:
            message += f"**Title:** {search_result['title']}\n"
            message += f"**Description:** {search_result['description']}\n"
            message += f"**Link:** {search_result['link']}\n\n"

        update.message.reply_text(message, parse_mode='Markdown')
    else:
        update.message.reply_text("No search results found.")

def button(update, context):
    query = update.callback_query
    if query.data == 'submit':
        query.answer()
        search_website(update, context)
    else:
        query.answer(text="Unknown button")


if __name__ == '__main__':
    updater = Updater(token=my_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addfilters", news_filter))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, news_filter))

    updater.start_polling()
    updater.idle()
