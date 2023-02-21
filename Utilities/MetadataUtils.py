from Scrapping.Filters import add_filters

import re


def get_name(soup2):
    name = soup2.find("span", {"id": "productTitle"}).text.strip()
    return name


def get_category(soup2):
    category = None

    # Try to find category from Amazon tree
    if soup2.find("ul", {"class", "a-unordered-list a-horizontal a-size-small"}) is not None:
        category = soup2.find("ul", {"class", "a-unordered-list a-horizontal a-size-small"}).findChildren("li")[
            -1].text.strip()

    if category is not None:
        return category

    bsr_category = get_bsr_category(soup2)

    # Category tree is not present.
    if bsr_category is None:
        if soup2.find("span", {"class", "cat-link"}) is not None:
            category = soup2.find("span", {"class", "cat-link"}).text.strip()

        if soup2.find("span", {"class": "ac-keyword-link"}) is not None:
            category = soup2.find("span", {"class": "ac-keyword-link"}).text.strip()

        if soup2.find("span", {"class": "ac-for-text"}) is not None:
            category = soup2.find("span", {"class": "ac-for-text"}).text.strip()
    else:
        category = bsr_category

    return category


def get_asin(curr_url):
    ASIN = re.search(r'/[dg]p/([^/]+)', curr_url, flags=re.IGNORECASE).group(1)
    return ASIN


def get_price(soup2):
    if soup2.find("span", {"class": "a-offscreen"}) is not None:
        price = soup2.find("span", {"class": "a-offscreen"}).text.strip()
    else:
        price = "NA"

    return price


def get_reviews(soup2):
    if soup2.find("span", {"id": "acrCustomerReviewText"}) is not None:
        reviews = soup2.find("span", {"id": "acrCustomerReviewText"}).text.strip()
    else:
        reviews = "NA"

    return reviews


def get_rating(soup2):
    if soup2.find("span", {"data-hook": "rating-out-of-text"}) is not None:
        rating = soup2.find("span", {"data-hook": "rating-out-of-text"}).text.strip()
    else:
        rating = "NA"

    return rating


def get_search(category, curr_url):
    if category is None:
        print(f'category not found for {curr_url}')
        search = "NA"
    else:
        category = category.split("by ")[0]
        category = category.split("in ")[-1]
        search = 'https://amazon.com/s?k=' + category.replace(' ', '+')

    search = add_filters(search)

    return search


def get_best_sellers_rank(soup2):
    rows = soup2.find_all('tr')
    best_seller_rank = None

    for row in rows:
        if 'Best Sellers Rank' in row.text:
            best_seller_rank = row.text.replace("\n", "").strip()
            best_seller_rank = best_seller_rank.split("Best Sellers Rank")[-1]
            best_seller_rank = re.sub(" +", " ", best_seller_rank)
            best_seller_rank = best_seller_rank.replace("#", "\n")
            break

    return best_seller_rank


def get_bsr_category(soup2):
    bsr_category = None
    try:
        bsr_category = get_best_sellers_rank(soup2).split("\n")[-1].split(" in ")[-1]
    except:
        print(f"couldn't find category here for {get_name(soup2)}")

    return bsr_category

def get_product_dimensions(soup2):
    dimensions = None
    rows = soup2.find_all('tr')

    for row in rows:
        if 'Dimensions' in row.text:
            dimensions = row.text.strip().split("\n")[-1].strip()
            #print(dimensions)
            break

    return dimensions

