import requests
import json
import logging
import re
from bs4 import BeautifulSoup
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_movie_details(movie_url):
    try:
        headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json;charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
                }
        response = requests.get(movie_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1').text.strip()
        year = soup.find('a', href=re.compile(r'ref_=tt_ov_rdat.*')).text.strip()
        rating = soup.find('span', class_='sc-bde20123-1 cMEQkK').text.strip()
        directors = [director.text.strip() for director in soup.find_all('li', class_='ipc-metadata-list__item')[0].find_all('a')]
        cast = [actor.text.strip() for actor in soup.find_all('li', class_='ipc-metadata-list__item')[2].find_all('a')][1:-1]
        summary = soup.find('span', class_='sc-466bb6c-2 chnFO').text.strip()

        movie_info = {
            'Title': title,
            'Year': year,
            'IMDb Rating': rating,
            'Directors': directors,
            'Cast': cast,
            'Plot Summary': summary
        }

        return movie_info

    except Exception as e:
        logging.error(f"Error occurred while scraping movie details: {e}")
        return None

def scrape_imdb_movies(genre, num_pages):
    base_url = f'https://www.imdb.com/search/title/?genres={genre}&title_type=feature&sort=user_rating,desc'
    all_movies = []

    try:
        for page in tqdm(range(1, num_pages + 1)):
            page_url = f"{base_url}&start={(page - 1) * 50 + 1}"
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json;charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
                }
            response = requests.get(page_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            movie_links = [a['href'] for a in soup.find_all('a', {'href': re.compile(r'/title/tt.*')})]
            movie_links = [link for link in movie_links if 'ref_=sr_i' in link]

            movies = list(map(get_movie_details, [f"https://www.imdb.com{link}" for link in movie_links]))
            all_movies.extend([movie for movie in movies if movie])

    except Exception as e:
        logging.error(f"Error occurred while scraping IMDb: {e}")

    return all_movies

def main(genre=None, num_pages=None):
    try:
        if genre is None and num_pages is None:
            genre = input("Enter genre or keyword (e.g., 'comedy', 'action'): ")
            num_pages = int(input("Enter number of pages to scrape: "))

        print(f"\nFetching the movies list based on : '{genre}' . . .\n")

        movies = scrape_imdb_movies(genre, num_pages)

        with open('imdb_movies.json', 'w') as f:
            json.dump(movies, f, indent=4)

        logging.info("Scraping completed. Data stored in 'imdb_movies.json'.")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
