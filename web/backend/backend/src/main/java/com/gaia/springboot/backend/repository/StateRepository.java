package com.gaia.springboot.backend.repository;

import com.gaia.springboot.backend.model.State;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StateRepository extends JpaRepository<State, Long> {
}
