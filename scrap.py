# Import Files
from crawl1 import crawl_item
from Utils import get_page_source

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
    with open('prod.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f,
                                fieldnames=['name', 'category', 'price', 'ASIN', 'BSR', 'reviews', 'rating', 'search',
                                            'url'])
        # writer = csv.DictWriter(f, fieldnames=['search', 'url'])
        for p in products:
            writer.writerow(p)


def program():
    subject_hrefs = []

    for page_url in page_URLs:
        subject_hrefs.extend(fetch_product_urls(page_url))

    print(len(subject_hrefs))
    products = []

    with ThreadPoolExecutor() as executor:
        for product in executor.map(crawl_item, subject_hrefs):
            products.append(product)

    save_data(products)


if __name__ == "__main__":
    program()