package com.gaia.springboot.backend.repository;

import com.gaia.springboot.backend.model.City;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CityRepository extends JpaRepository<City, Long> {
}
