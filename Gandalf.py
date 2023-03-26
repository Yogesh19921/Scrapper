from CollectingProducts.Collect import program
import sys

if __name__ == "__main__":
    url = sys.argv[1]
    products = program(url)
    print(products)
    print("Total scraped" + str(len(products)))