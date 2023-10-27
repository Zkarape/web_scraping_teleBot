import config
import requests
import asyncio
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
# from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
# from aiogram import executor
# from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from telegram.ext import CallbackContext
# from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQueryHandler

my_token = config.my_token
# bot = Bot(my_token, parse_mode=types.ParseMode.HTML)
# dp = Dispatcher(bot)
SEARCH_KEYWORD = 0
header_line = "================ News ================"
separator_line = "-" * (len(header_line) + 6)

# Replace this with your actual token
article_data = {}

def parse_website(query):
    url = "https://new.arlis.am/am/"
    print("hiiiiiiiiii")
    if url:
        try:
            # response = requests.get(url)
            # data = {
            #             'form-input': query,  # Replace 'input_field_name' with the actual field name in the website's HTML form
            #         }
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                articles_cards = soup.find_all("a", class_=lambda x: x and x.startswith("cursor-pointer show-lg"))

                for article in articles_cards:
                    article_title = article.find("h5", class_="no_line mtc_h fwn stm_animated").text.strip()
                    article_desc = article.find("div", class_="color-blue helvetica-75").text.strip()
                    article_url = f'{article.get("href")}'
                    article_day = article.find("span", class_=lambda x: x and x.startswith("act-card__about-value helvetica-"))
                    article_month = article.find("span", class_="month")

                    class_attr = article.get('class')
                    full_class_name = ' '.join(class_attr)
                    full_class_name = full_class_name.split("-")
                    necessary_id = full_class_name[1].split(" ")[0]

                    # Create a dictionary to store article data
                    article_data[necessary_id] = {
                        "article_day": article_day.text if article_day else "",
                        "article_month": article_month.text if article_month else "",
                        "article_title": article_title,
                        "article_url": article_url,
                        "article_desc": article_desc
                    }

                with open("news_dict.json", "w") as file:
                    json.dump(article_data, file, indent=4)  # Serialize the dictionary to JSON
            else:
                print("Failed to fetch data from the website.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    else:
        print(f"Website Tower not found in the dictionary.")


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Accountant Bot!")
    # show_search_window(update)


# @dp.message_handler(commands=Filters.text & ~Filters.command)
def handle_text_message(update, context):
    # user_id = update.message.from_user.id
    # text = update.message.text
    print('hereeeeee')
    # await parse_website(text)
    
    # Send a response back to the user
    # await get_all_news(update.message)
    update.message.reply_text(update.message)
    # print(text)
    # await text


def search(update: Update, context: CallbackContext):
    update.message.reply_text("Input and Send a keyword that you want to search in web.")


def get_all_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in news_dict.items():
        news = f"{header_line}\n" \
                f"<b>Date: {v['article_day']} {v['article_month']}</b>\n" \
                f"{separator_line}\n" \
                f"<u>Title: {v['article_title']}</u>\n" \
                f"<code>Description: {v['article_desc']}</code>\n" \
                f"URL: {v['article_url']}\n" \
                f"{separator_line}"

        message.answer(news)


if __name__ == '__main__':
    updater = Updater(token=my_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_message))
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_all_news))
    # print(handle_text_message(updater, context))
    updater.start_polling()
    updater.idle()
