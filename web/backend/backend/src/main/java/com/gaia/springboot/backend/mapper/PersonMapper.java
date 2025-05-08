package com.gaia.springboot.backend.mapper;

import com.gaia.springboot.backend.dto.PersonDto;
import com.gaia.springboot.backend.model.*;
import com.gaia.springboot.backend.service.AddressResolverService;
import org.mapstruct.*;

import java.util.Optional;

@Mapper(componentModel = "spring",
uses =  {AddressResolverService.class, AddressMapper.class}
)
public interface PersonMapper {
    @Mapping( target = "email", source = "requester.email")
    @Mapping( target = "phoneNumber", source = "requester.phoneNumber")
    @Mapping( target = "address", source = "requester.address")
    PersonDto toDto(Person person);

    @Mapping( target = "requester.email", source = "email")
    @Mapping( target = "requester.phoneNumber", source = "phoneNumber")
    @Mapping( target = "requester.address", source = "address", qualifiedByName = "resolve")
    Person dtoToPerson(PersonDto personDto);

    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    void updatePersonFromDto(PersonDto personDto, @MappingTarget Person person, @Context AddressResolverService addressService);

    @AfterMapping
    default void afterUpdatePerson(PersonDto personDto, @MappingTarget Person person, @Context AddressResolverService addressService){
        person.getRequester().setEmail(personDto.getEmail());
        person.getRequester().setPhoneNumber(personDto.getPhoneNumber());
        addressService.updateAddress(person.getRequester().getAddress(), personDto.getAddress());
    }
}
