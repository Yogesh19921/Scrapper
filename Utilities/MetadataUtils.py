from CollectingProducts.Filters import add_filters

import re


def validate_and_throw_exception(attribute, name):
    if attribute is None:
        raise Exception("attribute is None: " + str(name))


def get_name(soup2):
    name = soup2.find("span", {"id": "productTitle"}).text.strip()
    validate_and_throw_exception(name, "name")
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

    validate_and_throw_exception(category, "category")
    return category


def get_asin(url):
    ASIN = None
    pattern = r'/[A-Z0-9][A-Z0-9]{9}/'
    matches = re.findall(pattern, url)

    if len(matches) > 0:
        ASIN = matches[0].replace("/", "")

    validate_and_throw_exception(ASIN, "ASIN")
    return ASIN


def get_price(soup2):
    price = None

    if soup2.find("span", {"class": "a-price-whole"}) is not None:
        price = soup2.find("span", {"class": "a-price-whole"}).text.strip()

        if soup2.find("span", {"class": "a-price-decimal"}) is not None:
            if soup2.find("span", {"class": "a-price-fraction"}) is not None:
                price = price + soup2.find("span", {"class": "a-price-fraction"}).text.strip()

        price = re.sub(" +", "", price)
        price = re.sub("\n", "", price)

    validate_and_throw_exception(price, "price")
    return price


def get_reviews(soup2):
    if soup2.find("span", {"id": "acrCustomerReviewText"}) is not None:
        reviews = soup2.find("span", {"id": "acrCustomerReviewText"}).text.strip()
        reviews = reviews.split(" ")[0]
    else:
        reviews = "NA"

    validate_and_throw_exception(reviews, "reviews")
    return reviews


def get_rating(soup2):
    if soup2.find("span", {"data-hook": "rating-out-of-text"}) is not None:
        rating = soup2.find("span", {"data-hook": "rating-out-of-text"}).text.strip()
        rating = rating.split(" ")[0]
    else:
        rating = "NA"

    validate_and_throw_exception(rating, "rating")
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

    validate_and_throw_exception(search, "search")
    return search


def get_best_sellers_rank(page):
    best_seller_rank = None

    pattern = r'#\d{1,2}\s+in\s+\.*?<?.*?<'
    matches = re.findall(pattern, page)

    if len(matches) > 0:
        best_seller_rank = matches[0].replace('<', '').replace('>', '')

    validate_and_throw_exception(best_seller_rank, "best_seller_rank")
    return best_seller_rank


def get_bsr_category(page):
    bsr_category = None
    try:
        bsr_category = get_best_sellers_rank(page).split("in")[1]
    except Exception as e:
        print(f"couldn't find category")

    validate_and_throw_exception(bsr_category, "bsr_category")
    return bsr_category


def get_product_dimensions(soup2):
    dimensions = "NA"
    rows = soup2.find_all('tr')

    for row in rows:
        if 'Dimensions' in row.text:
            dimensions = row.text.strip().split("\n")[-1].strip()
            break

    if dimensions is None:
        rows = soup2.find_all('li')
        for row in rows:
            if 'Dimensions' in row.text:
                dimensions = row.text.strip().split("\n")[-1].strip()
                break;
    #validate_and_throw_exception(dimensions, "dimensions")
    return dimensions
