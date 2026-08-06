from anthropic import Anthropic


import msal
import requests

from mailGmail import getGmail
'''from mailOutlook import getOutlook'''

import os
import base64
from datetime import date, datetime, timedelta
from pathlib import Path
from email import message_from_bytes
from dotenv import load_dotenv
import keyring

load_dotenv()

SERVICE = "email-summariser"
KEY_NAME = "anthropic"

model = "claude-haiku-4-5"

def getApiKey():
    key = keyring.get_password(SERVICE, KEY_NAME)
    if not key:
        key = input("Paste your Anthropic API key").strip()
        keyring.set_password(SERVICE, KEY_NAME, key)
    return key

_client = None
def getClient():
    global _client
    if _client is None:
        _client = Anthropic(api_key=getApiKey())
    return _client



def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def chat(messages, system=None, temperature=0.3, stop_sequences=None, on_text=None):
    params = {
        "model": model,
        "max_tokens": 1500,
        "messages": messages,
        "temperature": temperature
    }
    
    if system:
        params["system"] = system
            
            
            
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    
    with getClient().messages.stream(**params) as stream:
        for text in stream.text_stream:
            if on_text:
                on_text(text)
        message = stream.get_final_message()

    return message.content[0].text


system_template = """
You summarise a user's e-mail inbox covering the last 7 days.

You receive a list of emails, each with fields: "from", "subject", "date", "body".
Gmail and Outlook emails are already merged into one list — treat them as a single
inbox and never group or label by provider.

Today's date is {today}. Use it to decide whether a dated appointment or
reservation has already passed.

Output:
- Begin with exactly this line: "Hello! Here is the report for the past 7 days"
- Group related emails (same sender, thread, or topic) into sections, ordered
  most important to least important. Treat personal/work messages, deadlines,
  security or account notices, and bills as more important than newsletters or
  automated notifications.
- Within each section, be concise but accurate: cut filler, keep the specifics —
  names, dates, amounts, and any action requested.

Rules:
- Purely promotional/marketing emails: list sender + subject only, do not summarise.
- If a body refers to a consequential attachment (invoice, contract, ticket),
  note that it references an attachment you cannot read.
- Skip any appointment/reservation email dated before {today}.
- If there are no emails at all, reply with a single short line saying there was
  nothing to report, and summarise nothing.

Never use conversational wrappers, preambles, sign-offs, or flattery beyond the
required greeting line.
"""

system_prompt = system_template.format(today=date.today().isoformat )

if __name__ == "__main__":
    emails = getGmail(days=7)
    messages = []
    add_user_message(messages, str(emails))
    summary = chat(messages, system=system_prompt)
    print(summary)

