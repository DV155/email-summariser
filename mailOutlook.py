import os
import msal
import requests
from datetime import datetime, timedelta, timezone, days
from bs4 import BeautifulSoup

SCOPES = ["Mail.Read"]
CACHE_FILE = "ms-token.json"

def getCreds():
    cache = msal.SerializableTokenCache()
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            cache.deserialize(f.read())


    app = msal.PublicClientApplication(os.getenv("MS_CLIENT_ID"), authority="https://login.microsoftonline.com/consumers", token_cache=cache)
    accounts = app.get_accounts()
    result = app.acquire_token_silent(SCOPES, account=accounts[0]) if accounts else None
    if not result:
        result = app.acquire_token_interactive(scopes=SCOPES)

    if cache.has_state_changed:
        with open(CACHE_FILE) as f:
            f.write(cache.serialize())

    if "access_token" not in result:
        raise RuntimeError(result.get("error_description", result))
    
    return result["acess_token"]

    

def getOutlook():
    token = getCreds()
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    r = requests.get("https://graph.microsoft.com/v1.0/me/messages", headers={"Authorization": f"Bearer {token}"}, params={"$filter": f"receivedDateTime ge {since}", "$top": 50})
    r.raise_for_status()

    emails = []
    for m in r.json()["value"]:
        body = m["body"]["content"]
        if m["body"]["contentType"] == "html":
            body = BeautifulSoup(body, "html.parser").get_text(" ", strip=True)
        emails.append({
            "from": m["from"]["emailAddress"]["address"],
            "subject": m.get("subject") or "(no subject)",
            "date": m["receivedDateTime"],
            "body": body[:1500],
        })


    return emails


if __name__ == '__main__':
    for e in getOutlook():
        print(e["date"], "|", e["from"], "|", e["subject"])