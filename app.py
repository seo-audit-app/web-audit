import streamlit as st
import pandas as pd
from crawler import crawl_website

st.set_page_config(page_title="SEO Audit Tool", layout="wide")

st.title("🔍 SEO Audit Tool (Web Version)")
st.markdown("Check your site's SEO status. Enter a URL and click 'Run Audit'.")

url = st.text_input("Website URL", placeholder="https://example.com")

if st.button("Run Audit"):
    if url:
        with st.spinner("Crawling the website..."):
            try:
                results = crawl_website(url)
                if results:
                    # Updated column names to include Title Length
                    df = pd.DataFrame(results, columns=["URL", "Status Code", "Title", "Title Length"])
                    st.success("Audit complete! ✅")
                    st.dataframe(df, use_container_width=True)

                    # Export CSV button
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name="seo_audit.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No data found. The site may be blocking crawlers or unreachable.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL.")
