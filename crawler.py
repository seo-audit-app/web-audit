# crawler.py
from utils import clean_url, is_valid_url, is_same_domain
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_internal(url, base):
    return urlparse(url).netloc == urlparse(base).netloc

def crawl_website(start_url, max_pages=20):
    visited = set()
    results = []

    try:
        queue = [start_url]

        while queue and len(visited) < max_pages:
            url = queue.pop(0)
            if url in visited:
                continue

            try:
                response = requests.get(url, timeout=5)
                status = response.status_code
                soup = BeautifulSoup(response.text, "html.parser")
                
                title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"
                title_length = len(title)
                
                results.append((url, status, title, title_length))
                visited.add(url)

                # Find internal links
                for a in soup.find_all('a', href=True):
                    link = urljoin(url, a['href'])
                    if is_internal(link, start_url) and link not in visited:
                        queue.append(link)

            except requests.RequestException:
                results.append((url, "Error", "Request failed", 0))
                visited.add(url)

    except Exception as e:
        results.append((start_url, "Error", str(e), 0))

    return results
