from Utilities.Utils import get_page_source
from Utilities.MetadataUtils import *

# Import libraries
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def create_group(search_url):
    candidate_urls = get_candidate_urls(search_url)
    candidates_metadata = get_candidates_metadata(candidate_urls)


def get_candidates_metadata(urls):
    all_metadata = []
    futures = []

    executor = ThreadPoolExecutor()

    for url in urls:
        futures.append(executor.submit(get_candidate_metadata, url))
        all_metadata.append(get_candidate_metadata(url))

    for future in futures:
        res = future.result()
        all_metadata.extend(res)

    return all_metadata


def get_candidate_metadata(url):
    page = get_page_source(url)
    soup1 = BeautifulSoup(page, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    metadata = {
        'name': get_name(soup2),
        'category': get_category(soup2),
        'price': get_price(soup2),
        'ASIN': get_asin(url),
        'reviews': get_reviews(soup2),
        'rating': get_rating(soup2),
        'url': url,
        'quantity': "NA", # TBD with jungleScout Api
        'revenue': "NA",
        'dimensions': get_product_dimensions(soup2)
    }

    return metadata




def get_candidate_urls(search_url):
    page = get_page_source(search_url)
    soup1 = BeautifulSoup(page, "html.parser")

    hrefs = soup1.find_all("a",
                           {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

    candidate_urls = []
    for href in hrefs:
        candidate_urls.append("https://amazon.com" + href.attrs['href'])
    return candidate_urls

