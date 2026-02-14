import streamlit as st
import difflib
import pandas as pd

st.set_page_config(page_title="ReguGuard AI", layout="wide")

# -----------------------------
# Sample Demo Data (So it runs instantly)
# -----------------------------
DEFAULT_SOP = """
All customer data must be encrypted.
Financial records should be reviewed annually.
Employees must complete safety training.
"""

DEFAULT_REGULATION = """
All customer data must be encrypted using approved standards.
Financial records must be audited every year.
Employee safety training is mandatory and must be documented.
Data breach incidents must be reported within 72 hours.
"""

# -----------------------------
# Compliance Comparison Logic
# -----------------------------
def compare_documents(company_text, regulation_text):
    company_lines = company_text.splitlines()
    regulation_lines = regulation_text.splitlines()

    results = []

    for rule in regulation_lines:
        if rule.strip() == "":
            continue

        similarity_scores = [
            difflib.SequenceMatcher(None, rule, comp).ratio()
            for comp in company_lines
        ]

        max_similarity = max(similarity_scores) if similarity_scores else 0

        if max_similarity > 0.75:
            status = "✅ Compliant"
        elif max_similarity > 0.40:
            status = "⚠️ Partial"
        else:
            status = "❌ Non-Compliant"

        results.append({
            "Regulation Clause": rule,
            "Match Score": round(max_similarity, 2),
            "Status": status
        })

    return pd.DataFrame(results)

# -----------------------------
# UI
# -----------------------------
st.title("🛡️ ReguGuard AI")
st.subheader("Autonomous Compliance Loop (Demo Preview)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Company SOP")
    company_text = st.text_area(
        "Paste or edit your SOP",
        value=DEFAULT_SOP,
        height=250
    )

with col2:
    st.markdown("### Regulatory Document")
    regulation_text = st.text_area(
        "Paste or edit regulation",
        value=DEFAULT_REGULATION,
        height=250
    )

if st.button("🔍 Run Compliance Check"):
    results_df = compare_documents(company_text, regulation_text)

    st.markdown("## 📊 Compliance Results")
    st.dataframe(results_df, use_container_width=True)

    non_compliant = results_df[
        results_df["Status"] == "❌ Non-Compliant"
    ].shape[0]

    partial = results_df[
        results_df["Status"] == "⚠️ Partial"
    ].shape[0]

    st.markdown("### 📈 Summary")
    st.success(f"Compliant Clauses: {len(results_df) - non_compliant - partial}")
    st.warning(f"Partial Matches: {partial}")
    st.error(f"Non-Compliant Clauses: {non_compliant}")

    st.markdown("---")
    st.markdown("### 📝 Suggested Remediation")

    for _, row in results_df.iterrows():
        if "❌" in row["Status"]:
            st.markdown(f"**Clause:** {row['Regulation Clause']}")
            st.info(
                "Suggestion: Update SOP to explicitly include this requirement "
                "with assigned responsibility, measurable controls, and documentation process."
            )