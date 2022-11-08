import os
from threading import Thread
import pandas as pd
import keyboard
import time
from order import Order

# windows terminal clearing
clear = lambda: os.system("cls")


def display_orders():
    while True:
        try:
            if keyboard.is_pressed("q"):
                clear()
                print("Quiting...")
                break
        except:
            pass
        clear()
        print("##### Order list: #####")
        Order.display()
        print("Press q to quit.")
        time.sleep(1)


def simulate_orders():
    Order("001", "Buy", "Add", 20.0, 100)
    time.sleep(2)
    Order("002", "Sell", "Add", 25.0, 200)
    time.sleep(3)
    Order("003", "Buy", "Add", 23.0, 50)
    time.sleep(1)
    Order("004", "Buy", "Add", 23.0, 70)
    time.sleep(5)
    Order("003", "Buy", "Remove", 23.0, 50)
    time.sleep(8)
    Order("005", "Sell", "Add", 28, 50)


if __name__ == "__main__":
    t1 = Thread(target=display_orders)
    t2 = Thread(target=simulate_orders)

    t2.start()
    t1.start()

    t1.join()
    t2.join()

    print("Q.")
