import json
import webview
from claudeTalking import *
from mailGmail import getGmail


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
