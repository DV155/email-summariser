import os
import msal
import requests
from datetime import datetime, timedelta, timezone, days

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
    emails = []
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    return emails


if __name__ == '__main__':
    for e in getOutlook():
        '''placeholder'''