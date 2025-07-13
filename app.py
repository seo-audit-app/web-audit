import streamlit as st
import pandas as pd

st.set_page_config(page_title="SEO Audit Tool", layout="wide")

# Hide Streamlit's default menu and GitHub icon
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .css-164nlkn.egzxvld1 {display: none;}
    .block-container {padding: 1rem 2rem;}
    .dataframe td, .dataframe th {
        border: 1px solid black;
        text-align: center;
        font-weight: bold;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h1 style='font-size: 2.5rem;'>🔍 SEO Audit Tool</h1>
        <p style='font-size: 1.2rem; color: gray;'>Check your site's SEO status — fast and free</p>
    </div>
""", unsafe_allow_html=True)

# Mock data placeholders
summary = {
    "total_pages": 12,
    "internal_pages": 10,
    "external_pages": 2,
    "sitemap_found": True,
    "robots_found": True,
    "ga_found": False,
    "noindex_count": 1
}

st.markdown("## 🧾 Website Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pages", summary['total_pages'])
col2.metric("Internal Pages", summary['internal_pages'])
col3.metric("External Pages", summary['external_pages'])
col4.metric("Noindex URLs", summary['noindex_count'])
col1b, col2b, col3b = st.columns(3)
col1b.metric("Sitemap Found", "✅" if summary['sitemap_found'] else "❌")
col2b.metric("Robots.txt Found", "✅" if summary['robots_found'] else "❌")
col3b.metric("GA Code Found", "✅" if summary['ga_found'] else "❌")

st.markdown("---")

# Left, Middle, Right Layout
left, middle, right = st.columns([1.5, 5, 2])

with left:
    st.subheader("Main Checks")
    check_option = st.radio("Select Category", ["Meta Title", "Meta Description"], index=0)

with middle:
    st.subheader("Sub-Issue Breakdown")

    sub_filter = st.selectbox("Select Sub-Issue", ["All", "Missing", "Duplicate", "Too Short", "Too Long"])

    meta_data = pd.DataFrame([
        {"Sr. No": 1, "URL": "https://example.com/page1", "Meta Title": "Home", "Length": 4},
        {"Sr. No": 2, "URL": "https://example.com/page2", "Meta Title": "", "Length": 0},
        {"Sr. No": 3, "URL": "https://example.com/page3", "Meta Title": "About Us", "Length": 9},
        {"Sr. No": 4, "URL": "https://example.com/page4", "Meta Title": "Very very long title that exceeds recommended length", "Length": 55}
    ])

    if sub_filter == "Missing":
        meta_data = meta_data[meta_data['Meta Title'] == ""]
    elif sub_filter == "Duplicate":
        meta_data = meta_data[meta_data.duplicated('Meta Title', keep=False)]
    elif sub_filter == "Too Short":
        meta_data = meta_data[meta_data['Length'] < 30]
    elif sub_filter == "Too Long":
        meta_data = meta_data[meta_data['Length'] > 60]

    st.dataframe(meta_data, use_container_width=True)

with right:
    st.subheader("Issue Summary")

    summary_data = pd.DataFrame([
        {"Sr.": 1, "Issue Type": "Missing Titles", "URL Count": 1},
        {"Sr.": 2, "Issue Type": "Duplicate Titles", "URL Count": 0},
        {"Sr.": 3, "Issue Type": "Short Titles", "URL Count": 2},
        {"Sr.": 4, "Issue Type": "Long Titles", "URL Count": 1},
    ])

    st.dataframe(summary_data, use_container_width=True)

    st.download_button("📥 Download Full Report", meta_data.to_csv(index=False).encode("utf-8"), "seo_audit.csv", "text/csv")
