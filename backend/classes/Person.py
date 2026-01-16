from backend.classes.Requester import Requester
from datetime import date
from typing import get_type_hints
from backend.classes.utils import verify_type
from backend.classes.Address import Address
from datetime import datetime


class Person(Requester):

    def __init__(self, phone_number: str, email: str, name: str, birth_date: str, cpf: str, address: Address) -> None:
        verify_type(get_type_hints(Person.__init__), locals())

        super().__init__(phone_number, email, address)
        
        # CORREÇÃO: Chamar métodos que atribuem internamente
        self.verify_valid_date(birth_date)  # ← Agora apenas chama
        self.verify_valid_cpf(cpf)          # ← Agora apenas chama  
        self.verify_name(name)              # ← Agora apenas chama

    def verify_valid_date(self, birth_date: str) -> None:
        """Valida e atribui data de nascimento"""
        try:
            self.__birth_date = datetime.strptime(birth_date, '%d/%m/%Y').strftime("%d/%m/%Y")
        except:
            raise ValueError("Error with values of 'birth_date'")

    def verify_valid_cpf(self, cpf: str) -> None:
        """Valida e atribui CPF"""
        if len(cpf) != 11:
            raise ValueError("Error with values of 'cpf'")
        equal_numbers = [x for x in cpf if x == cpf[0]]
        if len(equal_numbers) == 11:
            raise ValueError("Error with values of 'cpf'")
        
        first_digit = int(cpf[-2])
        second_digit = int(cpf[-1])

        def verify_digit(expected_digit, cpf_fraction):
            digit_sum = sum([int(x)*(len(cpf_fraction) + 1 - i) for i, x in enumerate(cpf_fraction)])
            calculated_digit = (digit_sum * 10 % 11) % 10
            if int(expected_digit) != calculated_digit:
                raise ValueError(f"CPF inválido: erro no dígito verificador {expected_digit}.")

        verify_digit(first_digit, cpf[:9])
        verify_digit(second_digit, cpf[:10])
        self.__cpf = cpf

    def verify_name(self, name: str) -> None:
        """Valida e atribui nome"""
        if any(char.isdigit() for char in name):
            raise ValueError("Error with values of 'name'")
        self.__name = name

    @property
    def cpf(self) -> str:
        return self.__cpf

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return super().get_email()

    @property
    def birth_date(self) -> str:
        return self.__birth_date