import time
from typing import *

from pizza import Pizza


class ShoppingCart:
    def __init__(self):
        self.pizzas: List[Pizza] = []
        self.coupons: List[Coupon] = []

    def add_pizza(self, pizza: Pizza):
        self.pizzas.append(pizza)

    def remove_pizza(self, pizza: Pizza):
        self.pizzas.remove(pizza)

    def add_coupon(self, coupon: "Coupon"):
        self.coupons.append(coupon)

    def remove_coupon(self, coupon: "Coupon"):
        self.coupons.remove(coupon)

    def calculate_price(self) -> float:
        pass


class EntireOrderCoupon:
    """ X% off entire order """

    def __init__(self, discount: float):
        # Discount is a float between 0 and 1
        self.discount = discount

    def calculate_price(self, subtotal: float) -> float:
        return subtotal * self.discount


class ItemCoupon:
    """
    Coupon types:
    - buy [X, ...] get [Y, ...] free
    - buy [X, ...] get [Y, ...] with $Z% discount
    - $X% off when buying [X, Y, ...]
    """

    def __init__(self):
        self.related_items: List[Pizza] = []

    def calculate_price(self) -> float:
        raise NotImplementedError


class ItemDiscountCoupon:
    """ $X% off when buying [X, Y, ...] """

    def __init__(self, name: str, condition: Callable[[ShoppingCart], bool], discount: float, valid_until: int):
        self.name = name
        self.condition = condition
        self.discount: float = discount
        self.valid_until: int = valid_until

    def apply(self, price: float) -> float:
        return price * (1 - self.discount)

    def __repr__(self):
        return f"Coupon(name='{self.name}', discount={self.discount}, valid_until={self.valid_until})"


if __name__ == "__main__":
    my_coupon: Coupon = Coupon("10% off", lambda cart: True, 0.1, int(time.time()) + 3600)
    print(my_coupon)

    cart: ShoppingCart = ShoppingCart()
