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

    @OneToOne
    @JoinColumn(name = "fk_address_id")
    private Address address;

    @Override
    public String toString() {
        return "Requester{" +
                "requesterId=" + requesterId +
                ", phoneNumber='" + phoneNumber + '\'' +
                ", email='" + email + '\'' +
                ", address=" + address +
                '}';
    }

    public Long getRequesterId() {
        return requesterId;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Address getAddress() {
        return address;
    }

    public void setAddress(Address address) {
        this.address = address;
    }
}
