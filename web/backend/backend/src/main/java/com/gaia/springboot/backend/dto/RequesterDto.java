package com.gaia.springboot.backend.dto;

import com.gaia.springboot.backend.model.Address;
import jakarta.persistence.*;

public class RequesterDto {
    private String phoneNumber;
    private String email;
    private Address address;

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Address getAddress() {
        return address;
    }

    public void setAddress(Address address) {
        this.address = address;
    }
}
