from bs4 import BeautifulSoup
from crawl1 import crawlItem
import csv
from concurrent.futures import ThreadPoolExecutor
# selenium 4
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions

options = EdgeOptions()
options.headless = True
options.add_argument("--window-size=1920,1080")
driver = webdriver.Edge(options=options, service=EdgeService(EdgeChromiumDriverManager().install()))

#driver.get('https://www.amazon.com/Best-Sellers-Home-Art-Supplies/zgbs/kitchen')
driver.get('https://www.amazon.com/gp/new-releases/home-garden')
total_height = int(driver.execute_script("return document.body.scrollHeight"))
for i in range(1, total_height, 10):
    driver.execute_script("window.scrollTo(0, {});".format(i))

content = driver.page_source

driver.quit()

soup1 = BeautifulSoup(content, "html.parser")
soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
subject_urls = soup1.find_all("a", {"class": "a-link-normal", "tabindex": "-1", "role": "link"})

print(len(subject_urls))
urls = set()
products = []
count = 0

"""
for item in subject_urls:
    if (count == 1):
        break
    #curr_url = "https://amazon.ca" + item.attrs['href']
    #urls.add(curr_url)
    product = crawlItem(item)
    products.append(product)
    count = count + 1
"""

with ThreadPoolExecutor() as executor:
    for product in executor.map(crawlItem, subject_urls):
        products.append(product)

    print("waiting ...")

with open('prod.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'category', 'price', 'ASIN', 'BSR', 'reviews', 'rating', 'search', 'url'])
    #writer = csv.DictWriter(f, fieldnames=['search', 'url'])
    for p in products:
        writer.writerow(p)
