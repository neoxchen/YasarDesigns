package com.pizzatime.pizzapricecalculator;

public class Discounts {
    private double priceBeforeDiscount;
    private int discountPercent;
    public Discounts(IPizza pizza, int discountPercent) {
        this.priceBeforeDiscount = pizza.calculateFinalPrice();
        this.discountPercent = discountPercent;
    }

    public double applyDiscount() {
        double priceAfterDiscount = priceBeforeDiscount - (priceBeforeDiscount * discountPercent) / 100;
        return priceAfterDiscount;
    }
}
