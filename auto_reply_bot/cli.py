from __future__ import annotations

import argparse
from pathlib import Path

from auto_reply_bot.reply_engine import DEFAULT_REPLY, choose_reply, load_rules


def main() -> None:
    parser = argparse.ArgumentParser(description="Test auto-replies from the terminal.")
    parser.add_argument("message", help="Incoming message text to simulate.")
    parser.add_argument(
        "--rules",
        default=Path(__file__).resolve().parent / "replies.json",
        type=Path,
        help="Path to the JSON reply rules file.",
    )
    parser.add_argument(
        "--default-reply",
        default=DEFAULT_REPLY,
        help="Fallback reply when no rule matches.",
    )
    args = parser.parse_args()

    rules = load_rules(args.rules)
    print(choose_reply(args.message, rules, args.default_reply))


if __name__ == "__main__":
    main()

