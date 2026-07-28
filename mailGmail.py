from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from bs4 import BeautifulSoup
from email import message_from_bytes
from email.policy import default 
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def getHTML(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup:
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)

def getCreds():
    creds = None

    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except:
            creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
    

def getGmail(days=7):
    creds = getCreds()

    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', q=f'newer_than:{days}d', maxResults=100).execute()
    messages = results.get('messages', [])

    emails = []
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id'], format='raw').execute()
        raw = base64.urlsafe_b64decode(txt['raw'])
        mime_msg = message_from_bytes(raw, policy=default)

        body_part = mime_msg.get_body(preferencelist=('plain', 'html'))
        if body_part:
            body = body_part.get_content()
            if body.get_content_type() == "text/html":
                body = getHTML(body)
        else:
            body = ''


        emails.append({
            'from': mime_msg['From'] or '',
            'subject': mime_msg['Subject'] or '(no subject)',
            'date': mime_msg['Date'] or '',
            'body': body,
        })


    return emails


if __name__ == '__main__':
    for e in getGmail():
        '''print(e['date'], '|', e['from'], '|', e['subject'])'''