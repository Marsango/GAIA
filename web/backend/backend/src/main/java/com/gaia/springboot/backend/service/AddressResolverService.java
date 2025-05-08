package com.gaia.springboot.backend.service;

import com.gaia.springboot.backend.dto.AddressDto;
import com.gaia.springboot.backend.model.Address;
import com.gaia.springboot.backend.model.Country;
import com.gaia.springboot.backend.model.State;
import com.gaia.springboot.backend.model.City;
import com.gaia.springboot.backend.model.Street;
import com.gaia.springboot.backend.repository.CityRepository;
import com.gaia.springboot.backend.repository.CountryRepository;
import com.gaia.springboot.backend.repository.StateRepository;
import com.gaia.springboot.backend.repository.StreetRepository;
import org.mapstruct.Named;
import org.springframework.stereotype.Component;

@Component
public class AddressResolverService {

    private final CountryRepository countryRepo;
    private final StateRepository stateRepo;
    private final CityRepository cityRepo;
    private final StreetRepository streetRepo;

    public AddressResolverService(CountryRepository countryRepo,
                                  StateRepository stateRepo,
                                  CityRepository cityRepo,
                                  StreetRepository streetRepo) {
        this.countryRepo = countryRepo;
        this.stateRepo   = stateRepo;
        this.cityRepo    = cityRepo;
        this.streetRepo  = streetRepo;
    }

    @Named("resolve")
    public Address resolve(AddressDto dto) {

        Country country = countryRepo.findOneByCountryName(dto.getCountry());
        if (country == null) {
            country = new Country(dto.getCountry());
            countryRepo.save(country);
        }

        State state = stateRepo.findOneByCountryAndStateName(country, dto.getState());
        if (state == null){
            state = new State(dto.getState(), country);
            stateRepo.save(state);
        }

        City city = cityRepo.findOneByStateAndCityName(state, dto.getCity());
        if (city == null){
            city = new City(dto.getCity(), state);
            cityRepo.save(city);
        }

        Street street = streetRepo.findOneByCityAndStreetName(city, dto.getStreet());
        if (street == null){
            street = new Street(dto.getStreet(), city);
            streetRepo.save(street);
        }
        return new Address(dto.getCep(), dto.getAddressNumber(), country, state, city, street);
    }

    public void updateAddress(Address address, AddressDto dto) {
        Country country = countryRepo.findOneByCountryName(dto.getCountry());
        if (country == null) {
            country = new Country(dto.getCountry());
            countryRepo.save(country);
        }

        State state = stateRepo.findOneByCountryAndStateName(country, dto.getState());
        if (state == null){
            state = new State(dto.getState(), country);
            stateRepo.save(state);
        }

        City city = cityRepo.findOneByStateAndCityName(state, dto.getCity());
        if (city == null){
            city = new City(dto.getCity(), state);
            cityRepo.save(city);
        }

        Street street = streetRepo.findOneByCityAndStreetName(city, dto.getStreet());
        if (street == null){
            street = new Street(dto.getStreet(), city);
            streetRepo.save(street);
        }
        address.setCountry(country);
        address.setState(state);
        address.setCity(city);
        address.setStreet(street);
        address.setCep(dto.getCep());
        address.setAddressNumber(dto.getAddressNumber());
    }

}
