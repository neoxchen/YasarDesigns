from pizza import *

if __name__ == "__main__":
    pizza: Pizza = (PizzaBuilder(PizzaSizes.LARGE.value)
                    .with_crust(PizzaCrusts.STUFFED.value)
                    .with_sauce(PizzaSauces.PESTO.value)
                    .with_toppings(PizzaToppings.MUSHROOM.value, PizzaToppings.ONION.value)
                    .build())
    print(pizza)