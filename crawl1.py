import requests
from bs4 import BeautifulSoup
import re
import logging
# selenium 4
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions

def crawlItem(url):
    options = EdgeOptions()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Edge(options=options, service=EdgeService(EdgeChromiumDriverManager().install()))
    curr_url = "https://amazon.com" + url.attrs['href']
    print("==================================================")
    #print(curr_url)
    #print("==================================================")
    driver.get(curr_url)
    page = driver.page_source
    driver.quit()
    soup1 = BeautifulSoup(page, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    name = soup2.find("span", {"id": "productTitle"}).text.strip()
    category = None
    if (soup2.find("span", {"class", "cat-link"}) is not None):
        category = soup2.find("span", {"class", "cat-link"}).text.strip()

    if (soup2.find("span", {"class": "ac-keyword-link"}) is not None):
        category = soup2.find("span", {"class": "ac-keyword-link"}).text.strip()

    if (soup2.find("span", {"class": "ac-for-text" }) is not None):
        category = soup2.find("span", {"class": "ac-for-text"}).text.strip()

    ASIN = re.search(r'/[dg]p/([^/]+)', curr_url, flags=re.IGNORECASE).group(1)
    if (soup2.find("span", {"class": "a-offscreen"}) is not None):
        price = soup2.find("span", {"class": "a-offscreen"}).text.strip()
    else:
        price = "NA"

    if (soup2.find("span", {"id": "acrCustomerReviewText"}) is not None):
        reviews = soup2.find("span", {"id": "acrCustomerReviewText"}).text.strip()
    else:
        reviews = "NA"

    if (soup2.find("span", {"data-hook": "rating-out-of-text"}) is not None):
        rating = soup2.find("span", {"data-hook": "rating-out-of-text"}).text.strip()
    else:
        rating = "NA"

    if (category is None):
        print(f'category not found for {curr_url}')
        search = "NA"
    else:
        category = category.split("by ")[0]
        category = category.split("in ")[-1]
        search = 'https://amazon.com/s?k=' + category.replace(' ', '+')

    rows = soup2.find_all('tr')

    BSR = None

    for row in rows:
        if ('Best Sellers Rank' in row.text):
            BSR = row.text.replace("\n", "").strip()
            BSR = BSR.split("Best Sellers Rank")[-1]
            BSR = re.sub(" +", " ", BSR)
            BSR = BSR.replace("#", "\n")
            break


    re.findall(r'(#\d{1} in [a-zA-Z]*)', soup2.find_all('tr')[15].text)

    product = {
        'name': name,
        'category': category,
        'price': price,
        'ASIN': ASIN,
        'reviews': reviews,
        'rating': rating,
        'search': search,
        'url': curr_url,
        'BSR': BSR
    }

    return product


# Smaller description and larger description of the group.
# E.g. - Description of the product in the group. Include:
# - dimensions
# -
