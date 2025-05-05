package com.gaia.springboot.backend.controller;

import com.gaia.springboot.backend.dto.PersonDto;
import com.gaia.springboot.backend.service.PersonService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/people")
public class PersonController {

    private final PersonService personService;

    public PersonController(PersonService personService){
        this.personService = personService;
    }

    @ResponseBody
    @GetMapping
    public List<PersonDto> getPeople(){
        return personService.getAll();
    }

//    @PostMapping
//    public PersonDto createPerson(@RequestBody PersonDto newPerson){
//        return personService.save();
//    }
}
