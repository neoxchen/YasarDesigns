package com.pizzatime.pizzapricecalculator;

import com.pizzatime.pizzapricecalculator.PizzaCrust.RegularCrust;
import com.pizzatime.pizzapricecalculator.PizzaSizes.LargePizza;
import com.pizzatime.pizzapricecalculator.PizzaToppings.Olives;
import com.pizzatime.pizzapricecalculator.PizzaToppings.Tomatoes;

public class App {
    public static void main(String[] args) throws Exception {
        PizzaBase pizzaBase = new PizzaBase();

        IPizza pizza = new LargePizza(new RegularCrust(new Olives(new Tomatoes(pizzaBase))));

        pizza.preparePizza();
        Discounts discount = new Discounts(pizza, 10);
        System.out.println("Price before discounts : " + Double.toString(pizza.calculateFinalPrice()));
        System.out.println(discount.applyDiscount());

    }
}
