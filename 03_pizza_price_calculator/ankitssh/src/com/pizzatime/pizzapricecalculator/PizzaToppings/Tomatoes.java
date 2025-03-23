package com.pizzatime.pizzapricecalculator.PizzaToppings;

import com.pizzatime.pizzapricecalculator.IPizza;
import com.pizzatime.pizzapricecalculator.PizzaDecorator;  

public class Tomatoes extends PizzaDecorator {
    public Tomatoes(IPizza pizza) {
        super(pizza);
    }

    @Override
    public void preparePizza() {
        System.out.println("You've selected tomatoes toppings");
        super.preparePizza();
    }

    @Override
    public double calculateFinalPrice() {
        return super.calculateFinalPrice() + super.getPriceFromJSONKeys("Toppings", "Tomatoes");
    }
}
