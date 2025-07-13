import streamlit as st
import pandas as pd

# Mock data (to be replaced with real crawler output later)
summary_data = {
    "Total Pages": 35,
    "Internal Pages": 28,
    "External Pages": 7,
    "XML Sitemap": "Found",
    "Robots.txt": "Found",
    "GA Code": "Yes",
    "Noindex URLs": 3
}

df_mock = pd.DataFrame({
    "URL": ["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"],
    "Meta Title": ["Home", "Contact", ""],
    "Length": [4, 7, 0]
})

issue_summary = [
    ("Missing Titles", 1),
    ("Duplicate Titles", 0),
    ("Short Titles", 1),
    ("Long Titles", 0),
    ("Missing Descriptions", 1),
    ("Duplicate Descriptions", 0),
    ("Short Descriptions", 1),
    ("Long Descriptions", 0),
]

# Streamlit page setup
st.set_page_config(page_title="SEO Audit Tool", layout="wide")

st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        .css-164nlkn.egzxvld1 {display: none;}
        table td {
            text-align: center;
            border: 1px solid black !important;
        }
        table th {
            text-align: center;
            border: 2px solid black !important;
            background-color: #f2f2f2;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🔍 SEO Audit Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color: gray;'>Fast & Lightweight SEO Analyzer</p>", unsafe_allow_html=True)
st.markdown("---")

# Website Summary
st.markdown("### 🧾 Website Summary")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pages", summary_data["Total Pages"])
col2.metric("Internal Pages", summary_data["Internal Pages"])
col3.metric("External Pages", summary_data["External Pages"])
col4.metric("Noindex URLs", summary_data["Noindex URLs"])

col5, col6, col7 = st.columns(3)
col5.metric("XML Sitemap", summary_data["XML Sitemap"])
col6.metric("Robots.txt", summary_data["Robots.txt"])
col7.metric("GA Code", summary_data["GA Code"])

st.markdown("---")

# Main layout
left, middle, right = st.columns([1, 5, 2])

with left:
    st.subheader("Main Checks")
    selected_main = st.radio("", ["Meta Title", "Meta Description"], label_visibility="collapsed")

with middle:
    st.subheader("Sub-Issue Breakdown")

    if selected_main == "Meta Title":
        st.markdown("##### Showing: Meta Title")
        st.dataframe(df_mock[["URL", "Meta Title", "Length"]], use_container_width=True)

    elif selected_main == "Meta Description":
        st.markdown("##### Showing: Meta Description")
        df_desc = df_mock.copy()
        df_desc.rename(columns={"Meta Title": "Meta Description"}, inplace=True)
        st.dataframe(df_desc[["URL", "Meta Description", "Length"]], use_container_width=True)

with right:
    st.subheader("Issue Summary")
    df_issues = pd.DataFrame(issue_summary, columns=["Issue", "URL Count"])
    st.dataframe(df_issues, use_container_width=True)

    csv = df_mock.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Full Report", csv, "seo_mock_audit.csv", "text/csv", use_container_width=True)
