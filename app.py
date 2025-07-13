import streamlit as st
import pandas as pd

# Sample mock data
summary_table = pd.DataFrame([{
    "Total Pages": 35,
    "Internal Pages": 28,
    "External Pages": 7,
    "XML Sitemap": "Found",
    "Robots.txt": "Found",
    "GA Code": "Yes",
    "Noindex URLs": 3
}])

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

# Streamlit config
st.set_page_config(page_title="SEO Audit Tool", layout="wide")

# Custom styling
st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        .css-164nlkn.egzxvld1 {display: none;}
        table, th, td {
            border: 2px solid black !important;
            border-collapse: collapse !important;
            text-align: center !important;
        }
        thead {
            background-color: #f0f0f0;
            font-weight: bold;
        }
        .block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center;'>🔍 SEO Audit Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color: gray;'>Fast & Lightweight SEO Analyzer</p>", unsafe_allow_html=True)
st.markdown("---")

# ✅ Summary Table
st.markdown("### 🧾 Website Summary")
st.dataframe(summary_table.style.set_properties(**{
    'text-align': 'center'
}).set_table_styles([{
    'selector': 'th',
    'props': [('text-align', 'center'), ('font-weight', 'bold')]
}]), use_container_width=True)

st.markdown("---")

# ✅ Layout
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
