from ScrapingProducts.Scrap import program
from multiprocessing import Process
import os


if __name__ == "__main__":
    while True:
        processes = []

        for i in range(3):
            p = Process(target=program, args=(i, ))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        # Change ip for next request
        os.system('sudo service tor reload')