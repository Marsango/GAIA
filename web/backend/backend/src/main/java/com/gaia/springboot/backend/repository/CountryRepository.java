package com.gaia.springboot.backend.repository;

import com.gaia.springboot.backend.model.Country;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface CountryRepository extends JpaRepository<Country, Long> {
}
