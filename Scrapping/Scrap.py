# Import Files
from Scrapping.Crawl import crawl_item
from Utilities.Utils import get_page_source

# Import libraries
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor

page_URLs = ["https://www.amazon.com/gp/new-releases/home-garden",
             "https://www.amazon.com/gp/new-releases/home-garden/ref=zg_bsnr_pg_2?ie=UTF8&pg=2"]


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
            products.append(res)

    return products


def program():
    subject_hrefs = get_product_page_hrefs()
    products = get_product_details(subject_hrefs[:2])

    save_data(products)
    return products
