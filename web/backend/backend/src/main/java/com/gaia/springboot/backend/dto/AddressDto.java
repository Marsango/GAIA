package com.gaia.springboot.backend.dto;

import com.gaia.springboot.backend.model.City;
import com.gaia.springboot.backend.model.Country;
import com.gaia.springboot.backend.model.State;
import com.gaia.springboot.backend.model.Street;

public class AddressDto {
    private String cep;
    private String addressNumber;
    private String country;
    private String state;
    private String city;
    private String street;

    public String getCep() {
        return cep;
    }

    public void setCep(String cep) {
        this.cep = cep;
    }

    public String getAddressNumber() {
        return addressNumber;
    }

    public void setAddressNumber(String addressNumber) {
        this.addressNumber = addressNumber;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public String getStreet() {
        return street;
    }

    public void setStreet(String street) {
        this.street = street;
    }
}
