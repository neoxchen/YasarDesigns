package com.pizzatime.pizzapricecalculator.PizzaSizes;

import com.pizzatime.pizzapricecalculator.IPizza;
import com.pizzatime.pizzapricecalculator.PizzaDecorator;  

public class SmallPizza extends PizzaDecorator {
    public SmallPizza(IPizza pizza) {
        super(pizza);
    }

    @Override
    public void preparePizza() {
        System.out.println("You've ordered a small pizza");
        super.preparePizza();
    }

    @Override
    public double calculateFinalPrice() {
        return super.calculateFinalPrice() + super.getPriceFromJSONKeys("PizzaSize", "Small");
    }
}
