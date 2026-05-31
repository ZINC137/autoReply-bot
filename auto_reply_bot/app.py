from __future__ import annotations

import os
from pathlib import Path
from xml.sax.saxutils import escape

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request

from auto_reply_bot.reply_engine import DEFAULT_REPLY, choose_reply, load_rules


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_RULES_PATH = BASE_DIR / "replies.json"


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    rules_path = Path(os.getenv("REPLY_RULES_PATH", DEFAULT_RULES_PATH))
    default_reply = os.getenv("DEFAULT_REPLY", DEFAULT_REPLY)

    @app.get("/")
    def health() -> tuple[dict[str, str], int]:
        return {"status": "ok", "service": "autoReply-bot"}, 200

    @app.get("/rules")
    def rules_preview() -> Response:
        rules = load_rules(rules_path)
        return jsonify(
            {
                "rules": [
                    {"name": rule.name, "pattern": rule.pattern, "reply": rule.reply}
                    for rule in rules
                ]
            }
        )

    @app.post("/sms")
    def sms_reply() -> Response:
        incoming_message = request.form.get("Body", "")
        rules = load_rules(rules_path)
        reply = choose_reply(incoming_message, rules, default_reply)
        twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{escape(reply)}</Message></Response>'
        return Response(twiml, mimetype="application/xml")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)

