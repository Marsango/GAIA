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

    protected State() {
    }

    public State(String stateName, Country country) {
        this.stateName = stateName;
        this.country = country;
    }

    public Long getStateId() {
        return stateId;
    }

    public String getStateName() {
        return stateName;
    }


    public Country getCountry() {
        return country;
    }

}

