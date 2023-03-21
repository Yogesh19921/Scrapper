from Utilities.Utils import get_page_source
from Utilities.MetadataUtils import *
from CollectingProducts.CollectionServiceBusUtils import get_message
from CollectingProducts.CollectionServiceBusUtils import complete_message
from Utilities.ServiceBusUtils import send_message
from Utilities.CosmosUtils import *
from ScrapingProducts.AmazonRateLimiterException import AmazonRateLimiterException

# Import libraries
from bs4 import BeautifulSoup
import time
import json

AMAZON_ERROR = "Sorry! Something went wrong on our end. Please go back and try again or go to Amazon's home page."


def create_group():
    it = True
    while it:
        try:
            candidate_urls = get_candidate_urls()
            print("===========================Gotten candidate URLS")
            send_candidate_urls(candidate_urls)
        except AmazonRateLimiterException as a:
            print("Amazon probably blocked us. Sleeping for 100 seconds.")
            time.sleep(100)
        except Exception as e:
            print(e)
            print("Some error occurred.")


def send_candidate_urls(candidate_urls):
    for url in candidate_urls:
        data = {
            'url': url
        }
        send_message(json.dumps(data))


def check_if_exists_in_db(asin):
    print("Got this asin:" + asin)
    return validate_item_exists(asin)


def get_candidate_urls():
    message = get_message()[0]
    message_json = json.loads(str(message))
    search_url = message_json['search']
    print(search_url)
    page = get_page_source(search_url)

    if AMAZON_ERROR in page:
        raise AmazonRateLimiterException

    soup1 = BeautifulSoup(page, "html.parser")

    hrefs = soup1.find_all("a",
                           {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

    candidate_urls = []
    for href in hrefs:
        # Filter sponsored content
        if '/gp/slredirect' in href.attrs['href']:
            continue

        print("Getting ASIN from :" + href.attrs['href'])
        # Check if we have already scraped this item by looking in the database
        if not check_if_exists_in_db(get_asin(href.attrs['href'])):
            long_href = href.attrs['href']
            short_href = long_href.split('ref=')[0]
            candidate_urls.append("https://amazon.com" + short_href)

    if len(hrefs) <= 0:
        print("=============No hrefs found.=====================" + search_url)
        text_file = open(message_json['ASIN'], "w")
        text_file.write(page)
        text_file.close()
        raise Exception("No links founds. Amazon probably blocked us")

    complete_message(message)
    return candidate_urls
