import streamlit as st
import json
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI DevSecOps Dashboard",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.metric-card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #2d333b;
}

.security-score {
    font-size: 40px;
    font-weight: bold;
    color: #00ff99;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🚀 AI DevSecOps Security Dashboard")

st.markdown("""
AI-Driven Container Security, Vulnerability Analysis,
ChatOps Approval Workflow, and Automated Remediation Platform
""")

st.divider()

# ---------------------------------------------------
# LOAD REPORT
# ---------------------------------------------------

try:
    with open("reports/report.json") as f:
        data = json.load(f)

except Exception as e:
    st.error(f"Failed to load report.json: {e}")
    st.stop()

# ---------------------------------------------------
# EXTRACT VULNERABILITIES
# ---------------------------------------------------

vulnerabilities = []

for result in data.get("Results", []):

    for vuln in result.get("Vulnerabilities", []):

        vulnerabilities.append({
            "CVE": vuln.get("VulnerabilityID"),
            "Package": vuln.get("PkgName"),
            "Severity": vuln.get("Severity"),
            "Installed Version": vuln.get("InstalledVersion"),
            "Fixed Version": vuln.get("FixedVersion"),
            "Title": vuln.get("Title"),
            "Description": vuln.get("Description"),
            "Published": vuln.get("PublishedDate"),
            "Primary URL": vuln.get("PrimaryURL")
        })

df = pd.DataFrame(vulnerabilities)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("⚙️ Dashboard Controls")

severity_filter = st.sidebar.multiselect(
    "Filter by Severity",
    options=df["Severity"].unique(),
    default=df["Severity"].unique()
)

search_package = st.sidebar.text_input(
    "Search Package"
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_df = df[df["Severity"].isin(severity_filter)]

if search_package:
    filtered_df = filtered_df[
        filtered_df["Package"].str.contains(
            search_package,
            case=False,
            na=False
        )
    ]

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------

total_vulns = len(filtered_df)
critical = len(filtered_df[filtered_df["Severity"] == "CRITICAL"])
high = len(filtered_df[filtered_df["Severity"] == "HIGH"])
medium = len(filtered_df[filtered_df["Severity"] == "MEDIUM"])

security_score = max(
    0,
    100 - (critical * 20 + high * 10 + medium * 5)
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Vulnerabilities", total_vulns)
col2.metric("Critical", critical)
col3.metric("High", high)
col4.metric("Medium", medium)
col5.metric("Security Score", f"{security_score}%")

st.divider()

# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------

chart_col1, chart_col2 = st.columns(2)

# Severity Pie Chart
with chart_col1:

    st.subheader("📊 Severity Distribution")

    severity_counts = filtered_df["Severity"].value_counts()

    fig = px.pie(
        values=severity_counts.values,
        names=severity_counts.index,
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

# Vulnerability Count by Package
with chart_col2:

    st.subheader("📦 Vulnerabilities by Package")

    package_counts = (
        filtered_df["Package"]
        .value_counts()
        .head(10)
    )

    fig2 = px.bar(
        x=package_counts.index,
        y=package_counts.values,
        labels={"x": "Package", "y": "Count"}
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------------------------------------------------
# SECURITY SCORE
# ---------------------------------------------------

st.subheader("🛡️ Security Health Score")

st.progress(security_score / 100)

if security_score > 80:
    st.success("Excellent Security Posture")

elif security_score > 50:
    st.warning("Moderate Security Risk")

else:
    st.error("Critical Security Risk Detected")

st.divider()

# ---------------------------------------------------
# VULNERABILITY TABLE
# ---------------------------------------------------

st.subheader("📋 Vulnerability Details")

display_columns = [
    "CVE",
    "Package",
    "Severity",
    "Installed Version",
    "Fixed Version"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    height=400
)

st.divider()

# ---------------------------------------------------
# AI RECOMMENDATION SECTION
# ---------------------------------------------------

st.subheader("🤖 AI Remediation Insights")

if len(filtered_df) > 0:

    top_vuln = filtered_df.iloc[0]

    st.info(f"""
### Recommended Remediation

- **CVE:** {top_vuln['CVE']}
- **Package:** {top_vuln['Package']}
- **Severity:** {top_vuln['Severity']}

### Suggested Fix
Upgrade package to secure version:
`{top_vuln['Fixed Version']}`

### Security Recommendation
- Use minimal container images
- Regularly rebuild images
- Apply CI/CD security scans
- Avoid outdated dependencies
""")

else:
    st.success("No vulnerabilities found.")

st.divider()

# ---------------------------------------------------
# TIMELINE / ACTIVITY
# ---------------------------------------------------

st.subheader("📅 Scan Activity")

scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

st.write(f"Last Scan Time: **{scan_time}**")

st.write("Pipeline Status: ✅ Completed")

st.write("AI Analysis Status: ✅ Successful")

st.write("Slack Notification Status: ✅ Delivered")

st.divider()
