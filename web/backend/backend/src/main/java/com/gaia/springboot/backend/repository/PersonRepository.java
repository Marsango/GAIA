package com.gaia.springboot.backend.repository;

import com.gaia.springboot.backend.model.Country;
import com.gaia.springboot.backend.model.Person;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PersonRepository extends JpaRepository<Person, Long> {

}
