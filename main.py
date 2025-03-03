from src.email_handler import authenticate_gmail, get_emails
from src.calendar_reader import authenticate_google_calendar, get_upcoming_events

def main():
    print("Starting OCI AI Assistant...")
    
    # Email section
    print("\nFetching recent emails...")
    gmail_service = authenticate_gmail()
    emails = get_emails(gmail_service)
    for email in emails:
        print(f"- {email['summary']}")
    
    # Calendar section
    print("\nFetching upcoming calendar events...")
    calendar_service = authenticate_google_calendar()
    events = get_upcoming_events(calendar_service, days_ahead=7)
    for event in events:
        print(f"- {event['start']}: {event['summary']}")

if __name__ == "__main__":
    main()