import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Scopes for Google Calendar API (read-only access)
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google_calendar():
    """Authenticate with Google Calendar API and return the service object."""
    creds = None
    # Load existing token if it exists
    if os.path.exists('token_calendar.json'):
        creds = Credentials.from_authorized_user_file('token_calendar.json', SCOPES)
    # If no valid credentials, refresh or generate new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for next time
        with open('token_calendar.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def get_upcoming_events(service, days_ahead=7):
    """Fetch upcoming events from the primary calendar."""
    # Get the current time in UTC
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # Calculate the end time (e.g., 7 days from now)
    end_time = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'

    # Fetch events
    events_result = service.events().list(
        calendarId='primary',  # Use 'primary' for the user's main calendar
        timeMin=now,
        timeMax=end_time,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    if not events:
        print("No upcoming events found.")
        return []

    # Process and return events
    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'No title')
        event_list.append({'start': start, 'summary': summary})
    return event_list

def main():
    """Main function to test the calendar reader."""
    print("Reading your Google Calendar...")
    service = authenticate_google_calendar()
    events = get_upcoming_events(service, days_ahead=7)
    
    if events:
        print(f"Upcoming events in the next 7 days:")
        for event in events:
            print(f"- {event['start']}: {event['summary']}")

if __name__ == "__main__":
    main()