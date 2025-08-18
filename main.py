from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import datetime
from commands import start_command, add_remind, notification, hello, linkgoogle, sendcode, connect_to_chat, connect_events, CodeHandler, load_context
from database import DataBase, con, cur, db
from api.GoogeParse import ParseEvents
from google.oauth2.credentials import Credentials



TOKEN = "8314871875:AAEQZOA3Z150_Fd7akq9l-kIBBV4dNsCG4U"


def main():
    load_context()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("remind", add_remind))
    app.add_handler(CommandHandler("link", linkgoogle))
    app.add_handler(CommandHandler("code", sendcode))
    app.add_handler(CommandHandler("conn", connect_to_chat))
    app.add_handler(CommandHandler("events", connect_events))
    app.add_handler(MessageHandler(filters=filters.TEXT, callback=CodeHandler))

    job1 = app.job_queue.run_repeating(check_reminders, interval=5, first=1, name="check_reminders")
    job1.job.max_instances = 5

    job2 = app.job_queue.run_repeating(parse_googles, interval=10, first=1, name="parse_googles")
    job2.job.max_instances = 5

    app.run_polling()


async def check_reminders(context: ContextTypes.DEFAULT_TYPE):
        app = context.application

        ids = db.get_all("id")
        print(ids)
        msgs = db.get_all("msg")
        finishes = db.get_all("finish")
        chat_ids = db.get_all("chat_id")


        if ids is None:
            return

        for i in range(len(ids)):

            if  int(finishes[i]) <= int(datetime.datetime.now().timestamp()) < int(finishes[i]) + 5:

                await notification(app, ids[i], msgs[i], chat_ids[i])
                db.remove_reminder(ids[i])


async def parse_googles(context: ContextTypes.DEFAULT_TYPE):
    id = db.get_google("id")
    token = db.get_google("token")
    r_token = db.get_google("r_token")

    print(id)

    if id is None:
        return

    for i in range(len(id)):

        creds = Credentials(

            token=token[i],
            refresh_token=r_token[i],
            token_uri="https://oauth2.googleapis.com/token",
            client_id="273973346204-b9v7smig8h522jp4fm6ocnan0tr4bk1b.apps.googleusercontent.com",
            client_secret="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",
            scopes=["https://www.googleapis.com/auth/calendar.readonly"]
        )
        print("new")
        ParseEvents(creds, id[i], -4816945682)


if __name__ == "__main__":
    main()

