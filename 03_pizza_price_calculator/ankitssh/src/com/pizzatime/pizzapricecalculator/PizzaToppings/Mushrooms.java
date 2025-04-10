package com.pizzatime.pizzapricecalculator.PizzaToppings;

import com.pizzatime.pizzapricecalculator.IPizza;
import com.pizzatime.pizzapricecalculator.PizzaDecorator;  

public class Mushrooms extends PizzaDecorator {
    public Mushrooms(IPizza pizza) {
        super(pizza);
    }

    @Override
    public void preparePizza() {
        System.out.println("You've selected mushroom toppings");
        super.preparePizza();
    }

    @Override
    public double calculateFinalPrice() {
        return super.calculateFinalPrice() + super.getPriceFromJSONKeys("Toppings", "Mushrooms");
    }
}
