import streamlit as st
import pandas as pd

# Mock Data (this will be replaced by crawler data later)
data = [
    {"URL": "https://example.com", "Title": "Example Title", "Title Length": 20, "Meta Description": "This is a test.", "Description Length": 15},
    {"URL": "https://example.com/about", "Title": "", "Title Length": 0, "Meta Description": "About us page description.", "Description Length": 26},
    {"URL": "https://example.com/contact", "Title": "Contact | Example", "Title Length": 18, "Meta Description": "Contact page.", "Description Length": 14},
    {"URL": "https://example.com/long-title", "Title": "This is a very long title exceeding normal length", "Title Length": 52, "Meta Description": "Long meta description example that exceeds the usual limit.", "Description Length": 65},
]

summary = {
    "total_pages": 50,
    "internal_pages": 42,
    "external_pages": 8,
    "noindex_count": 3,
    "sitemap_found": True,
    "robots_found": True,
    "ga_found": False
}

# Start Streamlit
st.set_page_config(page_title="SEO Audit Tool", layout="wide")

st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h1 style='font-size: 2.5rem;'>🔍 SEO Audit Tool</h1>
        <p style='font-size: 1.2rem; color: gray;'>Check your site's SEO status — fast and free</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("## 🧾 Website Summary")
summary_table = pd.DataFrame({
    "Metric": ["Total Pages", "Internal Pages", "External Pages", "Noindex URLs", "Sitemap Found", "Robots.txt Found", "GA Code Found"],
    "Value": [
        summary['total_pages'],
        summary['internal_pages'],
        summary['external_pages'],
        summary['noindex_count'],
        "Yes" if summary['sitemap_found'] else "No",
        "Yes" if summary['robots_found'] else "No",
        "Yes" if summary['ga_found'] else "No"
    ]
})

st.dataframe(summary_table.style.set_properties(**{
    'border': '1px solid black',
    'text-align': 'center',
    'font-weight': 'bold'
}).set_table_styles([{
    'selector': 'th',
    'props': [('text-align', 'center'), ('border', '1px solid black'), ('font-weight', 'bold')]
}]), use_container_width=True)

# Layout
st.markdown("---")
left, middle, right = st.columns([1.2, 3.8, 1.5])

with left:
    st.subheader("Main Checks")
    main_check = st.radio("Select Section", ["Meta Title", "Meta Description"])

with middle:
    st.subheader("Sub-Issue Breakdown")
    filter_option = st.selectbox("Filter By", ["All", "Missing", "Duplicate", "Short", "Long"])

    df = pd.DataFrame(data)
    filtered_df = df.copy()

    if main_check == "Meta Title":
        if filter_option == "Missing":
            filtered_df = df[df['Title'] == ""]
        elif filter_option == "Duplicate":
            filtered_df = df[df.duplicated('Title', keep=False) & (df['Title'] != "")]
        elif filter_option == "Short":
            filtered_df = df[df['Title Length'] < 30]
        elif filter_option == "Long":
            filtered_df = df[df['Title Length'] > 60]
        table = filtered_df[['URL', 'Title', 'Title Length']].reset_index(drop=True)
    else:
        if filter_option == "Missing":
            filtered_df = df[df['Meta Description'] == ""]
        elif filter_option == "Duplicate":
            filtered_df = df[df.duplicated('Meta Description', keep=False) & (df['Meta Description'] != "")]
        elif filter_option == "Short":
            filtered_df = df[df['Description Length'] < 60]
        elif filter_option == "Long":
            filtered_df = df[df['Description Length'] > 160]
        table = filtered_df[['URL', 'Meta Description', 'Description Length']].reset_index(drop=True)

    table.index += 1
    table.reset_index(inplace=True)
    table.columns = ["Sr. No."] + list(table.columns[1:])

    st.dataframe(table.style.set_properties(**{
        'border': '1px solid black',
        'text-align': 'center'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('text-align', 'center'), ('border', '1px solid black'), ('font-weight', 'bold')]
    }]), use_container_width=True)

with right:
    st.subheader("Issue Summary")
    issues = []

    if main_check == "Meta Title":
        issues = [
            ("Missing Titles", len(df[df['Title'] == ""])),
            ("Duplicate Titles", len(df[df.duplicated('Title', keep=False) & (df['Title'] != "")])),
            ("Short Titles (<30)", len(df[df['Title Length'] < 30])),
            ("Long Titles (>60)", len(df[df['Title Length'] > 60]))
        ]
    else:
        issues = [
            ("Missing Descriptions", len(df[df['Meta Description'] == ""])),
            ("Duplicate Descriptions", len(df[df.duplicated('Meta Description', keep=False) & (df['Meta Description'] != "")])),
            ("Short Descriptions (<60)", len(df[df['Description Length'] < 60])),
            ("Long Descriptions (>160)", len(df[df['Description Length'] > 160]))
        ]

    issue_df = pd.DataFrame(issues, columns=["Issue Type", "URL Count"])
    issue_df.index += 1
    issue_df.reset_index(inplace=True)
    issue_df.columns = ["Sr. No.", "Issue Type", "URL Count"]

    st.dataframe(issue_df.style.set_properties(**{
        'border': '1px solid black',
        'text-align': 'center'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('text-align', 'center'), ('border', '1px solid black'), ('font-weight', 'bold')]
    }]), use_container_width=True)

    st.download_button("📥 Download Full Report", df.to_csv(index=False).encode("utf-8"), "seo_audit.csv", "text/csv")
