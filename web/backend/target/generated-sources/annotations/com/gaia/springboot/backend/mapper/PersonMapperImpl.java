package com.gaia.springboot.backend.mapper;

import com.gaia.springboot.backend.dto.PersonDto;
import com.gaia.springboot.backend.model.Address;
import com.gaia.springboot.backend.model.Person;
import com.gaia.springboot.backend.model.Requester;
import com.gaia.springboot.backend.service.AddressResolver;
import javax.annotation.Generated;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Generated(
    value = "org.mapstruct.ap.MappingProcessor",
    date = "2025-05-06T17:20:12-0300",
    comments = "version: 1.6.3, compiler: javac, environment: Java 24.0.1 (Oracle Corporation)"
)
@Component
public class PersonMapperImpl implements PersonMapper {

    @Autowired
    private AddressResolver addressResolver;
    @Autowired
    private AddressMapper addressMapper;

    @Override
    public PersonDto toDto(Person person) {
        if ( person == null ) {
            return null;
        }

        PersonDto personDto = new PersonDto();

        personDto.setEmail( personRequesterEmail( person ) );
        personDto.setPhoneNumber( personRequesterPhoneNumber( person ) );
        personDto.setAddress( addressMapper.toDto( personRequesterAddress( person ) ) );
        personDto.setId( person.getId() );
        personDto.setName( person.getName() );
        personDto.setBirthDate( person.getBirthDate() );
        personDto.setCpf( person.getCpf() );

        return personDto;
    }

    @Override
    public Person dtoToPerson(PersonDto personDto) {
        if ( personDto == null ) {
            return null;
        }

        Requester requester = null;
        String name = null;
        String birthDate = null;
        String cpf = null;

        requester = personDtoToRequester( personDto );
        name = personDto.getName();
        birthDate = personDto.getBirthDate();
        cpf = personDto.getCpf();

        Person person = new Person( name, birthDate, cpf, requester );

        return person;
    }

    private String personRequesterEmail(Person person) {
        Requester requester = person.getRequester();
        if ( requester == null ) {
            return null;
        }
        return requester.getEmail();
    }

    private String personRequesterPhoneNumber(Person person) {
        Requester requester = person.getRequester();
        if ( requester == null ) {
            return null;
        }
        return requester.getPhoneNumber();
    }

    private Address personRequesterAddress(Person person) {
        Requester requester = person.getRequester();
        if ( requester == null ) {
            return null;
        }
        return requester.getAddress();
    }

    protected Requester personDtoToRequester(PersonDto personDto) {
        if ( personDto == null ) {
            return null;
        }

        String email = null;
        String phoneNumber = null;
        Address address = null;

        email = personDto.getEmail();
        phoneNumber = personDto.getPhoneNumber();
        address = addressResolver.resolve( personDto.getAddress() );

        Requester requester = new Requester( phoneNumber, email, address );

        return requester;
    }
}
