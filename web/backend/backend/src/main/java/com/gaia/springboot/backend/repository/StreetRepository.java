package com.gaia.springboot.backend.repository;

import com.gaia.springboot.backend.model.City;
import com.gaia.springboot.backend.model.State;
import com.gaia.springboot.backend.model.Street;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StreetRepository extends JpaRepository<Street, Long> {
    Street findOneByCityAndStreetName(City city, String streetName);
}
