package com.pizzatime.pizzapricecalculator;

import com.pizzatime.pizzapricecalculator.PriceData.PizzaPriceStorage;

public class PizzaDecorator implements IPizza {
    protected IPizza pizza;
    protected static PizzaPriceStorage pizzaPriceStorage = new PizzaPriceStorage();
    public PizzaDecorator(IPizza pizza) {
        this.pizza = pizza;
    }

    @Override
    public void preparePizza() {
        pizza.preparePizza();
    }

    @Override
    public double calculateFinalPrice() {
        return pizza.calculateFinalPrice();
    }

    protected double getPriceFromJSONKeys(String attr1, String attr2) {
        return pizzaPriceStorage.getPriceJSON().getJSONObject(attr1).getDouble(attr2);
    }
}
