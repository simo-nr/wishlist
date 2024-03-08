import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO

def get_image_dimensions(url):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        return width, height
    else:
        return None, None

def get_all_images_above_dimensions(url, min_width, min_height):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        
        image_data = []
        for img in images:
            src = img.get('src')
            if src:
                full_url = urljoin(url, src)
                width, height = get_image_dimensions(full_url)
                if width is not None and height is not None and width >= min_width and height >= min_height:
                    image_data.append({'url': full_url, 'width': width, 'height': height})
        
        # Sort images by resolution (width * height) in descending order
        sorted_images = sorted(image_data, key=lambda x: x['width'] * x['height'], reverse=True)
        
        return [image['url'] for image in sorted_images]
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return []

# Example usage
# website_url = 'https://www.bol.com/be/nl/p/lego-star-wars-venator-class-republic-attack-cruiser-75367/9300000161235312/?bltgh=ixguWwuO9MsJLy7gyM5AtQ.2_18.23.ProductTitle'
# website_url = 'https://www.amazon.com.be/-/en/75387/dp/B0CFW28JMN/ref=sr_1_17?crid=2JBGQMSLH28FY&keywords=lego+star+wars&qid=1706977355&sprefix=lego+star+wars%2Caps%2C94&sr=8-17'
website_url = 'https://www.bol.com/be/nl/p/lego-star-wars-millennium-falcon-75375/9300000157956368/?bltgh=u2ApZSQ0eyUc3Wj8pfxObw.2_18.22.ProductTitle'

min_width = 100
min_height = 100

def get_images(website_url):
    filtered_image_urls = get_all_images_above_dimensions(website_url, min_width, min_height)

    # print(f"Image URLs above {min_width}x{min_height} pixels, sorted by resolution:")
    # for url in filtered_image_urls:
    #     print(url)

    return filtered_image_urls


if __name__ == '__main__':
    get_images(website_url)
