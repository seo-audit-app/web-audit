import streamlit as st
import pandas as pd

# ✅ MAIN CHECK TO FILTER MAPPING
MAIN_CHECKS = {
    "Breadcrumbs": ["Missing", "Multiple Breadcrumbs", "Non-structured format"],
    "Broken Links (404, 5xx)": ["404 Errors", "5xx Errors", "Timeout", "Redirect Chains"],
    "Canonical Tag": ["Missing", "Multiple", "Conflicting Canonical", "Self-referencing"],
    "Crawlability (robots.txt)": ["Blocked by robots.txt", "Allowed", "Missing robots.txt"],
    "External Links": ["Broken External", "Too Many", "Non-secure (http)", "No Anchor Text"],
    "Favicon Check": ["Missing Favicon", "Invalid Format", "Not in Root"],
    "H1 Tag": ["Missing H1", "Multiple H1"],
    "H2 Tag": ["Missing H2", "Improper Order"],
    "HTTP Status Code": ["2xx OK", "3xx Redirect", "4xx Error", "5xx Server Error"],
    "HTTPS / SSL": ["No HTTPS", "Mixed Content", "Expired Certificate"],
    "Images": ["Missing Alt Text", "Broken Image", "Large Size", "Lazy-load Not Used"],
    "Indexability": ["Noindex Meta", "X-Robots Noindex", "Blocked URLs"],
    "Internal Linking": ["Orphan Pages", "Too Few Links", "Broken Internal Links"],
    "Language Tag": ["Missing <html lang>", "Invalid Lang Code", "Mismatched Language"],
    "Meta Description": ["Missing", "Duplicate", "Short", "Long", "Multiple"],
    "Meta Robots Tag": ["Missing", "Noindex", "Nofollow", "Conflicting Directives"],
    "Page Size": ["Over 500KB", "Over 1MB", "Heavy Images", "Excessive Scripts"],
    "Schema Markup": ["Missing", "Invalid JSON-LD", "Unrecognized Type"],
    "Title Tag": ["Missing", "Duplicate", "Short", "Long", "Multiple"],
    "URL Structure": ["Long URLs", "Contains UTM", "Dynamic Params", "Mixed Case", "Underscores"],
    "XML Sitemap Presence": ["Not Found", "Invalid Format", "Not Declared in robots.txt"]
}

# Sample summary table
summary_table = pd.DataFrame([{
    "Total Pages": 35,
    "Internal Pages": 28,
    "External Pages": 7,
    "XML Sitemap": "Found",
    "Robots.txt": "Found",
    "GA Code": "Yes",
    "Noindex URLs": 3
}])

# Mock master data for testing filters
df_mock = pd.DataFrame({
    "URL": ["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"],
    "Issue Detail": ["Missing", "Duplicate", "Short"],
    "Length": [12, 8, 15],
    "Status": ["Missing", "Duplicate", "Short"]
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
        .stSelectbox { margin-bottom: 0.25rem !important; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center;'>🔍 SEO Audit Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color: gray;'>Fast & Lightweight SEO Analyzer</p>", unsafe_allow_html=True)
st.markdown("---")

# ✅ Summary Table
st.markdown("### 🧾 Website Summary")
st.dataframe(summary_table.style.set_properties(**{
    'text-align': 'center',
    'vertical-align': 'middle'
}).set_table_styles([{
    'selector': 'td',
    'props': [('text-align', 'center'), ('vertical-align', 'middle')]
}, {
    'selector': 'th',
    'props': [('text-align', 'center'), ('font-weight', 'bold')]
}]), use_container_width=True)

st.markdown("---")

# ✅ Layout with adjusted column ratios
left, middle, right = st.columns([2, 4, 2])

with left:
    st.markdown('<div class="main-check-box">', unsafe_allow_html=True)
    st.subheader("Main Checks")
    selected_main = st.radio("", list(MAIN_CHECKS.keys()), label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

with middle:
    st.subheader("Sub-Issue Breakdown")

    filter_options = ["All"] + MAIN_CHECKS.get(selected_main, [])
    selected_filter = st.selectbox("Filter by Issue Type", filter_options)

    df_display = df_mock.copy()
    df_display["Issue Type"] = df_display["Status"]
    df_display.rename(columns={"Issue Detail": f"{selected_main} Detail"}, inplace=True)

    if selected_filter != "All":
        df_display = df_display[df_display["Issue Type"] == selected_filter]

    st.dataframe(df_display[["URL", f"{selected_main} Detail", "Length", "Issue Type"]], use_container_width=True, height=300)

with right:
    st.subheader("Issue Summary")
    df_issues = pd.DataFrame(issue_summary, columns=["Issue", "URL Count"])
    st.dataframe(df_issues, use_container_width=True)

    csv = df_mock.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Full Report", csv, "seo_mock_audit.csv", "text/csv", use_container_width=True)
