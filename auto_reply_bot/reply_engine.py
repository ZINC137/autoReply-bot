from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


DEFAULT_REPLY = (
    "Thanks for texting. I am away right now, but I will get back to you soon."
)

STOP_WORDS = {"stop", "unsubscribe", "cancel", "quit", "end"}


@dataclass(frozen=True)
class ReplyRule:
    name: str
    pattern: str
    reply: str

    def matches(self, message: str) -> bool:
        return re.search(self.pattern, message, flags=re.IGNORECASE) is not None


def load_rules(path: str | Path) -> list[ReplyRule]:
    rules_path = Path(path)
    payload = json.loads(rules_path.read_text(encoding="utf-8"))

    rules: list[ReplyRule] = []
    for item in payload.get("rules", []):
        rules.append(
            ReplyRule(
                name=str(item["name"]),
                pattern=str(item["pattern"]),
                reply=str(item["reply"]),
            )
        )
    return rules


def normalize_message(message: str | None) -> str:
    return " ".join((message or "").strip().split())


def is_opt_out(message: str | None) -> bool:
    normalized = normalize_message(message).lower()
    return normalized in STOP_WORDS


def choose_reply(
    message: str | None,
    rules: list[ReplyRule],
    default_reply: str = DEFAULT_REPLY,
) -> str:
    normalized = normalize_message(message)

    if not normalized:
        return "I received your message, but it looked empty. Please try again."

    if is_opt_out(normalized):
        return "You have been unsubscribed and will not receive auto-replies."

    for rule in rules:
        if rule.matches(normalized):
            return rule.reply

    return default_reply

