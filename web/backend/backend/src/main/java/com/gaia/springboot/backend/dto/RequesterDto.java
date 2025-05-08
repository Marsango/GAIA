package com.gaia.springboot.backend.dto;

import com.gaia.springboot.backend.model.Address;
import jakarta.persistence.*;

public class RequesterDto {
    private String phoneNumber;
    private String email;
    private AddressDto address;

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

    public AddressDto getAddress() {
        return address;
    }

    public void setAddress(AddressDto address) {
        this.address = address;
    }
}
