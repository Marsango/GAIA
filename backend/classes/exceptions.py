class CPFAlreadyExistsError(Exception):
    def __init__(self, cpf: str):
        super().__init__(f"O CPF '{cpf}' já está cadastrado no sistema.")