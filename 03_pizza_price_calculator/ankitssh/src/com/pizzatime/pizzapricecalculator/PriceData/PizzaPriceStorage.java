package com.pizzatime.pizzapricecalculator.PriceData;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.json.JSONException;
import org.json.JSONObject;

public class PizzaPriceStorage {
    protected JSONObject priceJSON;
    private String fileName = "src/com/pizzatime/pizzapricecalculator/PriceData/PriceConfig.json";
    public PizzaPriceStorage() {
        loadPriceInfo();
    }

    public void loadPriceInfo() {
        try {
            JSONObject jsonObject = parseJSONFile(fileName);
            this.priceJSON = jsonObject;
        } catch (JSONException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private JSONObject parseJSONFile(String filename) throws JSONException, IOException {
        String content = new String(Files.readAllBytes(Paths.get(filename)));
        return new JSONObject(content);
    }

    public JSONObject getPriceJSON() {
        return this.priceJSON;
    }

    public void displayLoadedPrice() {
        System.out.println(priceJSON.toString());
    }
}
