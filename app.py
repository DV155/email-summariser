import json
import webview
from claudeTalking import *
from mailGmail import getGmail

HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    html, body { margin: 0; height: 100%; }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #1e1e2e; color: #cdd6f4;
      padding: 2rem; box-sizing: border-box;
    }
    #output { white-space: pre-wrap; line-height: 1.6; }
    #close { position: fixed; top: 10px; right: 14px; cursor: pointer; opacity: .5; }
  </style>
</head>
<body>
  <div id="close" onclick="pywebview.api.close()">✕</div>
  <div id="output"></div>
  <script>
    function appendText(chunk) {
      document.getElementById('output').textContent += chunk;
      window.scrollTo(0, document.body.scrollHeight);
    }
  </script>
</body>
</html>
"""

class Api:
    def close(self):
        webview.windows[0].destroy


def run(window):
    window.events.loaded.wait()
    emails = getGmail(days=7)
    messages = []
    add_user_message(messages, str(emails))
    chat(
        messages,
        system=system_prompt,
        on_text=lambda t: window.evaluate_js(f"appendText({json.dumps(t)})"),
    )

if __name__ == "__main__":
    window = webview.create_window(
        "Weekly Email Summary", html=HTML,
        frameless=True, width=600, height=800, js_api=Api(),
    )
    webview.start(run, window)