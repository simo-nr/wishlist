import requests as r
from bs4 import BeautifulSoup
import os
import re

base_url = 'https://www.amazon.com.be'
url = 'https://www.amazon.com.be/-/en/dp/B0B928CDMT/?coliid=I2FV1G7XZ2ICR3&colid=150D9KTIA0UMT&psc=1&ref_=list_c_wl_lv_ov_lig_dp_it'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
}

def find_lines_with_word(url, target_word):
    base_response = r.get(base_url, headers=headers)
    cookies = base_response.cookies

    product_response = r.get(url, headers=headers, cookies=cookies)
    # Send a request to the URL

    # Check if the request was successful (status code 200)
    if product_response.status_code == 200:
        # Parse the HTML content of the page
        cleaned_html = remove_css_from_html(product_response.text)
        soup = BeautifulSoup(cleaned_html, 'html.parser')
        
        # Find all text elements that contain the target word
        lines_with_word = soup.find_all(string=lambda string: target_word.lower() in string.lower())

        # Extract the parent elements (lines) of the matching text
        lines = [line.parent for line in lines_with_word]

        return lines

    else:
        print(f"Failed to retrieve the page. Status code: {product_response.status_code}")
        return None
    

def writeToFile(text):
    
    f = open("junk/test.html", "a")
    f.write(text + '\n')
    f.close()
    

def somefunction():
    # Example usage
    url = 'https://www.amazon.com.be/-/en/dp/B0B928CDMT/?coliid=I2FV1G7XZ2ICR3&colid=150D9KTIA0UMT&psc=1&ref_=list_c_wl_lv_ov_lig_dp_it'
    target_word = 'price'

    lines_containing_word = find_lines_with_word(url, target_word)

    if lines_containing_word:
        print(f"Lines containing the word '{target_word}' on the webpage {url}:")
        for line in lines_containing_word:
            writeToFile(line.get_text().strip())
    else:
        print(f"Failed to find lines containing the word '{target_word}' on the webpage {url}.")


def find_lines_with_word_in_file(url, target_word):
    base_response = r.get(base_url, headers=headers)
    cookies = base_response.cookies

    product_response = r.get(url, headers=headers, cookies=cookies)

    # Parse the HTML content of the file
    soup = BeautifulSoup(product_response, 'html.parser')

    # Find all text elements that contain the target word
    lines_with_word = soup.find_all(text=lambda text: target_word.lower() in text.lower())

    # Extract the parent elements (lines) of the matching text
    lines = [line.parent for line in lines_with_word]

    return lines

def someotherfunction():
    target_word = 'price'
    url = 'https://www.amazon.com.be/-/en/dp/B0B928CDMT/?coliid=I2FV1G7XZ2ICR3&colid=150D9KTIA0UMT&psc=1&ref_=list_c_wl_lv_ov_lig_dp_it'

    lines_containing_word = find_lines_with_word_in_file(url, target_word)

    if lines_containing_word:
        print(f"Lines containing the word '{target_word}' in the HTML file:")
        for line in lines_containing_word:
            print(line.get_text().strip())
            writeToFile(line.get_text().strip())
    else:
        print(f"Failed to find lines containing the word '{target_word}' in the HTML file.")


def remove_css_from_html(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find and remove style elements
    for style_tag in soup.find_all('style'):
        style_tag.extract()

    # Get the remaining text content
    cleaned_html = soup.get_text()
    cleaned_html = re.sub("<script.*?>.*?</script.*?>", "", cleaned_html)

    return cleaned_html


if __name__ == '__main__':
    try:
        os.remove("junk/test.html")
    except:
        print("no file found")
    somefunction()