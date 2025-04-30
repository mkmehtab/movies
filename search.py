import requests
from bs4 import BeautifulSoup

def search_movie(query):
    results = []

    # KatMovieHD Search
    kat_url = f"https://katmoviehd.wales/?s={query.replace(' ', '+')}"
    try:
        response = requests.get(kat_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article')
            for article in articles:
                title_tag = article.find('h2', class_='title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag.find('a')['href']
                    # Fetch details from the movie page
                    movie_resp = requests.get(link, timeout=10)
                    if movie_resp.status_code == 200:
                        movie_soup = BeautifulSoup(movie_resp.text, 'html.parser')
                        # Extract quality and size from the content
                        content = movie_soup.get_text()
                        quality = 'Unknown'
                        size = 'Unknown'
                        for line in content.splitlines():
                            if 'Quality' in line:
                                quality = line.split(':')[-1].strip()
                            if 'Size' in line:
                                size = line.split(':')[-1].strip()
                        results.append({
                            'title': title,
                            'quality': quality,
                            'size': size,
                            'link': link
                        })
    except Exception as e:
        print(f"Error fetching from KatMovieHD: {e}")

    # HDHub4u Search
    hdhub_url = f"https://hdhub4u.graphics/?s={query.replace(' ', '+')}"
    try:
        response = requests.get(hdhub_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article')
            for article in articles:
                title_tag = article.find('h2', class_='title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag.find('a')['href']
                    # Fetch details from the movie page
                    movie_resp = requests.get(link, timeout=10)
                    if movie_resp.status_code == 200:
                        movie_soup = BeautifulSoup(movie_resp.text, 'html.parser')
                        # Extract quality and size from the content
                        content = movie_soup.get_text()
                        quality = 'Unknown'
                        size = 'Unknown'
                        for line in content.splitlines():
                            if 'Quality' in line:
                                quality = line.split(':')[-1].strip()
                            if 'Size' in line:
                                size = line.split(':')[-1].strip()
                        results.append({
                            'title': title,
                            'quality': quality,
                            'size': size,
                            'link': link
                        })
    except Exception as e:
        print(f"Error fetching from HDHub4u: {e}")

    return results
