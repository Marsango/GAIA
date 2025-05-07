package com.gaia.springboot.backend.model;
import jakarta.persistence.*;

@Entity
@Table(name = "city", uniqueConstraints = @UniqueConstraint(columnNames = {"city_name", "fk_state_id"}))
public class City {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "city_id")
    private Long cityId;

    @Column(name = "city_name")
    private String cityName;

    @ManyToOne
    @JoinColumn(name = "fk_state_id")
    private State state;

    protected City(){

    }

    public City(String cityName, State state) {
        this.cityName = cityName;
        this.state = state;
    }

    public Long getCityId() {
        return cityId;
    }

    public String getCityName() {
        return cityName;
    }


    public State getState() {
        return state;
    }


}
