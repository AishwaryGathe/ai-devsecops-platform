import os
import json
import requests

# ---------------------------------------------------
# LOAD WEBHOOK
# ---------------------------------------------------

WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# ---------------------------------------------------
# SAMPLE SECURITY DATA
# ---------------------------------------------------

total_vulnerabilities = 14
critical_count = 2
high_count = 5
security_score = 72

# ---------------------------------------------------
# SLACK MESSAGE PAYLOAD
# ---------------------------------------------------

message = {
    "text": "🚨 AI DevSecOps Security Alert",
    "blocks": [

        # Header
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🚨 AI DevSecOps Security Alert"
            }
        },

        # Divider
        {
            "type": "divider"
        },

        # Pipeline Status
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Pipeline Status:*\n✅ Completed"
                },
                {
                    "type": "mrkdwn",
                    "text": "*AI Analysis:*\n✅ Successful"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Container Scan:*\n✅ Trivy Executed"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Slack Integration:*\n✅ Active"
                }
            ]
        },

        # Divider
        {
            "type": "divider"
        },

        # Vulnerability Summary
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    "*📊 Vulnerability Summary*\n\n"
                    f"• Total Vulnerabilities: *{total_vulnerabilities}*\n"
                    f"• Critical Vulnerabilities: *{critical_count}*\n"
                    f"• High Vulnerabilities: *{high_count}*\n"
                    f"• Security Score: *{security_score}%*"
                )
            }
        },

        # Divider
        {
            "type": "divider"
        },

        # AI Recommendation
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    "*🤖 AI Remediation Recommendation*\n\n"
                    "Amazon Nova detected vulnerable dependencies "
                    "inside the container image.\n\n"
                    "*Recommended Actions:*\n"
                    "• Upgrade vulnerable packages\n"
                    "• Rebuild secure Docker image\n"
                    "• Trigger CI/CD security validation\n"
                    "• Apply dependency patch updates"
                )
            }
        },

        # Divider
        {
            "type": "divider"
        },

        # Approval Section
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    "*🛠 Human Approval Required*\n\n"
                    "Approve automated remediation workflow?"
                )
            }
        },

        # Action Buttons
        {
            "type": "actions",
            "elements": [

                # Approve Button
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "✅ Approve"
                    },
                    "style": "primary",
                    "value": "approve_fix",
                    "action_id": "approve_button"
                },

                # Reject Button
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "❌ Reject"
                    },
                    "style": "danger",
                    "value": "reject_fix",
                    "action_id": "reject_button"
                }
            ]
        },

        # Divider
        {
            "type": "divider"
        },

        # Footer
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": (
                        "🚀 AI DevSecOps Platform | "
                        "Trivy • Amazon Nova • GitHub Actions • Slack ChatOps"
                    )
                }
            ]
        }
    ]
}

# ---------------------------------------------------
# SEND MESSAGE
# ---------------------------------------------------

response = requests.post(
    WEBHOOK_URL,
    data=json.dumps(message),
    headers={"Content-Type": "application/json"}
)

# ---------------------------------------------------
# DEBUG LOGS
# ---------------------------------------------------

print("\n=== SLACK ALERT STATUS ===")

print("Status Code:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    print("✅ Slack alert delivered successfully.")

else:
    print("❌ Failed to send Slack alert.")