import os
from PIL import Image
from pathlib import Path
from tqdm import tqdm

def images_to_pdf(chapter_folder, manga_title, num_images):
    chapter_path = Path(f"downloads/{manga_title}/{chapter_folder}")
    image_files = [chapter_path / f"page_{i+1}.jpg" for i in range(num_images)]
    
    # Silently check for missing files
    missing_files = [img_file for img_file in image_files if not img_file.exists()]
    if missing_files:
        return

    images = []
    with tqdm(total=num_images, desc="Converting", position=1, leave=False) as pbar:
        for i in range(1, num_images + 1):
            try:
                image = Image.open(image_files[i-1]).convert('RGB')
                images.append(image)
                pbar.update(1)
            except Exception:
                return

    pdf_path = Path(f"downloads/{manga_title}/{chapter_folder}.pdf")
    
    try:
        images[0].save(pdf_path, save_all=True, append_images=images[1:], resolution=100.0, quality=95)
    except Exception:
        return

    # Silently delete image files
    for img_file in image_files:
        try:
            os.remove(img_file)
        except Exception:
            pass
    
    parent_folder = Path(f"downloads/{manga_title}")
    parent_folder.mkdir(parents=True, exist_ok=True)
    parent_pdf_path = parent_folder / f"{chapter_folder}.pdf"
    
    if pdf_path.exists():
        os.rename(pdf_path, parent_pdf_path)
        return str(parent_pdf_path)
    return None
