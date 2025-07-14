import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tldextract
import pandas as pd
import re

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; SEO-Audit-Bot/1.0)'}
visited_urls = set()

MAIN_CHECKS = {
    "Title Tag": ["Missing", "Duplicate", "Short", "Long", "Multiple"],
    "Meta Description": ["Missing", "Duplicate", "Short", "Long", "Multiple"],
    "H1 Tag": ["Missing H1", "Multiple H1"],
    "Indexability": ["Noindex Meta", "X-Robots Noindex", "Blocked URLs"],
    "Canonical Tag": ["Missing", "Multiple", "Conflicting Canonical", "Self-referencing"],
    # Add more if needed for Phase 1
}

def is_internal(base, target):
    return tldextract.extract(base).registered_domain == tldextract.extract(target).registered_domain

def clean_url(href, base):
    parsed = urlparse(urljoin(base, href))
    return parsed.scheme + "://" + parsed.netloc + parsed.path

def extract_page_issues(url, html, all_titles, all_descriptions):
    soup = BeautifulSoup(html, "lxml")
    issues = []

    title_tags = soup.find_all('title')
    meta_desc_tags = soup.find_all('meta', attrs={"name": "description"})
    h1_tags = soup.find_all('h1')
    canonical = soup.find('link', rel='canonical')
    robots = soup.find('meta', attrs={"name": "robots"})
    meta_robots = robots.get("content", "").lower() if robots else ""

    title = title_tags[0].text.strip() if title_tags else ""
    meta_desc = meta_desc_tags[0]["content"].strip() if meta_desc_tags and meta_desc_tags[0].get("content") else ""

    # TITLE TAG
    if not title:
        issues.append(("Title Tag", "Missing", 0))
    elif len(title) < 20:
        issues.append(("Title Tag", "Short", len(title)))
    elif len(title) > 60:
        issues.append(("Title Tag", "Long", len(title)))
    if all_titles.count(title) > 1:
        issues.append(("Title Tag", "Duplicate", len(title)))
    if len(title_tags) > 1:
        issues.append(("Title Tag", "Multiple", len(title)))

    # META DESCRIPTION
    if not meta_desc:
        issues.append(("Meta Description", "Missing", 0))
    elif len(meta_desc) < 50:
        issues.append(("Meta Description", "Short", len(meta_desc)))
    elif len(meta_desc) > 160:
        issues.append(("Meta Description", "Long", len(meta_desc)))
    if all_descriptions.count(meta_desc) > 1 and meta_desc:
        issues.append(("Meta Description", "Duplicate", len(meta_desc)))
    if len(meta_desc_tags) > 1:
        issues.append(("Meta Description", "Multiple", len(meta_desc)))

    # H1 Tag
    if not h1_tags:
        issues.append(("H1 Tag", "Missing H1", 0))
    elif len(h1_tags) > 1:
        issues.append(("H1 Tag", "Multiple H1", len(h1_tags)))

    # Indexability
    if "noindex" in meta_robots:
        issues.append(("Indexability", "Noindex Meta", 0))

    # Canonical Tag
    if not canonical:
        issues.append(("Canonical Tag", "Missing", 0))
    elif isinstance(canonical, list) and len(canonical) > 1:
        issues.append(("Canonical Tag", "Multiple", len(canonical)))

    return issues

def crawl_site(base_url, max_pages=50):
    queue = [base_url]
    all_data = []
    titles = []
    descriptions = []

    total_internal = 0
    total_external = 0
    noindex_count = 0
    has_ga = False

    while queue and len(visited_urls) < max_pages:
        url = queue.pop(0)
        if url in visited_urls:
            continue

        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            content_type = resp.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                continue

            visited_urls.add(url)
            soup = BeautifulSoup(resp.text, "lxml")

            title_tag = soup.title.string.strip() if soup.title else ""
            meta_desc_tag = soup.find('meta', attrs={"name": "description"})
            meta_desc = meta_desc_tag.get("content", "").strip() if meta_desc_tag else ""

            titles.append(title_tag)
            descriptions.append(meta_desc)

            links = [clean_url(a['href'], url) for a in soup.find_all('a', href=True)]
            for link in links:
                if is_internal(base_url, link):
                    total_internal += 1
                    if link not in visited_urls and link not in queue:
                        queue.append(link)
                else:
                    total_external += 1

            if "noindex" in resp.text.lower():
                noindex_count += 1
            if re.search(r'UA-\d{4,10}-\d{1,4}|GTM-[\w\d]+', resp.text):
                has_ga = True

            issues = extract_page_issues(url, resp.text, titles, descriptions)
            for main, status, length in issues:
                all_data.append({
                    "URL": url,
                    "Main Check": main,
                    "Issue Detail": status,
                    "Length": length,
                    "Status": status
                })

        except Exception as e:
            print(f"[Error] Failed: {url} | {e}")
            continue

    robots_url = urljoin(base_url, "/robots.txt")
    sitemap_url = ""
    try:
        robots_resp = requests.get(robots_url, headers=HEADERS, timeout=5)
        match = re.search(r"Sitemap:\s*(\S+)", robots_resp.text)
        if match:
            sitemap_url = match.group(1)
    except:
        pass

    summary = pd.DataFrame([{
        "Total Pages": len(visited_urls),
        "Internal Pages": total_internal,
        "External Pages": total_external,
        "XML Sitemap": "Found" if sitemap_url else "Not Found",
        "Robots.txt": "Found" if robots_resp.status_code == 200 else "Not Found",
        "GA Code": "Yes" if has_ga else "No",
        "Noindex URLs": noindex_count
    }])

    issue_df = pd.DataFrame(all_data)
    issue_summary = issue_df.groupby(["Main Check", "Issue Detail"]).size().reset_index(name="URL Count")
    issue_summary["Issue"] = issue_summary["Issue Detail"] + " " + issue_summary["Main Check"]
    return summary, issue_df, issue_summary[["Issue", "URL Count"]]

# Example run
if __name__ == "__main__":
    base = "https://example.com"
    summary, issues, issue_summary = crawl_site(base, max_pages=30)
    summary.to_csv("summary.csv", index=False)
    issues.to_csv("issue_table.csv", index=False)
    issue_summary.to_csv("issue_summary.csv", index=False)
