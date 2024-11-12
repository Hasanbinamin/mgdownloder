import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm

# Helper function to set up a session with retry strategy
def create_session_with_retries():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# Create directories if they don't exist and download images
def download_images(chapter_name, manga_title, image_urls):
    download_dir = os.path.join("downloads", manga_title, chapter_name)
    os.makedirs(download_dir, exist_ok=True)

    session = create_session_with_retries()
    failed_downloads = []

    with tqdm(total=len(image_urls), desc="Downloading", position=1, leave=False) as pbar:
        for i, url in enumerate(image_urls, 1):
            try:
                response = session.get(url, timeout=10)
                if response.status_code == 200:
                    image_path = os.path.join(download_dir, f"page_{i}.jpg")
                    with open(image_path, "wb") as img_file:
                        img_file.write(response.content)
                else:
                    failed_downloads.append((i, url))
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                failed_downloads.append((i, url))
            pbar.update(1)

    # Retry failed downloads silently
    for index, image_url in failed_downloads:
        try:
            response = session.get(image_url, timeout=10)
            if response.status_code == 200:
                image_path = os.path.join(download_dir, f"page_{index}.jpg")
                with open(image_path, "wb") as img_file:
                    img_file.write(response.content)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pass
