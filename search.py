import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# MONGO DATABASE SETUP
MONGO_URI = "mongodb://yashdd:password@yashdd.a9gbuqp.mongodb.net/?retryWrites=true&w=majority&appName=yashdd"
client = MongoClient(MONGO_URI)
db = client["yashdd"]
collection = db["movies"]

# KATMOVIEHD SCRAPER
def scrape_katmoviehd():
    url = "https://katmoviehd.wales/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    posts = soup.find_all("h2", class_="title")

    for post in posts[:10]:
        try:
            title = post.get_text(strip=True)
            link = post.a["href"]
            movie_page = requests.get(link)
            movie_soup = BeautifulSoup(movie_page.text, "html.parser")
            download_section = movie_soup.find("a", string=lambda s: s and "Download" in s)
            file_link = download_section["href"] if download_section else ""

            data = {
                "title": title,
                "quality": "Unknown",
                "audio": "Dual",
                "file_link": file_link,
                "source": "katmoviehd"
            }
            collection.update_one({"title": title}, {"$set": data}, upsert=True)
            print(f"Inserted: {title}")
        except Exception as e:
            print(f"Failed for {title}: {e}")

# HDHUB4U SCRAPER
def scrape_hdhub4u():
    url = "https://hdhub4u.graphics/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    posts = soup.find_all("h2", class_="entry-title")

    for post in posts[:10]:
        try:
            title = post.get_text(strip=True)
            link = post.a["href"]
            movie_page = requests.get(link)
            movie_soup = BeautifulSoup(movie_page.text, "html.parser")
            download_links = movie_soup.find_all("a", href=True)
            file_link = ""
            for a in download_links:
                if "mkvcinemas" in a["href"] or "download" in a["href"]:
                    file_link = a["href"]
                    break

            data = {
                "title": title,
                "quality": "Unknown",
                "audio": "Dual",
                "file_link": file_link,
                "source": "hdhub4u"
            }
            collection.update_one({"title": title}, {"$set": data}, upsert=True)
            print(f"Inserted: {title}")
        except Exception as e:
            print(f"Failed for {title}: {e}")

# RUN BOTH SCRAPERS
scrape_katmoviehd()
scrape_hdhub4u()
print("Scraping Completed!")
