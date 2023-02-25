from Scrapping.Scrap import program
from Grouping.CreateGroup import create_group

if __name__ == "__main__":
    products = program()
    print(products)
    for product in products:
        create_group(product['search'])