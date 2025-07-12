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
    .css-164nlkn.egzxvld1 {display: none;} /* GitHub icon */
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Header section with icon and custom style
st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h1 style='font-size: 2.5rem;'>🔍 SEO Audit Tool</h1>
        <p style='font-size: 1.2rem; color: gray;'>Check your site's SEO status — fast and free</p>
    </div>
""", unsafe_allow_html=True)

# Input form
st.markdown("---")
url = st.text_input("🌐 Enter Website URL", placeholder="https://example.com")
st.markdown("---")

if st.button("🚀 Run Audit", use_container_width=True):
    if url:
        with st.spinner("🔎 Crawling the website..."):
            try:
                results = crawl_website(url)
                if results:
                    # Add title length to each row if not already added
                    clean_results = []
                    for row in results:
                        if len(row) == 3:
                            row = list(row)
                            row.append(len(row[2]))  # title length
                        clean_results.append(row)

                    df = pd.DataFrame(clean_results, columns=["URL", "Status Code", "Title", "Title Length"])
                    st.success(f"✅ Audit complete! {len(df)} pages crawled.")

                    # Display results
                    st.dataframe(df, use_container_width=True)

                    with st.expander("📥 Download Results"):
                        csv = df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            label="Download as CSV",
                            data=csv,
                            file_name="seo_audit.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                else:
                    st.warning("⚠️ No data found. The site may be blocking crawlers or is unreachable.")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("⚠️ Please enter a valid URL.")
