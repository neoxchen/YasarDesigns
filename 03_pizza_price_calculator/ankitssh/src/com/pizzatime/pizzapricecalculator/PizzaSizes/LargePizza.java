package com.pizzatime.pizzapricecalculator.PizzaSizes;

import com.pizzatime.pizzapricecalculator.IPizza;
import com.pizzatime.pizzapricecalculator.PizzaDecorator;  

public class LargePizza extends PizzaDecorator {
    public LargePizza(IPizza pizza) {
        super(pizza);
    }

    @Override
    public void preparePizza() {
        System.out.println("You've ordered a large pizza");
        super.preparePizza();
    }

    @Override
    public double calculateFinalPrice() {
        return super.calculateFinalPrice() + super.getPriceFromJSONKeys("PizzaSize", "Large");
    }
}
