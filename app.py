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
                    # ✅ Only add title length if it's not already present
                    if len(results[0]) == 3:
                        results = [list(row) + [len(row[2])] for row in results]

                    df = pd.DataFrame(results, columns=["URL", "Status Code", "Title", "Title Length"])
                    st.success("Audit complete! ✅")
                    st.dataframe(df, use_container_width=True)

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
        