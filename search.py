import requests
from bs4 import BeautifulSoup
import jsoj

def hdhub4u_scraper(movie_name):
    # HDHub4U URL (Search page)
    search_url = f'https://hdhub4u.graphics/?s={movie_name}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    movies = []
    
    # Find all movie links in search results
    for link in soup.find_all('a', class_='post-title'):
        movie_url = link.get('href')
        movie_title = link.text.strip()
        
        # Fetch movie page details
        movie_response = requests.get(movie_url, headers=headers)
        movie_soup = BeautifulSoup(movie_response.text, 'html.parser')
        
        # Extract quality, format, size (if available)
        details = {
            'title': movie_title,
            'url': movie_url,
            'quality': 'N/A',
            'size': 'N/A',
            'format': 'N/A'
        }
        
        for tag in movie_soup.find_all('span', {'class': 'quality'}):
            details['quality'] = tag.text.strip()
        
        for tag in movie_soup.find_all('span', {'class': 'size'}):
            details['size'] = tag.text.strip()
        
        for tag in movie_soup.find_all('span', {'class': 'format'}):
            details['format'] = tag.text.strip()
        
        movies.append(details)
    
    return json.dumps(movies, indent=4)

# Example usage
movie_name = "Pathaan"
movie_data = hdhub4u_scraper(movie_name)
print(movie_data)
