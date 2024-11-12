import requests
from ratelimit import limits, sleep_and_retry

BASE_URL = "https://api.mangadex.org"
ONE_MINUTE = 60  # Adjust this based on MangaDex API's rate limit if known

# Fetch manga based on title
def search_manga(title):
    url = f"{BASE_URL}/manga"
    params = {"title": title}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return [(manga["id"], manga["attributes"]["title"]["en"]) for manga in data["data"]]
    else:
        print(f"Failed to search for manga '{title}'. Status code: {response.status_code}")
        return []

# Fetch chapters for a specific manga ID
def get_manga_chapters(manga_id):
    url = f"{BASE_URL}/manga/{manga_id}/feed"
    params = {
        "translatedLanguage[]": "en",
        "limit": 500,  # Increase limit to get all chapters
        "order[chapter]": "asc"  # Sort by chapter number
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        
        # Create a dictionary to store unique chapters
        unique_chapters = {}
        
        for chapter in data["data"]:
            chapter_num = chapter["attributes"]["chapter"]
            
            # Only store the chapter if we haven't seen it before
            if chapter_num not in unique_chapters:
                unique_chapters[chapter_num] = (chapter["id"], chapter_num)
        
        # Convert back to list and sort by chapter number
        chapters = list(unique_chapters.values())
        chapters.sort(key=lambda x: float(x[1]) if x[1].replace('.', '').isdigit() else float('inf'))
        
        return chapters
    else:
        print(f"Failed to retrieve chapters for manga ID {manga_id}. Status code: {response.status_code}")
        return []

# Fetch pages for a specific chapter ID, with rate limiting
@sleep_and_retry
@limits(calls=30, period=ONE_MINUTE)  # Adjust based on MangaDex API's rate limit
def get_chapter_pages(chapter_id):
    url = f"{BASE_URL}/at-home/server/{chapter_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        base_url = data["baseUrl"]
        hash_value = data["chapter"]["hash"]
        page_filenames = data["chapter"]["data"]

        return [f"{base_url}/data/{hash_value}/{filename}" for filename in page_filenames]
    elif response.status_code == 429:
        print(f"Rate limit exceeded for chapter {chapter_id}. Retrying in 5 seconds...")
        time.sleep(5)  # Optional additional sleep to retry
        return get_chapter_pages(chapter_id)
    else:
        print(f"Failed to retrieve pages for chapter {chapter_id}. Status code: {response.status_code}")
        return []
