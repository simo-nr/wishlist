# from urllib.request import urlopen
import requests as r
import bs4
import re
import os


base_url = 'https://www.amazon.com.be'
url = 'https://www.amazon.com.be/-/en/dp/B0B928CDMT/?coliid=I2FV1G7XZ2ICR3&colid=150D9KTIA0UMT&psc=1&ref_=list_c_wl_lv_ov_lig_dp_it'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
}


def someFunction():
    base_response = r.get(base_url, headers=headers)
    cookies = base_response.cookies

    product_response = r.get(url, headers=headers, cookies=cookies)

    soup = bs4.BeautifulSoup(product_response.text, features='html.parser')
    price_lines = soup.find_all(class_="a-price-whole")
    item_price = price_lines[0]
    item_price = re.sub("<.*?>", "", str(item_price))
    print(item_price)


def find_word_on_webpage(url, target_word):
    base_response = r.get(base_url, headers=headers)
    cookies = base_response.cookies

    product_response = r.get(url, headers=headers, cookies=cookies)

    # Check if the request was successful (status code 200)
    if product_response.status_code == 200:
        # Parse the HTML content of the page
        soup = bs4.BeautifulSoup(product_response.text, 'html.parser')

        # Find all occurrences of the target word
        occurrences = soup.body(text=lambda text: target_word.lower() in text.lower())

        return occurrences

    else:
        print(f"Failed to retrieve the page. Status code: {product_response.status_code}")
        return None
    

def find_word(url, target_word):
    base_response = r.get(base_url, headers=headers)
    cookies = base_response.cookies
    data = r.get(url, headers=headers, cookies=cookies)

    clean_html = re.sub("<script.*?>.*?</script.*?>", "", data.text)

    soup = bs4.BeautifulSoup(clean_html, 'html.parser')
    results = soup.body.find_all(string = re.compile('.*{0}.*'.format(target_word)), recursive=True)
    return results

    

def writeToFile(text):
    try:
        os.remove("junk/test.html")
    except:
        print("no file found")
    f = open("junk/test.html", "a")
    f.write(text)
    f.close()

    
if __name__ == "__main__":
    url = 'https://www.amazon.com.be/-/en/dp/B0B928CDMT/?coliid=I2FV1G7XZ2ICR3&colid=150D9KTIA0UMT&psc=1&ref_=list_c_wl_lv_ov_lig_dp_it'
    text = find_word(url, target_word="price")
    for line in text:
        writeToFile(line)