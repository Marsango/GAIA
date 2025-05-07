package com.gaia.springboot.backend.service;

import com.gaia.springboot.backend.dto.PersonDto;
import com.gaia.springboot.backend.mapper.PersonMapper;
import com.gaia.springboot.backend.model.Person;
import com.gaia.springboot.backend.repository.PersonRepository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class PersonService {

    private final PersonRepository personRepository;
    private final PersonMapper personMapper;

    public PersonService(PersonMapper personMapper, PersonRepository personRepository){
        this.personMapper = personMapper;
        this.personRepository = personRepository;
    }

    public List<PersonDto> getAll(){
        List<PersonDto> personDtoList = new ArrayList<>();
        personRepository.findAll().forEach(person -> System.out.println(person.getRequester()));
        personRepository.findAll().forEach( person -> personDtoList.add(personMapper.toDto(person)));
        return personDtoList;
    }

    public PersonDto save(PersonDto newPerson){
        Person person = personMapper.dtoToPerson(newPerson);
        return personMapper.toDto(personRepository.save(person));
    }
}
