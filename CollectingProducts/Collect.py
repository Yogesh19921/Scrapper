# Import Files
from CollectingProducts.Crawl import crawl_item
from Utilities.Utils import get_page_source
from CollectingProducts.CollectionServiceBusUtils import send_message

# Import libraries
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor
import json
import random

page_URLs = ["https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing/zgbs/arts-crafts/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Automotive/zgbs/automotive/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Baby/zgbs/baby-products/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Industrial-Scientific/zgbs/industrial/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Musical-Instruments/zgbs/musical-instruments/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Office-Products/zgbs/office-products/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden/zgbs/lawn-garden/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Tools-Home-Improvement/zgbs/hi/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/ref=zg_bs_nav_0"]


def fetch_product_urls(page_url):
    content = get_page_source(page_url=page_url, scroll=True)

    soup1 = BeautifulSoup(content, "html.parser")
    subject_urls = soup1.find_all("a", {"class": "a-link-normal", "tabindex": "-1", "role": "link"})

    return subject_urls


def save_data(products):
    columns = ['name', 'category', 'price', 'ASIN', 'BSR', 'reviews', 'rating', 'search', 'url']
    with open('prod.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        for p in products:
            writer.writerow(p)


def get_product_page_hrefs():
    subject_hrefs = []
    futures = []

    executor = ThreadPoolExecutor()

    for page_url in page_URLs:
        futures.append(executor.submit(fetch_product_urls, page_url))

    for future in futures:
        res = future.result()
        subject_hrefs.extend(res)

    return subject_hrefs


def get_product_details(subject_hrefs):
    products = []
    futures = []

    executor = ThreadPoolExecutor()

    for href in subject_hrefs:
        futures.append(executor.submit(crawl_item, href))

    for future in futures:
        res = future.result()
        if res is not None:
            send_message(json.dumps(res))
            products.append(res)

    return products


def program():
    subject_hrefs = get_product_page_hrefs()
    random.shuffle(subject_hrefs)
    print("Total subject hrefs =============" + str(len(subject_hrefs)))
    products = get_product_details(subject_hrefs)

    return products