import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO


def dummy_function(url):
    print(f"url: {url}")
    url = 'http://olympus.realpython.org/profiles/aphrodite'
    response = requests.get(url, headers=headers)
    print(f"response: {response}")

    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    print(f"images: {images}")

    image_data = []
    for img in images:
        src = img.get('src')
        if src:
            full_url = urljoin(url, src)
            image_data.append(full_url)
    print(f"image_data: {image_data}")
    return image_data


def get_image_dimensions(url):
    try:
        response = requests.get(url, headers=headers)
    except:
        return None, None
    
    if response.status_code == 200:
        try:
            img = Image.open(BytesIO(response.content))
            width, height = img.size
        except:
            return None, None
        return width, height
    else:
        return None, None

def get_all_images_above_dimensions(url, min_width, min_height):
    try:
        response = requests.get(url, headers=headers)
    except:
        return []

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
# website_url = 'https://www.bol.com/be/nl/p/lego-star-wars-millennium-falcon-75375/9300000157956368/?bltgh=u2ApZSQ0eyUc3Wj8pfxObw.2_18.22.ProductTitle'
# website_url = 'https://www.amazon.com.be/-/en/Feandrea-Stuffing-Machine-Washable-PGW204G01/dp/B09TSZJW1B/?_encoding=UTF8&pd_rd_w=7u7nj&content-id=amzn1.sym.78427eee-a311-4484-b77d-804ebca95bf1&pf_rd_p=78427eee-a311-4484-b77d-804ebca95bf1&pf_rd_r=FET1T0TFS1KTKZF850Q8&pd_rd_wg=G7Kef&pd_rd_r=2495e6aa-ffc4-480f-bd05-f0f94059ab87&ref_=pd_gw_crs_zg_bs_27157903031&th=1'
website_url = 'http://olympus.realpython.org/profiles/aphrodite'

min_width = 100
min_height = 100

# headers = {
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
# }

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def get_images(website_url):
    filtered_image_urls = get_all_images_above_dimensions(website_url, min_width, min_height)
    return filtered_image_urls


if __name__ == '__main__':
    # filtered_image_urls = get_images(website_url)

    # print(f"Image URLs above {min_width}x{min_height} pixels, sorted by resolution:")
    # for url in filtered_image_urls:
    #     print(url)
    print(dummy_function('bol.com'))
