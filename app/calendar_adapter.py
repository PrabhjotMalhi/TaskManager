from datetime import datetime
from models import Task
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
from typing import List

class CalendarAdapter:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        # The file token.pickle stores the user's access and refresh tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('calendar', 'v3', credentials=self.creds)

    def add_task_to_calendar(self, task: Task) -> bool:
        """Add a task to Google Calendar"""
        event = {
            'summary': task.title,
            'description': f"Task ID: {task.id}\n{task.description}",
            'start': {
                'dateTime': task.deadline.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': task.deadline.isoformat(),
                'timeZone': 'UTC',
            },
            'reminders': {
                'useDefault': True
            }
        }

        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            return True
        except Exception as e:
            print(f"Error adding event to calendar: {e}")
            return False

    def remove_task_from_calendar(self, task_id: int) -> bool:
        """Remove a task from Google Calendar"""
        try:
            # Search for the event with the task ID in description
            events_result = self.service.events().list(
                calendarId='primary',
                q=f"Task ID: {task_id}"
            ).execute()
            
            events = events_result.get('items', [])
            if events:
                self.service.events().delete(
                    calendarId='primary',
                    eventId=events[0]['id']
                ).execute()
            return True
        except Exception as e:
            print(f"Error removing event from calendar: {e}")
            return False

    def get_upcoming_tasks(self) -> List[dict]:
        """Get upcoming tasks from Google Calendar"""
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except Exception as e:
            print(f"Error getting upcoming tasks: {e}")
            return []
