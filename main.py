from manga_fetcher import search_manga, get_manga_chapters, get_chapter_pages
from downloader import download_images
from convert_to_pdf import images_to_pdf
import os
import shutil
from tqdm import tqdm

def clear_screen():
    # Clear command based on operating system
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    title = input("Enter the manga title to search: ")
    mangas = search_manga(title)

    if not mangas:
        print("No manga found.")
        return

    clear_screen()
    print(f"Search results for: {title}\n")
    for idx, (manga_id, manga_title) in enumerate(mangas, start=1):
        print(f"{idx}. {manga_title} (ID: {manga_id})")

    manga_idx = int(input("\nSelect the manga by number: ")) - 1
    manga_id, manga_title = mangas[manga_idx]

    chapters = get_manga_chapters(manga_id)
    if not chapters:
        print("No chapters found.")
        return

    # Sort chapters by chapter number
    sorted_chapters = sorted(chapters, key=lambda x: float(x[1].split()[0].split('.')[0]))

    clear_screen()
    print(f"Chapters for {manga_title}:\n")
    for idx, (chapter_id, chapter_name) in enumerate(sorted_chapters, start=1):
        print(f"{idx}. Chapter {chapter_name}")

    chapter_idx = int(input("Select a chapter to download images by number: ")) - 1
    chapter_id, chapter_name = sorted_chapters[chapter_idx]

    clear_screen()
    print(f"Processing Chapter {chapter_name} of '{manga_title}'...")
    image_urls = get_chapter_pages(chapter_id)

    if image_urls:
        total_steps = 4
        with tqdm(total=total_steps, desc="Overall Progress", position=0) as pbar:
            pbar.set_description("Downloading images")
            download_images(f"Chapter_{chapter_name}", manga_title, image_urls)
            pbar.update(1)
            
            pbar.set_description("Converting to PDF")
            pdf_path = images_to_pdf(f"Chapter_{chapter_name}", manga_title, len(image_urls))
            pbar.update(1)

            pbar.set_description("Moving PDF")
            pbar.update(1)

            pbar.set_description("Cleaning up")
            images_folder = os.path.join("downloads", manga_title, f"Chapter_{chapter_name}")
            if os.path.exists(images_folder):
                shutil.rmtree(images_folder)
            pbar.update(1)
            
            print(f"\nCompleted! PDF saved at: {pdf_path}")
    else:
        print(f"No images found for Chapter {chapter_name}.")

if __name__ == "__main__":
    main()
