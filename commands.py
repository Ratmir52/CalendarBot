import telegram.ext
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
from datetime import datetime
import sys
import os
from database import DataBase, con, cur, db
import sys
import os
from api.GoogeParse import ParseEvents
import json

usrs_context = {}
token, r_token = None, None

def load_context():
    try:
        global usrs_context

        with open('context.json', 'r') as file:
            usrs_context = json.load(file)

    except json.decoder.JSONDecodeError:
        usrs_context = {}


def save_context():

    with open('context.json', 'w') as file:
        json.dump(usrs_context, file)

# Greeting users.
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Привет! Я бот для создания напоминаний.")

# Get Google auch link.
async def linkgoogle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    with open("api/url.txt", "r") as f:
        url = f.readline()
    await update.message.reply_text(f"Ссылка: {url}")
    msg = await update.message.reply_text(f"Ответным сообщением пришлите access token, выданный на сайте.")

    usrs_context[str(update.message.from_user.id)] = "get_token"
    save_context()

# Get user data received after GoogleAPI authorization.
async def sendcode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parts = update.message.text.split()
    print(parts[1])
    print(parts[2])
    db.add_token(update.message.from_user.id, str(parts[1]), str(parts[2]))



# Connect DataBase for user events in Google Calendar.
async def connect_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        id = update.message.from_user.id
        chat_id = update.message.chat_id
        print(chat_id)
        token = db.get_token(id)
        print(token[1])
        print(token[2])
        creds = Credentials(

            token=token[1],
            refresh_token=token[2],
            token_uri="https://oauth2.googleapis.com/token",
            client_id="273973346204-b9v7smig8h522jp4fm6ocnan0tr4bk1b.apps.googleusercontent.com",
            client_secret="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",
            scopes=["https://www.googleapis.com/auth/calendar.readonly"]
        )

        ParseEvents(creds, id, chat_id)

        return True

    except:
        return False

async def CodeHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global token, r_token
    if update.message.reply_to_message:

        if update.message.reply_to_message.from_user.is_bot:


            if usrs_context[str(update.message.from_user.id)] == "get_token":
                token = update.message.text
                usrs_context[str(update.message.from_user.id)] = "get_r_token"
                await update.message.reply_text("Введите refresh_token.")
                save_context()

            elif usrs_context[str(update.message.from_user.id)] == "get_r_token":
                r_token = update.message.text

                db.add_token(update.message.from_user.id, token, r_token)

                if await connect_events(update, context):

                    await update.message.reply_text("Вы были успешно подключили свой аккаунт Google")

                else:
                    await update.message.reply_text("Ошибка получения данных пожалуйста, проверьте корректность данных")


# User link chat for bot notification.
async def connect_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.message.from_user.id
    chat_id = update.message.chat_id

    db.upd_chat(chat_id, id)






async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("<UNK> <UNK> <UNK> <UNK> <UNK> <UNK> <UNK> <UNK> <UNK>")
    message = update.message.text
    msg = message.split()[1]
    time = message.split()[2]
    t = message.split()[3]

    time_in_seconds = int(time)

    if t == "min":
        time_in_seconds = int(time) * 60

    elif t == "hour":
        time_in_seconds = int(time) * 60 * 60

    elif t == "day":
        time_in_seconds = int(time) * 60 * 60 * 24



    user_id = update.message.from_user.id
    ch_id = update.message.chat_id

    finish_time = datetime.datetime.now().timestamp() + time_in_seconds

    db.add_reminder(user_id, ch_id, msg, finish_time)

async def add_remind(update: Update, context: ContextTypes.DEFAULT_TYPE):

        message = update.message.text

        if "-d" not in message.split():
            msg = message.split()[1]
            time = message.split()[2]
            t = message.split()[3]

            time_in_seconds = int(time)

            if t == "min":
                time_in_seconds = int(time) * 60

            elif t == "hour":
                time_in_seconds = int(time) * 60 * 60

            elif t == "day":
                time_in_seconds = int(time) * 60 * 60 * 24

            else:
                time_in_seconds = int(time)

            user_id = update.message.from_user.id
            ch_id = update.message.chat_id

            finish_time = datetime.datetime.now().timestamp() + time_in_seconds

            db.add_reminder(user_id, ch_id, msg, finish_time)

        else:
            msg = message.split()[2]

            date_str = message.split()[3]
            date_format = "%Y-%m-%d-%H:%M:%S"
            dt_object = datetime.strptime(date_str, date_format)
            unix_timestamp = dt_object.timestamp()

            user_id = update.message.from_user.id
            ch_id = update.message.chat_id

            db.add_reminder(user_id, ch_id, msg, unix_timestamp)






async def notification(app, id, msg, chat_id):

    mention = f"<a href='tg://user?id={id}'>пользователь</a>"
    if chat_id is not None:
        print(1)
        await app.bot.send_message(chat_id = chat_id, text= f"""{mention} Ваш таймер {msg} подошел к концу!!!""", parse_mode=ParseMode.HTML)
    else:
        print(0)


