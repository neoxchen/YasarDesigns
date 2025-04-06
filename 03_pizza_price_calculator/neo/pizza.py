from enum import Enum
from typing import *

"""
Low-Level Design (LLD) Problem: Pizza Price Calculator
Problem Statement:

Design a system to calculate the price of a pizza based on different parameters such as size, toppings, crust type, and discounts. The system should allow dynamic configurations for pricing rules.
Requirements
Functional Requirements:

    Select Pizza Size – The user should be able to choose a size (e.g., Small, Medium, Large).
    Choose Crust Type – Options should include Regular, Thin Crust, and Stuffed Crust.
    Add Toppings – Users can add multiple toppings (e.g., Mushrooms, Pepperoni, Extra Cheese).
    Calculate Final Price – The system should calculate the final price based on selected parameters.
    Apply Discounts – The system should support percentage-based and fixed amount discounts.
    Tax Calculation – The system should add tax based on location.
    Dynamic Pricing Rules – The system should allow price updates without code changes.

Non-Functional Requirements:

    Scalability – The design should accommodate future additions (e.g., more pizza sizes, toppings).
    Extensibility – The system should allow new pricing rules or special offers without major code changes.
    Performance – The pricing calculation should be optimized for quick response.

Constraints:

    The system should be object-oriented, following SOLID principles.
    The pricing configuration should be easily maintainable (e.g., from a database or config file).
    The pricing model should allow multiple promotions to be applied together.
"""


class PizzaComponent:
    def __init__(self, name: str, price: float, mandatory: bool = False):
        self.name: str = name
        self.price: float = price
        self.mandatory: bool = mandatory


# ===========================
class PizzaSize:
    """ Denotes the size of the pizza, has multiplier on top of the final price """

    def __init__(self, name: str, price_multiplier: float):
        self.name = name
        self.price_multiplier = price_multiplier

    def __repr__(self):
        return f"PizzaSize(name={self.name}, multiplier={self.price_multiplier})"


class PizzaSizes(Enum):
    SMALL: PizzaSize = PizzaSize("Small", 0.5)
    MEDIUM: PizzaSize = PizzaSize("Medium", 0.8)
    LARGE: PizzaSize = PizzaSize("Large", 1)
    EXTRA_LARGE: PizzaSize = PizzaSize("Extra Large", 1.5)


# ===========================
class PizzaCrust(PizzaComponent):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, True)
        self.name: str = name
        self.price: float = price

    def __repr__(self):
        return f"PizzaCrust(name={self.name}, price={self.price})"


class PizzaCrusts(Enum):
    REGULAR: PizzaCrust = PizzaCrust("Regular", 8)
    THIN: PizzaCrust = PizzaCrust("Thin", 8)
    STUFFED: PizzaCrust = PizzaCrust("Stuffed", 10)


# ===========================
class PizzaSauce(PizzaComponent):
    """ It's not mandatory to have a sauce on the pizza """

    def __init__(self, name: str, price: float):
        super().__init__(name, price, False)
        self.name: str = name
        self.price: float = price

    def __repr__(self):
        return f"PizzaSauce(name={self.name}, price={self.price})"


class PizzaSauces(Enum):
    MARINARA: PizzaSauce = PizzaSauce("Marinara", 1)
    ALFREDO: PizzaSauce = PizzaSauce("Alfredo", 1)
    PESTO: PizzaSauce = PizzaSauce("Pesto", 2)


# ===========================
class PizzaTopping(PizzaComponent):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, False)
        self.name: str = name
        self.price: float = price

    def __repr__(self):
        return f"PizzaTopping(name={self.name}, price={self.price})"


class PizzaToppings(Enum):
    # Veggies
    MUSHROOM: PizzaTopping = PizzaTopping("Mushroom", 2)
    BELL_PEPPER: PizzaTopping = PizzaTopping("Bell Pepper", 1.5)
    ONION: PizzaTopping = PizzaTopping("Onion", 1.5)

    # Meats
    PEPPERONI: PizzaTopping = PizzaTopping("Pepperoni", 2.5)
    SAUSAGE: PizzaTopping = PizzaTopping("Sausage", 3)
    CHICKEN: PizzaTopping = PizzaTopping("Chicken", 2)

    # Extra cheeses
    MOZZARELLA: PizzaTopping = PizzaTopping("Mozzarella", 2)
    CHEDDAR: PizzaTopping = PizzaTopping("Cheddar", 2)
    FETA: PizzaTopping = PizzaTopping("Feta", 2)


# ===========================
class Pizza:
    def __init__(self, size: PizzaSize, components: List[PizzaComponent]):
        self.size: PizzaSize = size
        self.components: List[PizzaComponent] = components

    def calculate_price(self) -> float:
        price: float = 0
        for component in self.components:
            price += component.price
        return price

    def __repr__(self):
        return f"Pizza(size={self.size.name}, price={self.calculate_price()}, components={self.components})"


class PizzaBuilder:
    def __init__(self, size: PizzaSize):
        self.size: PizzaSize = size
        self.components: List[PizzaComponent] = []

    def with_crust(self, crust: PizzaCrust):
        self.components.append(crust)
        return self

    def with_sauce(self, sauce: PizzaSauce):
        self.components.append(sauce)
        return self

    def with_toppings(self, *args: PizzaTopping):
        for topping in args:
            self.components.append(topping)
        return self

    def build(self) -> Pizza:
        return Pizza(self.size, self.components)
