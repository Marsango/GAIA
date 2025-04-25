package com.gaia.springboot.backend.model;
import jakarta.persistence.*;

@Entity
@Table(name = "requester")
public class Requester {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "requester_id")
    private Long requesterId;

    @Column(name = "phone_number")
    private String phoneNumber;

    @Column(name = "email")
    private String email;

    @ManyToOne
    @JoinColumn(name = "fk_address_id")
    private Address address;
}
