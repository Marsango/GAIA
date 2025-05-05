package com.gaia.springboot.backend.mapper;

import com.gaia.springboot.backend.dto.PersonDto;
import com.gaia.springboot.backend.model.Person;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring",
uses =  AddressMapper.class )
public interface PersonMapper {
    @Mapping( target = "email", source = "requester.email")
    @Mapping( target = "phoneNumber", source = "requester.phoneNumber")
    @Mapping( target = "address", source = "requester.address")
    PersonDto toDto(Person person);
}
