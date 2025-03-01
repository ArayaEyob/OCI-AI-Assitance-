import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from transformers import pipeline

# Summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Gmail API setup
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_emails(service, max_results=5):
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = msg_data['snippet']
        summary = summarizer(snippet, max_length=30, min_length=10, do_sample=False)[0]['summary_text']
        emails.append({'id': msg['id'], 'snippet': snippet, 'summary': summary})
    return emails

if __name__ == "__main__":
    service = authenticate_gmail()
    emails = get_emails(service)
    for email in emails:
        print(f"Original: {email['snippet']}")
        print(f"Summary: {email['summary']}\n")