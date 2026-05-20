from fastapi import FastAPI, Request
import subprocess

app = FastAPI()

@app.post("/slack/actions")
async def slack_actions(request: Request):

    form_data = await request.form()

    payload = form_data.get("payload")

    print("\nSlack Payload Received:\n")
    print(payload)

    # Run remediation automatically
    subprocess.run(["python", "../scripts/remediation.py"])

    return {
        "text": "✅ AI remediation triggered successfully."
    }