package com.gaia.springboot.backend.model;
import jakarta.persistence.*;

@Entity
@Table(name = "street", uniqueConstraints = @UniqueConstraint(columnNames = {"street_name", "fk_city_id"}))
public class Street {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "street_id")
    private Long streetId;

    @Column(name = "street_name")
    private String streetName;

    @ManyToOne
    @JoinColumn(name = "fk_city_id")
    private City city;

    public Street(){

    }

    public String getStreetName() {
        return streetName;
    }

    public void setStreetName(String streetName) {
        this.streetName = streetName;
    }

    public City getCity() {
        return city;
    }

    public void setCity(City city) {
        this.city = city;
    }
}
