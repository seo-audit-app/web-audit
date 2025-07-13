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

# Mock SEO data
df_mock = pd.DataFrame({
    "URL": ["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"],
    "Meta Title": ["Home", "Contact", ""],
    "Length": [4, 7, 0],
    "Status": ["Short", "All Good", "Missing"]
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
        .block-container {
            padding-top: 1rem;
            padding-left: 2%;
            padding-right: 2%;
        }
        table, th, td {
            border: 2px solid black !important;
            border-collapse: collapse !important;
            text-align: center !important;
            vertical-align: middle !important;
        }
        thead {
            background-color: #f0f0f0;
            font-weight: bold;
        }
        .main-check-box {
            border: 2px solid black;
            border-radius: 8px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center;'>🔍 SEO Audit Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color: gray;'>Fast & Lightweight SEO Analyzer</p>", unsafe_allow_html=True)
st.markdown("---")

# ✅ Summary Table with full center alignment
st.markdown("### 🧾 Website Summary")
styled_summary = summary_table.style.set_properties(**{
    'text-align': 'center',
    'vertical-align': 'middle'
}).set_table_styles([{
    'selector': 'th',
    'props': [('text-align', 'center'), ('font-weight', 'bold')]
}])
st.dataframe(styled_summary, use_container_width=True)

st.markdown("---")

# ✅ Layout: 96% width via CSS block-container, visible bordered menu
left, middle, right = st.columns([1, 5, 2])

with left:
    st.markdown('<div class="main-check-box">', unsafe_allow_html=True)
    st.subheader("Main Checks")
    selected_main = st.radio("", ["Meta Title", "Meta Description"], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

with middle:
    st.subheader("Sub-Issue Breakdown")
    selected_filter = st.selectbox("Filter by Issue Type", ["All", "Missing", "Duplicate", "Short", "Long", "Multiple"])

    if selected_main == "Meta Title":
        df_display = df_mock[["URL", "Meta Title", "Length", "Status"]].copy()
        df_display.rename(columns={"Meta Title": "Meta Title/Description"}, inplace=True)

    elif selected_main == "Meta Description":
        df_display = df_mock[["URL", "Meta Title", "Length", "Status"]].copy()
        df_display.rename(columns={"Meta Title": "Meta Title/Description"}, inplace=True)
        df_display["Meta Title/Description"] = ["Welcome to site", "", "About Us"]
        df_display["Status"] = ["Duplicate", "Missing", "Short"]

    if selected_filter != "All":
        df_display = df_display[df_display["Status"] == selected_filter]

    st.dataframe(df_display[["URL", "Meta Title/Description", "Length", "Status"]], use_container_width=True)

with right:
    st.subheader("Issue Summary")
    df_issues = pd.DataFrame(issue_summary, columns=["Issue", "URL Count"])
    st.dataframe(df_issues, use_container_width=True)

    csv = df_mock.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Full Report", csv, "seo_mock_audit.csv", "text/csv", use_container_width=True)
