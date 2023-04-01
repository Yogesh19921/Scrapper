# Import Files
from CollectingProducts.Crawl import crawl_item
from Utilities.Utils import get_page_source
from CollectingProducts.CollectionServiceBusUtils import *

# Import libraries
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
import random


def fetch_product_urls(page_url):
    content = get_page_source(page_url=page_url, scroll=True)

    soup1 = BeautifulSoup(content, "html.parser")
    subject_urls = soup1.find_all("a", {"class": "a-link-normal", "tabindex": "-1", "role": "link"})

    return subject_urls


def get_product_details(subject_hrefs):
    products = []
    futures = []

    executor = ThreadPoolExecutor(max_workers=1)

    for href in subject_hrefs:
        futures.append(executor.submit(crawl_item, href))

    for future in futures:
        res = future.result()
        if res is not None:
            send_message(json.dumps(res))
            products.append(res)

    return products


def crawl_and_generate_search_url(product_url):
    product_metadata = crawl_item(product_url)
    send_message(json.dumps(product_metadata))
    print("Sent the product metadata with search URL")
    print("====================")


def send_url_to_sb(hrefs):
    for href in hrefs:
        url = "https://amazon.com" + href.attrs['href']
        send_message_best_sellers({
            'url': url
        })


def collect_and_send_url_to_sb(url):
    subject_hrefs = fetch_product_urls(url)
    random.shuffle(subject_hrefs)
    print("Total subject hrefs =============" + str(len(subject_hrefs)))
    products = get_product_details(subject_hrefs)

    return products
