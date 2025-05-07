package com.gaia.springboot.backend.model;

import jakarta.persistence.*;

@Entity
@Table(name = "country")
public class Country {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "country_id")
    private Long countryId;

    @Column(name = "country_name", unique = true)
    private String countryName;

    protected Country(){

    }


    public Country(String countryName){
        this.countryName = countryName;
    }

    @Override
    public String toString() {
        return "Country{" +
                "countryId=" + countryId +
                ", countryName='" + countryName + '\'' +
                '}';
    }

    public Long getCountryId() {
        return countryId;
    }

    public String getCountryName() {
        return countryName;
    }

}

