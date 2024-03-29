import sys
import subprocess
import os
import json

from CollectingProducts.CollectionServiceBusUtils import get_message_best_seller
from CollectingProducts.CollectionServiceBusUtils import complete_message_best_seller

page_URLs = ["https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing/zgbs/arts-crafts/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Automotive/zgbs/automotive/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Baby/zgbs/baby-products/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Industrial-Scientific/zgbs/industrial/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Musical-Instruments/zgbs/musical-instruments/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Office-Products/zgbs/office-products/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden/zgbs/lawn-garden/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Tools-Home-Improvement/zgbs/hi/ref=zg_bs_nav_0",
             "https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/ref=zg_bs_nav_0"]

for url in page_URLs:
    proc = subprocess.Popen([sys.executable, 'Gandalf.py', 'collect', url])
    proc.wait()

    print(
        "=======================================================run complete=======================================================")
    os.system('sudo service tor reload')

messages_incoming = True
while messages_incoming:
    try:
        message = get_message_best_seller()[0]
        message_json = json.loads(str(message))
        proc = subprocess.Popen([sys.executable, 'Gandalf.py', 'crawl', message_json['url']])
        proc.wait()
        complete_message_best_seller(message)
    except Exception as e:
        print(e)
        messages_incoming = False
