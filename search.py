import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0"
}

def search_hdhub4u(query):
    base_url = "https://hdhub4u.graphics"
    search_url = f"{base_url}/?s={query.replace(' ', '+')}"
    results = []

    try:
        res = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        for post in soup.select("div#content div.post"):
            title_tag = post.select_one("h2 a")
            if not title_tag:
                continue

            title = title_tag.text.strip()
            url = title_tag["href"]

            movie_res = requests.get(url, headers=headers, timeout=10)
            movie_soup = BeautifulSoup(movie_res.text, "html.parser")
            desc = movie_soup.select_one("div.entry-content")
            description = desc.get_text(strip=True)[:500] if desc else "No description found"

            download_links = [
                a["href"]
                for a in movie_soup.select("a")
                if any(x in a["href"] for x in ["download", "desidrive", "linkbox", "gplinks"])
            ]

            results.append({
                "source": "HDHub4u",
                "title": title,
                "url": url,
                "description": description,
                "downloads": download_links[:5]
            })
    except Exception as e:
        print(f"HDHub4u Error: {e}")
    
    return results


def search_katmoviehd(query):
    base_url = "https://katmoviehd.wales"
    search_url = f"{base_url}/?s={query.replace(' ', '+')}"
    results = []

    try:
        res = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        for post in soup.select("div#content article"):
            title_tag = post.select_one("h2 a")
            if not title_tag:
                continue

            title = title_tag.text.strip()
            url = title_tag["href"]

            movie_res = requests.get(url, headers=headers, timeout=10)
            movie_soup = BeautifulSoup(movie_res.text, "html.parser")
            desc = movie_soup.select_one("div.entry-content")
            description = desc.get_text(strip=True)[:500] if desc else "No description found"

            download_links = [
                a["href"]
                for a in movie_soup.select("a")
                if any(x in a["href"] for x in ["katmoviehd", "desidrive", "linkbox", "gplinks"])
            ]

            results.append({
                "source": "KatmovieHD",
                "title": title,
                "url": url,
                "description": description,
                "downloads": download_links[:5]
            })
    except Exception as e:
        print(f"KatmovieHD Error: {e}")

    return results


def search_movies(query):
    return search_hdhub4u(query) + search_katmoviehd(query)
