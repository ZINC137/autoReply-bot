# autoReply-bot

A small SMS auto-reply bot that receives incoming texts through a webhook and sends back a rule-based response.

The project is designed for services such as Twilio, which can call the `/sms` endpoint whenever a text arrives. It does not read messages directly from your phone or private apps.

## Features

- SMS webhook at `POST /sms`
- TwiML XML response compatible with Twilio Messaging webhooks
- JSON-based reply rules
- Opt-out handling for `STOP`, `UNSUBSCRIBE`, `CANCEL`, `QUIT`, and `END`
- CLI simulator for testing replies locally
- Unit tests for reply selection logic

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run Locally

```bash
flask --app auto_reply_bot.app run --port 5000
```

Health check:

```bash
curl http://127.0.0.1:5000/
```

Simulate an incoming SMS:

```bash
curl -X POST http://127.0.0.1:5000/sms -d "From=+15551234567" -d "Body=hey, are you free?"
```

## Test Reply Logic Without Running The Server

```bash
python -m auto_reply_bot.cli "this is urgent"
```

## Edit Replies

Update `auto_reply_bot/replies.json`:

```json
{
  "name": "example",
  "pattern": "\\b(example|demo)\\b",
  "reply": "Your auto-reply text here."
}
```

Patterns are regular expressions and are matched case-insensitively.

## Connect To Twilio

1. Create or open a Twilio phone number.
2. Expose your local server using a tunnel such as ngrok.
3. Set the Messaging webhook URL to:

```text
https://your-public-url.example/sms
```

4. Use HTTP `POST`.

## Run Tests

```bash
python -m unittest discover -s tests
```
