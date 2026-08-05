"""
Astelhub Bot — простой бот с кнопками-ссылками на каналы.

ЧТО НУЖНО СДЕЛАТЬ ПЕРЕД ЗАПУСКОМ:
1. Установи библиотеку (один раз, в терминале/командной строке):
   pip install python-telegram-bot --upgrade

2. Вставь свой токен от BotFather вместо "ВСТАВЬ_СЮДА_ТОКЕН" ниже.

3. Запусти файл:
   python astelhub_bot.py

Бот будет работать, пока запущен этот скрипт (окно терминала открыто).
Чтобы бот работал 24/7, его нужно потом разместить на сервере/хостинге
(это отдельный шаг, скажи — подскажу варианты, когда дойдёшь до этого).
"""

import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]

# Ссылки на твои каналы и чаты
LINKS = {
    "cis": {
        "title": "🇷🇺 CIS",
        "channel": "https://t.me/astel_cis",
        "chat": "https://t.me/astel_cis_chat",
    },
    "ua": {
        "title": "🇺🇦 UA",
        "channel": "https://t.me/astel_ua",
        "chat": "https://t.me/astel_ua_chat",
    },
    "en": {
        "title": "🇬🇧 EN",
        "channel": "https://t.me/astel_en",
        "chat": "https://t.me/astel_en_chat",
    },
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(data["title"], callback_data=key)]
        for key, data in LINKS.items()
    ]
    await update.message.reply_text(
        "Привет! Выбери язык / регион:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def language_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    key = query.data
    data = LINKS[key]

    keyboard = [
        [InlineKeyboardButton("📢 Канал", url=data["channel"])],
        [InlineKeyboardButton("💬 Чат", url=data["chat"])],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back")],
    ]
    await query.edit_message_text(
        f"{data['title']} — выбери, куда перейти:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(data["title"], callback_data=key)]
        for key, data in LINKS.items()
    ]
    await query.edit_message_text(
        "Привет! Выбери язык / регион:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(back_to_menu, pattern="^back$"))
    app.add_handler(CallbackQueryHandler(language_chosen, pattern="^(cis|ua|en)$"))

    print("Бот запущен. Останови через Ctrl+C.")
    app.run_polling()


if __name__ == "__main__":
    main()
