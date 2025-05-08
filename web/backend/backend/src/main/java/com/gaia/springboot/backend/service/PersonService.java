package com.gaia.springboot.backend.service;

import com.gaia.springboot.backend.dto.PersonDto;
import com.gaia.springboot.backend.mapper.PersonMapper;
import com.gaia.springboot.backend.model.Person;
import com.gaia.springboot.backend.repository.PersonRepository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class PersonService {

    private final PersonRepository personRepository;
    private final PersonMapper personMapper;
    private final AddressResolverService addressService;

    public PersonService(PersonMapper personMapper, PersonRepository personRepository, AddressResolverService addressService){
        this.personMapper = personMapper;
        this.personRepository = personRepository;
        this.addressService = addressService;
    }

    public List<PersonDto> getPeople(){
        List<PersonDto> personDtoList = new ArrayList<>();
        personRepository.findAll().forEach( person -> personDtoList.add(personMapper.toDto(person)));
        return personDtoList;
    }

    public PersonDto savePerson(PersonDto newPerson){
        Person person = personMapper.dtoToPerson(newPerson);
        return personMapper.toDto(personRepository.save(person));
    }

    public PersonDto updatePerson(Long id, PersonDto newPerson){
        Person person = personRepository.findById(id).orElse(null);
        personMapper.updatePersonFromDto(newPerson, person, addressService);
        if (person != null){
            personRepository.save(person);
        }
        return personMapper.toDto(person);
    }

    public void deletePerson(Long id){
        personRepository.deleteById(id);
    }
}
