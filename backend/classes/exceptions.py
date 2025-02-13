class CPFAlreadyExistsError(Exception):
    def __init__(self, cpf: str):
        super().__init__(f"O CPF '{cpf}' já está cadastrado no sistema.")

class CNPJAlreadyExistsError(Exception):
    def __init__(self, cnpj: str):
        super().__init__(f"O CNPJ '{cnpj}' já está cadastrado no sistema.")