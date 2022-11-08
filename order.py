from pathlib import Path
import pandas as pd
import csv


class Order:
    orders = list()
    filename = "orders.csv"

    def __init__(
        self,
        id: str,
        order: str,
        o_type: str,
        price: float,
        quantity: int,
        init_from_file=False,
    ):
        self.__id = id
        self.__order = order
        self.__o_type = o_type
        self.__price = price
        self.__quantity = quantity
        Order.orders.append(self)

        # if file is already created - load file and add new record, if there is no file
        # create one and save the record.
        file = Path("./orders.csv")
        if init_from_file:
            # if initializing happens from file
            # Don't do anything
            pass
        elif file.is_file():
            if not self.orders:
                # If there is the file and there is no orders in memory, initialize
                # orders form the file.
                self.load_from_csv()
            self.add_record()
        else:
            self.save()

    @property
    def id(self):
        return self.__id

    @property
    def order(self):
        return self.__order

    @property
    def o_type(self):
        return self.__o_type

    @property
    def price(self):
        return self.__price

    @property
    def quantity(self):
        return self.__quantity

    @id.setter
    def id(self, new_id):
        if isinstance(new_id, str):
            raise TypeError("Id attribute should be of the type str.")
        self.__id = new_id

    @order.setter
    def order(self, new_order):
        allowed = ("Buy", "Sell")
        if isinstance(new_order, str):
            raise TypeError("Order attribute should be of the type str.")
        if new_order not in allowed:
            raise ValueError("Only Buy/Sell orders are allowed.")
        self.__order = new_order

    @o_type.setter
    def o_type(self, new_o_type):
        allowed = ("Add", "Remove")
        if isinstance(new_o_type, str):
            raise TypeError("Type attribute should be of the type str.")
        if new_o_type not in allowed:
            raise ValueError("Only Add/Remove types of order are allowed.")
        self.__o_type = new_o_type

    @price.setter
    def price(self, new_price):
        if isinstance(new_price, float):
            raise TypeError("Type attribute should be of the type float.")
        self.__price = new_price

    @quantity.setter
    def quantity(self, new_quantity):
        if isinstance(new_quantity, int):
            raise TypeError("Type attribute should be of the type float.")
        self.__quantity = new_quantity

    def get_dict(self):
        """Return dictionary representation of an order"""
        return {
            "Id": self.id,
            "Order": self.order,
            "Type": self.o_type,
            "Price": self.price,
            "Quantity": self.quantity,
        }

    def add_record(self):
        """Add record to the existing csv file."""
        header = ["Id", "Order", "Type", "Price", "Quantity"]
        with open(self.filename, "a") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writerow(self.get_dict())

    @classmethod
    def save(cls):
        """Save all instances to csv file"""
        header = ["Id", "Order", "Type", "Price", "Quantity"]
        with open(cls.filename, "w") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            writer.writerows(cls._get_dict_list())

    @classmethod
    def load_from_csv(cls):
        """Load orders from cls file"""
        with open(cls.filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cls(
                    row["Id"],
                    row["Order"],
                    row["Type"],
                    float(row["Price"]),
                    int(row["Quantity"]),
                    init_from_file=True,
                )

    @classmethod
    def _get_dict_list(cls):
        l_dict = list()
        for order in cls.orders:
            l_dict.append(order.get_dict())
        return l_dict

    @classmethod
    def display(cls):
        """Display frame of orders."""
        cls.orders.sort(key=lambda x: x.price)
        d = pd.DataFrame.from_records([o.get_dict() for o in cls.orders])
        print(d)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.order}, {self.o_type}, {self.price},"
            f"{self.quantity})"
        )

    def __str__(self):
        return f"{self.order} {self.o_type} {self.price} {self.quantity}"
