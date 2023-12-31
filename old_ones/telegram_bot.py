# import logging
# from telegram import Update
# from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
# import types

# # Set up logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# bot_token = '6494550350:AAETENK33De_V5ovXlzWE3vovWPzTN2QL5E'

# updater = Updater(token=bot_token, use_context=True)

# dispatcher = updater.dispatcher

# async def start(message: types.Message):
#     start_buttons = ["All news", "Last 5 news", "Updated news"]
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*start_buttons)

#     # await message.answer("Лента новостей", reply_markup=keyboard)

# def echo(update: Update, context: CallbackContext):
#     update.message.reply_text(update.message.text)

# dispatcher.add_handler(CommandHandler("start", start))
# dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# # Start the bot
# def main():
#     updater.start_polling()
#     updater.idle()

# if __name__ == '__main__':
#     main()

#//////////////////////////////////////////////
# def process_text_message(text)
# {
#     parse_website(text)

# }

# def show_search_window(update):
#     keyboard = [
#         [InlineKeyboardButton("Submit", callback_data='submit')],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.message.reply_text("Enter a keyword to search:", reply_markup=reply_markup)

# def search_keyword(update: Update, context: CallbackContext):
#     user_id = update.message.from_user.id
#     context.user_data[user_id] = {'keyword': None}

#     update.message.reply_text("Please enter the keyword you want to search for:")
#     return SEARCH_KEYWORD

# def search_website(update: Update, context: CallbackContext):
#     user_id = update.message.from_user.id
#     keyword = update.message.text
#     context.user_data[user_id]['keyword'] = keyword

#     if not keyword:
#         update.message.reply_text("You didn't enter a keyword. Please try again.")
#         return SEARCH_KEYWORD
#     else:
#         # Access the stored keyword using context.user_data[user_id]['keyword']
#         stored_keyword = context.user_data[user_id]['keyword']
#         print("Stored keyword:", stored_keyword)
        
#         # Now you can use the stored keyword in your search logic.
#         # For example, you can use 'stored_keyword' in the URL or for web scraping.
        
#         # Rest of your search logic here.

#     return ConversationHandler.END


# def news_filter(update: Update, context: CallbackContext):
#     user_input = update.message.text

#     search_results = search_website(user_input)

#     if search_results:
#         message = ""
#         for search_result in search_results:
#             message += f"**Title:** {search_result['title']}\n"
#             message += f"**Description:** {search_result['description']}\n"
#             message += f"**Link:** {search_result['link']}\n\n"

#         update.message.reply_text(message, parse_mode='Markdown')
#     else:
        # update.message.reply_text("No search results found.")

import asyncio
import datetime
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
from config import token, user_id
from main import check_news_update


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все новости", "Последние 5 новостей", "Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Лента новостей", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        # news = f"<b>{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}</b>\n" \
        #        f"<u>{v['article_title']}</u>\n" \
        #        f"<code>{v['article_desc']}</code>\n" \
        #        f"{v['article_url']}"
        # news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
        #        f"{hunderline(v['article_title'])}\n" \
        #        f"{hcode(v['article_desc'])}\n" \
        #        f"{hlink(v['article_title'], v['article_url'])}"
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
               f"{hlink(v['article_title'], v['article_url'])}"

        await message.answer(news)


@dp.message_handler(Text(equals="Последние 5 новостей"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
               f"{hlink(v['article_title'], v['article_url'])}"

        await message.answer(news)


@dp.message_handler(Text(equals="Свежие новости"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                   f"{hlink(v['article_title'], v['article_url'])}"

            await message.answer(news)

    else:
        await message.answer("Пока нет свежих новостей...")


async def news_every_minute():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                       f"{hlink(v['article_title'], v['article_url'])}"

                # get your id @userinfobot
                await bot.send_message(user_id, news, disable_notification=True)

        else:
            await bot.send_message(user_id, "Пока нет свежих новостей...", disable_notification=True)

        await asyncio.sleep(40)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)
