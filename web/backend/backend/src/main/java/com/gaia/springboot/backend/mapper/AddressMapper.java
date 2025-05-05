package com.gaia.springboot.backend.mapper;

import com.gaia.springboot.backend.dto.AddressDto;
import com.gaia.springboot.backend.model.Address;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface AddressMapper {

    @Mapping(source = "country.countryName", target = "country")
    @Mapping(source = "state.stateName",   target = "state")
    @Mapping(source = "city.cityName",    target = "city")
    @Mapping(source = "street.streetName", target = "street")
    AddressDto toDto(Address address);
}