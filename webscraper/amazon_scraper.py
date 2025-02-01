import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json

options = Options()
options.add_argument('--headless')  # Enabling headless mode for production
options.add_argument('--disable-gpu')

service = Service(r'C:\Users\dilsa\OneDrive\Documents\code\PROJECTS\DEAL_OF_THE_DAY\chromedriver-win64\chromedriver-win64\chromedriver.exe')

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)
baseurl = 'https://www.amazon.com/gp/goldbox?ref_=nav_cs_gb'
driver.get(baseurl)

# Scroll down to load more products
scroll_pause_time = 3  # Time to wait after each scroll
seen_products = set()  # To track already displayed products

def scrape_products():
    """ Scrapes Amazon deals and returns a list of new products with images """
    
    driver.execute_script("window.scrollBy(0, 500);")  # Scroll down 500 pixels
    time.sleep(scroll_pause_time)  # Wait for new content to load

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    product_list = soup.find_all('div', class_='GridItem-module__container_PW2gdkwTj1GQzdwJjejN')
    new_products = []

    for product in product_list:
        name = product.find('span', class_='a-truncate-cut')
        link = product.find('a', href=True)
        discount = product.find('span', class_='a-size-mini')
        image = product.find('img')

        if name and discount and link and image:
            product_name = name.get_text(strip=True)
            product_link = link['href']
            product_discount = discount.get_text(strip=True)
            product_image = image.get('src') or image.get('data-src')

            # Creating a unique id for each product
            product_id = (product_name, product_discount, product_link)

            if product_id not in seen_products:  # Avoid duplicate entries
                seen_products.add(product_id)
                new_products.append({
                    "name": product_name,
                    "discount": product_discount,
                    "link": product_link,
                    "image": product_image
                })

    # Store results in JSON file
    with open('db.json', 'w') as file:
        json.dump(new_products, file, indent=4)

    return new_products 


scrape_products()

