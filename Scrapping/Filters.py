def add_price_filter(url):
    filter_url = url + "&rh=p_36%3A1600-15000"
    return filter_url


def add_filters(search_url):
    filter_url = add_price_filter(search_url)
    return filter_url
