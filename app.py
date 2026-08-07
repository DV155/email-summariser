import json
import webview
from claudeTalking import *
import sys, os, keyring
from mailGmail import getGmail

SERVICE, KEY_NAME = "email-summariser", "anthropic"

# --- Key-entry window (first run only) ---
SETUP_HTML = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
  html, body { margin: 0; height: 100%; }
  body { font-family: 'Segoe UI', sans-serif; background: #1e1e2e; color: #cdd6f4;
         padding: 2rem; box-sizing: border-box; }
  input { width: 100%; padding: 8px; box-sizing: border-box; margin-top: 8px; }
  button { margin-top: 12px; padding: 8px 16px; cursor: pointer; }
  .err { color: #f38ba8; margin-top: 8px; min-height: 1em; }
</style></head><body>
  <h3>Enter your Anthropic API key</h3>
  <p>Stored securely on this computer. You only enter it once.</p>
  <input id="key" type="password" placeholder="sk-ant-..." />
  <button onclick="save()">Save</button>
  <div class="err" id="err"></div>
  <script>
    async function save() {
      const res = await pywebview.api.save_key(document.getElementById('key').value);
      if (!res.ok) document.getElementById('err').textContent = res.error;
    }
  </script>
</body></html>
"""

class SetupApi:
    def save_key(self, key):
        key = (key or "").strip()
        if not key:
            return {"ok": False, "error": "Please paste a key."}
        keyring.set_password(SERVICE, KEY_NAME, key)
        self._window.destroy()
        return {"ok": True}

def runSetup():
    api = SetupApi()
    api._window = webview.create_window(
        "Setup", html=SETUP_HTML, js_api=api, width=460, height=280
    )
    webview.start()

def hasKey():
    return bool(keyring.get_password(SERVICE, KEY_NAME))

# --- Main summary window ---
HTML = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
  html, body { margin: 0; height: 100%; }
  body { font-family: 'Segoe UI', sans-serif; background: #1e1e2e; color: #cdd6f4;
         padding: 2rem; box-sizing: border-box; }
  #output { white-space: pre-wrap; line-height: 1.6; }
  #close { position: fixed; top: 10px; right: 14px; cursor: pointer; opacity: .5; }

  #loader { display: flex; flex-direction: column; align-items: center;
            justify-content: center; height: 80vh; gap: 1rem; }
  .spinner { width: 40px; height: 40px; border: 4px solid #45475a;
             border-top-color: #cba6f7; border-radius: 50%;
             animation: spin 0.8s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .hidden { display: none; }
</style></head><body>
  <div id="close" onclick="pywebview.api.close()">✕</div>
  <div id="loader">
    <div class="spinner"></div>
    <div>Fetching and summarising your inbox…</div>
  </div>
  <div id="output"></div>
  <script>
    function appendText(chunk) {
      const loader = document.getElementById('loader');
      if (loader) loader.remove();          // first chunk kills the spinner
      document.getElementById('output').textContent += chunk;
      window.scrollTo(0, document.body.scrollHeight);
    }
  </script>
</body></html>
"""

class Api:
    def close(self):
        webview.windows[0].destroy()

def formatEmails(emails, max_body=1500):
    blocks = []
    for e in emails:
        body = e["body"][:max_body]
        blocks.append(
            f"From: {e['from']}\nDate: {e['date']}\nSubject: {e['subject']}\n\n{body}"
        )
    return "\n\n---\n\n".join(blocks)

def run(window):
    window.events.loaded.wait()
    try:
        emails = getGmail(days=7)
        messages = []
        add_user_message(messages, formatEmails(emails))
        chat(
            messages,
            system=system_prompt,
            on_text=lambda t: window.evaluate_js(f"appendText({json.dumps(t)})"),
        )
    except Exception as e:
         window.evaluate_js(f"appendText({json.dumps('⚠ Error: ' + str(e))})")
if __name__ == "__main__":
    if not hasKey():
        runSetup()
        webview.create_window(
            "Setup complete",
            html="<body style='font-family:sans-serif;background:#1e1e2e;"
                 "color:#cdd6f4;padding:2rem'><h3>Key saved</h3>"
                 "<p>Please reopen the app to see your summary.</p></body>",
        )
        webview.start()
        sys.exit(0)

    window = webview.create_window(
        "Weekly Email Summary", html=HTML,
        frameless=True, width=600, height=800, js_api=Api(),
    )
    webview.start(run, window)