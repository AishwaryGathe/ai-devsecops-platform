import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

message = {
    "text": "Vulnerability Alert",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*HIGH Vulnerability Found*"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Package:*\nbody-parser"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Severity:*\nHIGH"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*AI Recommendation:*\nUpgrade to 1.20.3"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Approve"
                    },
                    "style": "primary",
                    "value": "approve_fix"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Reject"
                    },
                    "style": "danger",
                    "value": "reject_fix"
                }
            ]
        }
    ]
}

response = requests.post(
    WEBHOOK_URL,
    data=json.dumps(message),
    headers={"Content-Type": "application/json"}
)

print("Slack alert sent:", response.status_code)