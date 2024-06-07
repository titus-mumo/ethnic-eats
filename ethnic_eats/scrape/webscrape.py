import requests
from bs4 import BeautifulSoup
import json

SEARCH_TERMS = 'trending foods'
GOOGLE_SEARCH_URL = 'https://www.google.com/search'

def google_search(query):
    params = {'q': query, 'num': 10}  # Number of search results to fetch
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(GOOGLE_SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()

    return response.text

def parse_search_results(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    search_results = []

    for g in soup.find_all('div', class_='g'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').get_text() if g.find('h3') else 'No title'
            search_results.append({'title': title, 'link': link})

    return search_results

def fetch_web_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_web_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.string if soup.title else 'No title'
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    return {'title': title, 'paragraphs': paragraphs}

def main():
    search_results_html = google_search(SEARCH_TERMS)
    search_results = parse_search_results(search_results_html)
    web_pages = []

    for result in search_results:
        url = result['link']
        print(f'Fetching: {url}')
        try:
            html_content = fetch_web_page(url)
            parsed_content = parse_web_page(html_content)
            web_pages.append({'url': url, 'content': parsed_content})
        except requests.RequestException as e:
            print(f'Failed to fetch {url}: {e}')

    # Save results to a JSON file
    with open('web_pages.json', 'w') as f:
        json.dump(web_pages, f, indent=2)

if __name__ == '__main__':
    main()
