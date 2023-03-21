from CollectingProducts.Collect import program

if __name__ == "__main__":
    products = program()
    print(products)
    print("Total scraped" + str(len(products)))