# crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def is_internal(url, base):
    return urlparse(url).netloc == urlparse(base).netloc

def detect_ga_code(soup):
    return bool(soup.find("script", string=re.compile("google-analytics|gtag|ga\(")))

def detect_noindex(soup):
    meta = soup.find("meta", attrs={"name": "robots"})
    return meta and "noindex" in meta.get("content", "").lower()

def extract_metadata(soup):
    title_tag = soup.title
    title = title_tag.string.strip() if title_tag and title_tag.string else ""

    description = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag and desc_tag.get("content"):
        description = desc_tag["content"].strip()

    return title, description

def crawl_website(start_url, max_pages=50):
    visited = set()
    to_visit = [start_url]
    results = []

    internal_links = set()
    external_links = set()
    noindex_urls = []
    found_ga = False
    found_sitemap = False
    found_robots = False

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=10)
            visited.add(url)
            status = response.status_code
            content_type = response.headers.get("Content-Type", "")

            if "text/html" not in content_type:
                continue  # skip non-HTML

            soup = BeautifulSoup(response.text, "html.parser")

            title, description = extract_metadata(soup)
            title_length = len(title)
            desc_length = len(description)
            has_ga = detect_ga_code(soup)
            has_noindex = detect_noindex(soup)

            if has_ga:
                found_ga = True
            if has_noindex:
                noindex_urls.append(url)

            results.append({
                "url": url,
                "status": status,
                "title": title,
                "title_length": title_length,
                "description": description,
                "description_length": desc_length,
            })

            # Detect links
            for a in soup.find_all("a", href=True):
                link = urljoin(url, a['href'])
                if link.startswith("mailto") or link.startswith("javascript"):
                    continue
                if is_internal(link, start_url):
                    internal_links.add(link)
                    if link not in visited and link not in to_visit:
                        to_visit.append(link)
                else:
                    external_links.add(link)

        except requests.RequestException:
            visited.add(url)
            results.append({
                "url": url,
                "status": "Error",
                "title": "Request failed",
                "title_length": 0,
                "description": "",
                "description_length": 0,
            })

    # Check robots.txt and sitemap.xml manually
    parsed = urlparse(start_url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    try:
        rbt = requests.get(urljoin(base, "/robots.txt"), timeout=5)
        found_robots = rbt.status_code == 200
    except:
        pass

    try:
        sm = requests.get(urljoin(base, "/sitemap.xml"), timeout=5)
        found_sitemap = sm.status_code == 200
    except:
        pass

    summary = {
        "total_pages": len(visited),
        "internal_links": len(internal_links),
        "external_links": len(external_links),
        "robots_found": found_robots,
        "sitemap_found": found_sitemap,
        "ga_found": found_ga,
        "noindex_count": len(noindex_urls)
    }

    return results, summary
