import os
import json
import requests

WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

message = {
    "text": "🚨 AI DevSecOps Alert",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Vulnerability Detected During CI/CD Scan*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "AI remediation workflow triggered successfully."
            }
        }
    ]
}

response = requests.post(
    WEBHOOK_URL,
    data=json.dumps(message),
    headers={"Content-Type": "application/json"}
)

print("Slack Status:", response.status_code)
print("Slack Response:", response.text)