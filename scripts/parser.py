import json

with open("../reports/report.json") as f:
    data = json.load(f)

for result in data.get("Results", []):
    vulnerabilities = result.get("Vulnerabilities", [])

    for vuln in vulnerabilities:
        print("=" * 50)
        print("CVE:", vuln.get("VulnerabilityID"))
        print("Package:", vuln.get("PkgName"))
        print("Severity:", vuln.get("Severity"))
        print("Installed:", vuln.get("InstalledVersion"))
        print("Fixed:", vuln.get("FixedVersion"))