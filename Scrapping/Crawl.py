# Import files
from Utilities.Utils import get_page_source
from Utilities.MetadataUtils import *

# Import libraries
from bs4 import BeautifulSoup


def crawl_item(href):
    curr_url = "https://amazon.com" + href.attrs['href']
    page = get_page_source(curr_url)
    soup1 = BeautifulSoup(page, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    BSR = get_best_sellers_rank(soup2)
    bsr_category = get_bsr_category(soup2)

    category = get_category(soup2)

    product = {
        'name': get_name(soup2),
        'category': category,
        'price': get_price(soup2),
        'ASIN': get_asin(curr_url),
        'reviews': get_reviews(soup2),
        'rating': get_rating(soup2),
        'search': get_search(category, curr_url),
        'url': curr_url,
        'BSR': BSR
    }

    return product
