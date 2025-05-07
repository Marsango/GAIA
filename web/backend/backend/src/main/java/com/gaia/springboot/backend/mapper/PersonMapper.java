package com.gaia.springboot.backend.mapper;

import com.gaia.springboot.backend.dto.AddressDto;
import com.gaia.springboot.backend.dto.PersonDto;
import com.gaia.springboot.backend.model.*;
import com.gaia.springboot.backend.repository.CityRepository;
import com.gaia.springboot.backend.repository.CountryRepository;
import com.gaia.springboot.backend.repository.StateRepository;
import com.gaia.springboot.backend.repository.StreetRepository;
import com.gaia.springboot.backend.service.AddressResolver;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.Named;

@Mapper(componentModel = "spring",
uses =  {AddressResolver.class, AddressMapper.class} )
public interface PersonMapper {
    @Mapping( target = "email", source = "requester.email")
    @Mapping( target = "phoneNumber", source = "requester.phoneNumber")
    @Mapping( target = "address", source = "requester.address")
    PersonDto toDto(Person person);

    @Mapping( target = "requester.email", source = "email")
    @Mapping( target = "requester.phoneNumber", source = "phoneNumber")
    @Mapping( target = "requester.address", source = "address", qualifiedByName = "resolve")
    Person dtoToPerson(PersonDto personDto);
}
