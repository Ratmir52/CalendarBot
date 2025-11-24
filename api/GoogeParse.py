
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
from database import db
from dateutil import parser


def ParseEvents(creds, id, chat_id):

    service = build("calendar", "v3", credentials=creds)

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()


    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=15,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        return

    for event in events:

        iso_time = event["start"].get("dateTime", event["start"].get("date"))
        dt = parser.isoparse(iso_time)

        start_unix = int(dt.timestamp())
        summary = event.get("summary", "Без названия")

        print(f"Timer {summary} дата unix: {start_unix}")

        db.add_reminder(id, chat_id, summary, start_unix)



