from fastapi import FastAPI, Request
import subprocess
import json

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI DevSecOps Backend Running"}

@app.post("/slack/actions")
async def slack_actions(request: Request):

    form_data = await request.form()

    payload = json.loads(form_data["payload"])

    action = payload["actions"][0]["value"]

    print("\nReceived Action:", action)

    if action == "approve_fix":

        print("\nRunning remediation...\n")

        subprocess.run(["python", "../scripts/remediation.py"])

        print("\nPushing changes...\n")

        subprocess.run(["git", "add", ".."])

        subprocess.run([
            "git",
            "commit",
            "-m",
            "AI remediation approved"
        ])

        subprocess.run(["git", "push"])

        return {
            "text": "✅ Remediation approved and pipeline triggered."
        }

    return {
        "text": "❌ Remediation rejected."
    }