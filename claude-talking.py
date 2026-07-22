from anthropic import Anthropic


import msal
import requests

import webview

import os
import json
import base64
from datetime import datetime, timedelta
from pathlib import Path
from email import message_from_bytes
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()
model = "claude-opus-4-6"

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def chat(messages, system=None, temperature=0.3, stop_sequences=None):
    params = {
        "model": model,
        "max_tokens": 2500,
        "messages": messages,
        "temperature": temperature
    }
    
    if system:
        params["system"] = system
            
            
            
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    
    message = client.messages.create(**params)
    return message.content[0].text


system_prompt = """
You are a bot that summarises the contents of an e-mail inbox over the course of 7 days.
You should:
- Split the emails into sections by topic/sender, start with most important to least important;
- Keep the gmail and outlook emails together for this purpose, do not split them into separate sections;
- Before summarising, greet the user with "[Greeting given by user], [Username]! Here is the report for the past 7 days";
- Summarise them in a concise manner while retaining a large degree of accuracy - drop the fluff but keep the important things;
- If no emails are present in either inbox, simply say so without summarising anything;
You should NOT:
- Use conversational wrappers of any kind, unless mentioned in the "You should:" section;
- Use sycophantic fillers of any kind, unless mentioned in the "You should:" section;
- Read or summarise emails marked as spam;
- Read or summarise emails related to appointments/reservations the date for which is before the current system date;
"""

