import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO

website_url = 'http://olympus.realpython.org/profiles/aphrodite'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
}


response = requests.get(website_url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
images = soup.find_all('img')

image_data = []
for img in images:
    src = img.get('src')
    if src:
        full_url = urljoin(website_url, src)
        image_data.append({'url': full_url})

print(image_data)