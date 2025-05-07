package com.gaia.springboot.backend.model;
import jakarta.persistence.*;

@Entity
@Table(name = "address")
public class Address {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "address_id")
    private Long addressId;

    @Column(name = "cep")
    private String cep;

    @Column(name = "address_number")
    private String addressNumber;

    @ManyToOne
    @JoinColumn(name = "fk_country_id")
    private Country country;

    @ManyToOne
    @JoinColumn(name = "fk_state_id")
    private State state;

    @ManyToOne
    @JoinColumn(name = "fk_city_id")
    private City city;

    @ManyToOne
    @JoinColumn(name = "fk_street_id")
    private Street street;

    protected Address(){

    }

    public Address(String cep, String addressNumber, Country country, State state, City city, Street street) {
        this.cep = cep;
        this.addressNumber = addressNumber;
        this.country = country;
        this.state = state;
        this.city = city;
        this.street = street;
    }

    public Long getAddressId() {
        return addressId;
    }

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

    public Country getCountry() {
        return country;
    }

    public void setCountry(Country country) {
        this.country = country;
    }

    public State getState() {
        return state;
    }

    public void setState(State state) {
        this.state = state;
    }

    public City getCity() {
        return city;
    }

    public void setCity(City city) {
        this.city = city;
    }

    public Street getStreet() {
        return street;
    }

    public void setStreet(Street street) {
        this.street = street;
    }
}
