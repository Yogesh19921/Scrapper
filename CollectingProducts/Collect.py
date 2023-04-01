# Import Files
from CollectingProducts.Crawl import crawl_item
from Utilities.Utils import get_page_source
from CollectingProducts.CollectionServiceBusUtils import *

# Import libraries
from bs4 import BeautifulSoup
import json
import random


def fetch_product_urls(page_url):
    content = get_page_source(page_url=page_url, scroll=True)

    soup1 = BeautifulSoup(content, "html.parser")
    subject_urls = soup1.find_all("a", {"class": "a-link-normal", "tabindex": "-1", "role": "link"})

    return subject_urls


def crawl_and_generate_search_url(product_url):
    product_metadata = crawl_item(product_url)
    if product_metadata is not None:
        send_message(json.dumps(product_metadata))
        print("Sent the product metadata with search URL")
        print("====================")


def send_urls_to_sb(hrefs):
    for href in hrefs:
        url = "https://amazon.com" + href.attrs['href']
        data = {
            'url': url
        }
        send_message_best_sellers(json.dumps(data))


def collect_and_send_url_to_sb(url):
    subject_hrefs = fetch_product_urls(url)
    random.shuffle(subject_hrefs)
    print("Total subject hrefs ============= " + str(len(subject_hrefs)))
    send_urls_to_sb(subject_hrefs)
