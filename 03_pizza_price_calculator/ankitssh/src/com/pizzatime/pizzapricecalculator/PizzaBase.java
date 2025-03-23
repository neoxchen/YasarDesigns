package com.pizzatime.pizzapricecalculator;
public class PizzaBase implements IPizza {

    @Override
    public void preparePizza() {
        System.out.println("Starting your pizza preparation");
    }

    @Override
    public double calculateFinalPrice() {
        return 10;
    }

}
