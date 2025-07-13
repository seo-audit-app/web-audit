import streamlit as st
import pandas as pd

st.set_page_config(page_title="SEO Audit Tool", layout="wide")

# Hide Streamlit default items
st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .css-164nlkn.egzxvld1 {display: none;}
    table, th, td {
        border: 1px solid black !important;
        border-collapse: collapse;
        text-align: center;
    }
    th, td {
        padding: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <h1 style='font-size: 2.5rem;'>🔍 SEO Audit Tool</h1>
    <p style='font-size: 1.2rem; color: gray;'>Visualize your SEO site health before crawling</p>
</div>
""", unsafe_allow_html=True)

# URL Input (inactive for mockup)
st.text_input("🌐 Enter Website URL (Mock Mode)", value="https://example.com", disabled=True)

# Mock Summary Table
st.markdown("## 🧾 Website Summary")
sum_data = {
    "Metric": ["Total Pages", "Internal Links", "External Links", "Noindex URLs", "Sitemap Found", "Robots.txt Found", "GA Code Found"],
    "Value": [35, 120, 34, 4, "Yes", "Yes", "No"]
}
sum_df = pd.DataFrame(sum_data)
st.markdown("### Summary Table")
st.dataframe(sum_df, use_container_width=True, hide_index=True)

# 3-Column Layout
st.markdown("---")
left, middle, right = st.columns([1, 4, 1])

# Left Box (Main Checks)
with left:
    st.subheader("Main Checks")
    selected_main = st.radio("Select Category", [
        "Meta Title", "Meta Description", "H1 Tags", "Canonical Tag", "Broken Links"
    ])

# Middle Box (Detail by Sub-Issue)
with middle:
    st.subheader("Sub-Issue Breakdown")
    if selected_main == "Meta Title":
        st.markdown("**Missing Meta Titles**")
        st.dataframe(pd.DataFrame({"URL": ["/about", "/team"]}), use_container_width=True)
        st.markdown("**Duplicate Meta Titles**")
        st.dataframe(pd.DataFrame({"URL": ["/services", "/pricing"]}), use_container_width=True)
        st.markdown("**Too Short (<30)**")
        st.dataframe(pd.DataFrame({"URL": ["/contact"]}), use_container_width=True)
        st.markdown("**Too Long (>60)**")
        st.dataframe(pd.DataFrame({"URL": ["/features"]}), use_container_width=True)
    elif selected_main == "Meta Description":
        st.markdown("**Missing Descriptions**")
        st.dataframe(pd.DataFrame({"URL": ["/privacy", "/terms"]}), use_container_width=True)
        st.markdown("**Too Long (>160)**")
        st.dataframe(pd.DataFrame({"URL": ["/blog"]}), use_container_width=True)

# Right Box (Issue Summary)
with right:
    st.subheader("Issue Summary")
    issue_summary = pd.DataFrame({
        "Issue": ["Missing Titles", "Duplicate Titles", "Short Descriptions", "Long Descriptions"],
        "URL Count": [2, 2, 1, 1]
    })
    st.table(issue_summary)
    st.download_button(
        "📥 Download Mock Report",
        data=pd.DataFrame({"URL": ["/about", "/team"]}).to_csv(index=False).encode("utf-8"),
        file_name="seo_mock_report.csv",
        mime="text/csv"
    )
