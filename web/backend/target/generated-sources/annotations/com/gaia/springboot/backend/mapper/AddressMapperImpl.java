package com.gaia.springboot.backend.mapper;

import com.gaia.springboot.backend.dto.AddressDto;
import com.gaia.springboot.backend.model.Address;
import com.gaia.springboot.backend.model.City;
import com.gaia.springboot.backend.model.Country;
import com.gaia.springboot.backend.model.State;
import com.gaia.springboot.backend.model.Street;
import javax.annotation.Generated;
import org.springframework.stereotype.Component;

@Generated(
    value = "org.mapstruct.ap.MappingProcessor",
    date = "2025-05-06T17:20:12-0300",
    comments = "version: 1.6.3, compiler: javac, environment: Java 24.0.1 (Oracle Corporation)"
)
@Component
public class AddressMapperImpl implements AddressMapper {

    @Override
    public AddressDto toDto(Address address) {
        if ( address == null ) {
            return null;
        }

        AddressDto addressDto = new AddressDto();

        addressDto.setCountry( addressCountryCountryName( address ) );
        addressDto.setState( addressStateStateName( address ) );
        addressDto.setCity( addressCityCityName( address ) );
        addressDto.setStreet( addressStreetStreetName( address ) );
        addressDto.setCep( address.getCep() );
        addressDto.setAddressNumber( address.getAddressNumber() );

        return addressDto;
    }

    private String addressCountryCountryName(Address address) {
        Country country = address.getCountry();
        if ( country == null ) {
            return null;
        }
        return country.getCountryName();
    }

    private String addressStateStateName(Address address) {
        State state = address.getState();
        if ( state == null ) {
            return null;
        }
        return state.getStateName();
    }

    private String addressCityCityName(Address address) {
        City city = address.getCity();
        if ( city == null ) {
            return null;
        }
        return city.getCityName();
    }

    private String addressStreetStreetName(Address address) {
        Street street = address.getStreet();
        if ( street == null ) {
            return null;
        }
        return street.getStreetName();
    }
}
