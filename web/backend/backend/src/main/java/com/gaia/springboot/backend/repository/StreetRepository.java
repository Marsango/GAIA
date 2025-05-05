package com.gaia.springboot.backend.repository;

import com.gaia.springboot.backend.model.Street;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StreetRepository extends JpaRepository<Street, Long> {

}
