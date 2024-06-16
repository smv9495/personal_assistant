import datetime
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from logging_module.logging_config import get_logger

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

logger = get_logger(__name__)


class CalendarAPI():
    def __init__(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        logger.info("Credentials verified for Calendar API")
        try:
            self.service = build("calendar", "v3", credentials=creds)
        except Exception as e:
            logger.error(f"Error occurred while building calendar service. Error: {e}")
    
    def view_events(self, next_n:int=10):
        # Call the Calendar API
        # now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        logger.info(f"Getting the upcoming {next_n} events as of {now}")
        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=next_n,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        logger.debug(f"Upcoming Events\n{events}")
        if not events:
            logger.info("No upcoming events found.")
            return None

        # Prints the start and name of the next_n events
        event_summary=[]
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            event_summary.append((start, event["summary"]))
        return event_summary