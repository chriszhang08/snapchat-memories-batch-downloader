import os
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

# Set your local HTML file path and desired output directory here
html_file_path = 'memories_history.html'
output_dir = 'TODO INSERT YOUR OUTPUT DIRECTORY HERE'

os.makedirs(output_dir, exist_ok=True)


def extract_url(js_string):
    """
    Extracts the HTTPS URL from a JavaScript function call string.

    Args:
        js_string: A string containing a JavaScript call with an embedded URL.

    Returns:
        The extracted URL string, or None if no URL is found.
    """
    match = re.search(r"https://[^\']+", js_string)
    if match:
        return match.group(0)
    return None


def extract_extension(url):
    """
    Extracts the file extension from the path portion of a URL.

    Args:
        url: A complete URL string.

    Returns:
        The file extension including the dot (e.g., '.mp4'), or an empty string if no extension found.
    """
    parsed = urlparse(url)
    path = parsed.path
    ext = os.path.splitext(path)[-1]
    return ext


# Read and parse the HTML
with open(html_file_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Extract all URLs from 'href' attributes in anchor tags
urls = []
for tag in soup.find_all(['a']):
    for attr in ['href']:
        url = tag.get(attr)
        if url and url.startswith('javascript:downloadMemories('):
            urls.append(extract_url(url))

# Download each media file
for i, url in enumerate(urls):
    try:
        # Step 1: POST to Snapchat endpoint to get AWS media link
        response = requests.post(url, timeout=10)
        response.raise_for_status()

        # Extract the AWS S3 signed URL from the response
        aws_url = response.text.strip()

        # Step 2: GET the AWS link to download the actual media file
        media_response = requests.get(aws_url, stream=True, timeout=10)
        media_response.raise_for_status()

        # Extract file extension from the AWS link
        ext = extract_extension(aws_url)
        if not ext or len(ext) > 5:
            ext = ""  # fallback in case of missing or weird extension
        file_name = os.path.join(output_dir, f'media_{i + 1}{ext}')

        # Save file to disk
        with open(file_name, 'wb') as f_out:
            for chunk in media_response.iter_content(chunk_size=8192):
                f_out.write(chunk)
        print(f'Downloaded: {file_name}')
    except Exception as e:
        print(f'Failed to download from {url}: {e}')

print(f'Downloads saved to {output_dir}')
