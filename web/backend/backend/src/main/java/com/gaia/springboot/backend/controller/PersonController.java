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
        return personService.getPeople();
    }

    @PostMapping
    public PersonDto postPerson(@RequestBody PersonDto newPerson){
        return personService.savePerson(newPerson);
    }

    @PatchMapping("/{id}")
    public PersonDto patchPerson(@PathVariable Long id, @RequestBody PersonDto newPerson) {
        return personService.updatePerson(id, newPerson);
    }

    @DeleteMapping("/{id}")
    public void deletePerson(@PathVariable Long id) {
        personService.deletePerson(id);
    }
}
