# Mg Downloader

A Python application that allows you to search, download, and convert manga chapters to PDF format using the MangaDex API.

## Features

- Search manga by title
- List available chapters
- Download manga chapters
- Automatically convert chapters to PDF
- Clean up temporary files after conversion

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/manga-downloader.git

   cd manga-downloader
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script:
```bash
python main.py
```

Follow the interactive prompts to:
1. Enter a manga title to search
2. Select the desired manga from search results
3. Choose a chapter to download
4. Wait for the download and PDF conversion to complete

## Project Structure
manga-downloader/
├── main.py
├── manga_fetcher.py
├── downloader.py
├── convert_to_pdf.py
├── requirements.txt
└── README.md

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [MangaDex API](https://api.mangadex.org/) for providing the manga data
