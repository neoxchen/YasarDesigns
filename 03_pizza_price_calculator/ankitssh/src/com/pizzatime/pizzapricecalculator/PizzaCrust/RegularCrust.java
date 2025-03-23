package com.pizzatime.pizzapricecalculator.PizzaCrust;

import com.pizzatime.pizzapricecalculator.IPizza;
import com.pizzatime.pizzapricecalculator.PizzaDecorator;  

public class RegularCrust extends PizzaDecorator {
    public RegularCrust(IPizza pizza) {
        super(pizza);
    }

    @Override
    public void preparePizza() {
        System.out.println("You've chosen a regular crust");
        super.preparePizza();
    }

    @Override
    public double calculateFinalPrice() {
        return super.calculateFinalPrice() + super.getPriceFromJSONKeys("CrustType", "Regular");
    }
}
