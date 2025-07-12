import streamlit as st
import pandas as pd
from crawler import crawl_website

st.set_page_config(page_title="SEO Audit Tool", layout="wide")

# Hide Streamlit's default menu and GitHub icon
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .css-164nlkn.egzxvld1 {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h1 style='font-size: 2.5rem;'>🔍 SEO Audit Tool</h1>
        <p style='font-size: 1.2rem; color: gray;'>Check your site's SEO status — fast and free</p>
    </div>
""", unsafe_allow_html=True)

url = st.text_input("🌐 Enter Website URL", placeholder="https://example.com")

if st.button("🚀 Run Audit", use_container_width=True):
    if url:
        with st.spinner("🔎 Crawling the website..."):
            try:
                page_data, summary = crawl_website(url)

                if page_data:
                    # ✅ Safe column assignment on DataFrame creation
                    df = pd.DataFrame(page_data, columns=[
                        "URL", "Status Code", "Title", "Title Length",
                        "Meta Description", "Description Length", "Noindex"
                    ])

                    st.success(f"✅ Audit complete! {len(df)} pages crawled.")

                    # Phase 2: Website Summary
                    st.markdown("## 🧾 Website Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total Pages", summary['total_pages'])
                    col2.metric("Internal Links", summary['internal_links'])
                    col3.metric("External Links", summary['external_links'])
                    col4.metric("Noindex URLs", summary['noindex_count'])
                    col1b, col2b, col3b = st.columns(3)
                    col1b.metric("Sitemap Found", summary['sitemap_found'])
                    col2b.metric("Robots.txt Found", summary['robots_found'])
                    col3b.metric("GA Code Found", summary['ga_found'])

                    # Phase 3: 3-Column Layout
                    st.markdown("---")
                    left, middle, right = st.columns([1, 4, 1])

                    with left:
                        st.subheader("Main Checks")
                        check_option = st.radio("Select Category", ["Meta Title", "Meta Description"])

                    with middle:
                        st.subheader("Details")
                        if check_option == "Meta Title":
                            st.markdown("#### Meta Title Issues")
                            st.markdown("- Missing")
                            st.dataframe(df[df['Title'].isnull() | (df['Title'] == "")])
                            st.markdown("- Duplicate")
                            dup_titles = df[df.duplicated('Title', keep=False)]
                            st.dataframe(dup_titles)
                            st.markdown("- Too Short (<30)")
                            st.dataframe(df[df['Title Length'] < 30])
                            st.markdown("- Too Long (>60)")
                            st.dataframe(df[df['Title Length'] > 60])

                        elif check_option == "Meta Description":
                            st.markdown("#### Meta Description Issues")
                            st.markdown("- Missing")
                            st.dataframe(df[df['Meta Description'].isnull() | (df['Meta Description'] == "")])
                            st.markdown("- Duplicate")
                            dup_desc = df[df.duplicated('Meta Description', keep=False)]
                            st.dataframe(dup_desc)
                            st.markdown("- Too Short (<60)")
                            st.dataframe(df[df['Description Length'] < 60])
                            st.markdown("- Too Long (>160)")
                            st.dataframe(df[df['Description Length'] > 160])

                    with right:
                        st.subheader("Issue Summary")
                        issues = [
                            ("Missing Titles", len(df[df['Title'].isnull() | (df['Title'] == "")])),
                            ("Duplicate Titles", len(df[df.duplicated('Title', keep=False)])),
                            ("Short Titles", len(df[df['Title Length'] < 30])),
                            ("Long Titles", len(df[df['Title Length'] > 60])),
                            ("Missing Descriptions", len(df[df['Meta Description'].isnull() | (df['Meta Description'] == "")])),
                            ("Duplicate Descriptions", len(df[df.duplicated('Meta Description', keep=False)])),
                            ("Short Descriptions", len(df[df['Description Length'] < 60])),
                            ("Long Descriptions", len(df[df['Description Length'] > 160]))
                        ]
                        for i, (label, count) in enumerate(issues, 1):
                            st.write(f"{i}. {label}: {count}")

                        st.download_button("📥 Download Full Report", df.to_csv(index=False).encode("utf-8"), "seo_audit.csv", "text/csv")

                else:
                    st.warning("⚠️ No data found. The site may be blocking crawlers or is unreachable.")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("⚠️ Please enter a valid URL.")
