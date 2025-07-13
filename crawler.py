import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re


def is_internal(url, base):
    return urlparse(url).netloc == urlparse(base).netloc

def detect_ga_code(soup):
    return bool(soup.find("script", string=re.compile("google-analytics|gtag|ga\\(")))

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

    robots = ""
    robots_tag = soup.find("meta", attrs={"name": "robots"})
    if robots_tag and robots_tag.get("content"):
        robots = robots_tag["content"].strip()

    canonical = ""
    link_tag = soup.find("link", attrs={"rel": "canonical"})
    if link_tag and link_tag.get("href"):
        canonical = link_tag["href"].strip()

    lang = ""
    html_tag = soup.find("html")
    if html_tag and html_tag.get("lang"):
        lang = html_tag["lang"]

    h1_count = len(soup.find_all("h1"))
    h2_count = len(soup.find_all("h2"))

    breadcrumb = soup.find(class_=re.compile("breadcrumb"))
    has_breadcrumbs = bool(breadcrumb)

    schema = soup.find(attrs={"type": re.compile("application/ld\+json")})
    has_schema = bool(schema)

    favicon = soup.find("link", rel=re.compile("icon", re.I))
    has_favicon = bool(favicon)

    return {
        "title": title,
        "description": description,
        "robots": robots,
        "canonical": canonical,
        "lang": lang,
        "h1_count": h1_count,
        "h2_count": h2_count,
        "breadcrumbs": has_breadcrumbs,
        "schema": has_schema,
        "favicon": has_favicon
    }

def crawl_website(start_url, max_pages=50):
    visited = set()
    to_visit = [start_url]
    results = []

    internal_links = set()
    external_links = set()
    broken_links = set()
    found_ga = False
    found_sitemap = False
    found_robots = False
    noindex_urls = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=10)
            visited.add(url)
            status = response.status_code
            content_type = response.headers.get("Content-Type", "")
            content_length = int(response.headers.get("Content-Length", 0))
            size_kb = round(content_length / 1024, 2)
            is_https = urlparse(url).scheme == "https"

            if "text/html" not in content_type:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            meta = extract_metadata(soup)
            has_ga = detect_ga_code(soup)
            has_noindex = detect_noindex(soup)
            if has_ga:
                found_ga = True
            if has_noindex:
                noindex_urls.append(url)

            img_count = len(soup.find_all("img"))

            results.append({
                "url": url,
                "status": status,
                "https": is_https,
                "title": meta['title'],
                "title_length": len(meta['title']),
                "description": meta['description'],
                "description_length": len(meta['description']),
                "robots_meta": meta['robots'],
                "canonical": meta['canonical'],
                "lang": meta['lang'],
                "h1_count": meta['h1_count'],
                "h2_count": meta['h2_count'],
                "breadcrumbs": meta['breadcrumbs'],
                "schema": meta['schema'],
                "favicon": meta['favicon'],
                "images": img_count,
                "page_size_kb": size_kb
            })

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

        except requests.RequestException as e:
            visited.add(url)
            broken_links.add(url)

    # Check robots.txt and sitemap.xml
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
        "broken_links": len(broken_links),
        "robots_txt": found_robots,
        "sitemap_xml": found_sitemap,
        "ga_code_found": found_ga,
        "noindex_count": len(noindex_urls),
    }

    return results, summary
