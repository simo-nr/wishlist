# from urllib.request import urlopen
import requests as r
import bs4
import re


base_url = 'https://www.amazon.com.be'
url = 'https://www.amazon.com.be/-/en/dp/B0B928CDMT/?coliid=I2FV1G7XZ2ICR3&colid=150D9KTIA0UMT&psc=1&ref_=list_c_wl_lv_ov_lig_dp_it'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
}

base_response = r.get(base_url, headers=headers)
cookies = base_response.cookies

product_response = r.get(url, headers=headers, cookies=cookies)

soup = bs4.BeautifulSoup(product_response.text, features='html.parser')
price_lines = soup.find_all(class_="a-price-whole")
item_price = price_lines[0]
item_price = re.sub("<.*?>", "", str(item_price))
print(item_price)