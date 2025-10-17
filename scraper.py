import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import time
import random

def sanitize_filename(url):
    path = urlparse(url).path
    filename = os.path.basename(path)
    filename = unquote(filename)  # Decode URL-encoded characters
    return filename

def create_unique_folder(base_folder='images'):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    unique_folder = os.path.join(base_folder, timestamp)
    os.makedirs(unique_folder, exist_ok=True)
    return unique_folder

def scrape_images(url, folder_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tags = soup.find_all('img')

        for img in img_tags:
            img_url = img.get('src') or img.get('data-src')
            if not img_url or img_url.startswith('data:'):
                continue

            img_url = urljoin(url, img_url)
            img_name = sanitize_filename(img_url)

            if not img_name:
                continue

            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                img_path = os.path.join(folder_path, img_name)
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"Saved image: {img_path}")
            else:
                print(f"Failed to download image: {img_url}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")

def find_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

def load_seed_urls(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    return []

def save_seed_urls(file_path, seed_urls):
    with open(file_path, 'w') as file:
        for url in seed_urls:
            file.write(url + '\n')

def append_seed_url(file_path, url):
    with open(file_path, 'a') as file:
        file.write(url + '\n')

def automate_scraping(seed_file, interval):
    seed_urls = load_seed_urls(seed_file)
    visited_urls = set()

    while seed_urls:
        current_url = random.choice(seed_urls)
        seed_urls.remove(current_url)
        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)
        print(f"Scraping URL: {current_url}")

        folder_path = create_unique_folder()
        scrape_images(current_url, folder_path)

        new_links = find_links(current_url)
        for link in new_links:
            if link not in visited_urls and link not in seed_urls:
                seed_urls.append(link)
                append_seed_url(seed_file, link)

        save_seed_urls(seed_file, seed_urls)

        print(f"Waiting for {interval} seconds before the next scrape.")
        time.sleep(interval)

if __name__ == "__main__":
    seed_file = 'seed_urls.txt'  # Path to the seed URLs file
    interval = 10  # e.g., 10 seconds for 1 hour

    automate_scraping(seed_file, interval)

#add cool thiong