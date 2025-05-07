package com.gaia.springboot.backend.repository;

import com.gaia.springboot.backend.model.City;
import com.gaia.springboot.backend.model.Country;
import com.gaia.springboot.backend.model.State;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CityRepository extends JpaRepository<City, Long> {
    City findOneByStateAndCityName(State state, String cityName);
}
