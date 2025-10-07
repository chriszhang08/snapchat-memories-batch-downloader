# Snapchat Memories Downloader

This Python script downloads Snapchat Memories from an exported HTML file by extracting download URLs, sending POST requests to obtain AWS S3 signed URLs, and downloading the media files to your local machine.

## Requirements

- Python 3.7 or higher
- Internet connection
- Snapchat data export HTML file

## Installation

1. Download or clone this repository to your local machine.

2. Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```


## Usage

1. **Export your Snapchat data:**
   - Go to Snapchat and request a data export
   - Download the ZIP file containing your memories
   - Extract the ZIP file and locate the HTML file (usually named `memories_history.html`)

2. **Configure the script:**
   - Open `snapchat_memories_downloader.py` in a text editor
   - Update the following variables at the top of the file:
     - `html_file_path`: Path to your Snapchat memories HTML file
     - `output_dir`: Directory where you want to save downloaded media files

Example:
```python
html_file_path = 'memories_history.html'
output_dir = 'D:\Pictures\Camera Roll\Snapchat Memories'
```

3. **Run the script:**

4. The script will:
   - Parse the HTML file to extract download URLs
   - Send POST requests to Snapchat's servers to obtain AWS S3 signed URLs
   - Download each media file (images and videos) to your specified output directory
   - Display progress messages for each download

## How It Works

1. **HTML Parsing:** The script uses BeautifulSoup to parse the exported HTML file and extract JavaScript download links.

2. **URL Extraction:** Regular expressions extract the actual HTTPS URLs from the JavaScript function calls.

3. **Two-Step Download Process:**
   - First, the script sends a POST request to the Snapchat endpoint
   - The server responds with an AWS S3 pre-signed URL
   - The script then downloads the actual media file from AWS S3

4. **File Naming:** Downloaded files are saved with sequential names (e.g., `media_1.mp4`, `media_2.jpg`) preserving their original file extensions.

## Troubleshooting

- **"HTTP method GET is not supported":** This error occurs if you try to access the URLs directly in a browser. The script uses POST requests as required by Snapchat's API.

- **"Failed to download" errors:** These may occur due to expired URLs, network issues, or rate limiting. The script will continue downloading remaining files.

- **Missing files:** Ensure your HTML file path is correct and that the file contains the expected `javascript:downloadMemories()` links.

## Notes

- Download URLs from Snapchat may have expiration times (typically 7 days based on the `X-Amz-Expires` parameter).
- Ensure you have sufficient disk space for all your memories.
- The script will create the output directory if it doesn't exist.

## License

This script is provided as-is for personal use only.
