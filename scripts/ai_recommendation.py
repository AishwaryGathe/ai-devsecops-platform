import json
import boto3

# Create Bedrock Runtime Client
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# Load Trivy report
with open("../reports/report.json") as f:
    data = json.load(f)

# Extract vulnerabilities
vulnerabilities = []

for result in data.get("Results", []):
    for vuln in result.get("Vulnerabilities", []):
        vulnerabilities.append({
            "cve": vuln.get("VulnerabilityID"),
            "package": vuln.get("PkgName"),
            "severity": vuln.get("Severity"),
            "installed": vuln.get("InstalledVersion"),
            "fixed": vuln.get("FixedVersion")
        })

# Take first vulnerability
v = vulnerabilities[0]

prompt = f"""
You are a DevSecOps security expert.

Analyze this container vulnerability and suggest remediation.

CVE: {v['cve']}
Package: {v['package']}
Severity: {v['severity']}
Installed Version: {v['installed']}
Fixed Version: {v['fixed']}

Provide:
1. Risk summary
2. Recommended fix
3. Dockerfile improvement
4. Best security practice
"""

# Invoke Amazon Nova Lite
response = client.invoke_model(
    modelId="amazon.nova-lite-v1:0",
    body=json.dumps({
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 500,
            "temperature": 0.3
        }
    })
)

# Parse response
response_body = json.loads(response["body"].read())

# Print AI output
print(response_body["output"]["message"]["content"][0]["text"])