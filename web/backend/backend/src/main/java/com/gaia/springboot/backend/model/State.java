package com.gaia.springboot.backend.model;
import jakarta.persistence.*;

@Entity
@Table(name = "state", uniqueConstraints = @UniqueConstraint(columnNames = {"state_name", "fk_country_id"}))
public class State {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "state_id")
    private Long stateId;

    @Column(name = "state_name")
    private String stateName;

    @ManyToOne
    @JoinColumn(name = "fk_country_id")
    private Country country;

    public State() {
    }

    public String getStateName() {
        return stateName;
    }

    public void setStateName(String stateName) {
        this.stateName = stateName;
    }

    public Country getCountry() {
        return country;
    }

    public void setCountry(Country country) {
        this.country = country;
    }
}

