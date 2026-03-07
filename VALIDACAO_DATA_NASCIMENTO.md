# Validação de Data de Nascimento

## Descrição

Foi implementada validação automática de data de nascimento em todos os endpoints de cadastro e edição de usuários.

## Regras de Validação

A função `validate_data_nascimento()` realiza as seguintes verificações:

1. **Formato válido**: Aceita os formatos:
   - `YYYY-MM-DD` (ISO 8601) - Ex: `2000-01-15`
   - `DD/MM/YYYY` (brasileiro) - Ex: `15/01/2000`

2. **Data não futura**: A data de nascimento não pode ser posterior à data atual

3. **Idade mínima**: Usuário deve ter pelo menos **18 anos**

4. **Idade máxima**: Idade não pode exceder **120 anos** (validação de razoabilidade)

5. **Ano mínimo**: Ano de nascimento não pode ser anterior a **1900**

## Endpoints Afetados

### 1. Cadastro de Cliente (Web)

```bash
POST /api/register/
```

**Exemplo de requisição:**

```json
{
  "cpf": "12345678900",
  "email": "usuario@exemplo.com",
  "first_name": "João",
  "last_name": "Silva",
  "telefone": "11987654321",
  "data_nascimento": "1990-05-15"
}
```

### 2. Cadastro de Empresa (Web)

```bash
POST /api/register/empresa/
```

**Exemplo de requisição:**

```json
{
  "cnpj": "12345678000190",
  "email": "empresa@exemplo.com",
  "first_name": "Empresa XYZ",
  "telefone": "1133334444",
  "data_nascimento": "1980-03-20"
}
```

_Nota: Para empresas, pode representar data de nascimento do representante legal_

### 3. Sincronização de Usuário (Desktop)

```bash
POST /api/sync/usuario/
```

**Exemplo de requisição:**

```json
{
  "cpf": "12345678900",
  "email": "usuario@exemplo.com",
  "first_name": "João",
  "telefone": "11987654321",
  "data_nascimento": "1995-08-25"
}
```

### 4. Atualização por CPF

```bash
PATCH /api/sync/usuario/cpf/
```

**Exemplo de requisição:**

```json
{
  "cpf": "12345678900",
  "email": "novoemail@exemplo.com",
  "data_nascimento": "1992-12-10"
}
```

### 5. Atualização por CNPJ

```bash
PATCH /api/sync/usuario/cnpj/
```

**Exemplo de requisição:**

```json
{
  "cnpj": "12345678000190",
  "data_nascimento": "1985-07-30"
}
```

## Exemplos de Respostas de Erro

### Idade menor que 18 anos

```json
{
  "error": "Idade mínima é 18 anos. Idade atual: 16 anos"
}
```

### Data futura

```json
{
  "error": "Data de nascimento não pode ser futura"
}
```

### Formato inválido

```json
{
  "error": "Data de nascimento inválida. Use formato YYYY-MM-DD ou DD/MM/YYYY"
}
```

### Idade muito antiga

```json
{
  "error": "Data de nascimento muito antiga. Idade calculada: 125 anos"
}
```

### Ano anterior a 1900

```json
{
  "error": "Ano de nascimento não pode ser anterior a 1900"
}
```

## Campo Opcional

O campo `data_nascimento` é **opcional** em todos os endpoints. Se não for fornecido, o cadastro/atualização prossegue normalmente sem validação.

## Formato Recomendado

Para evitar ambiguidades, recomenda-se usar o formato ISO 8601: `YYYY-MM-DD`

Exemplo: `1995-03-15` para 15 de março de 1995

## Integração com Software Desktop

O software desktop pode enviar a data de nascimento no formato brasileiro ou ISO:

```python
# Formato ISO (recomendado)
data = {
    "cpf": "12345678900",
    "email": "usuario@exemplo.com",
    "first_name": "João",
    "data_nascimento": "1990-05-15"
}

# Formato brasileiro (também aceito)
data = {
    "cpf": "12345678900",
    "email": "usuario@exemplo.com",
    "first_name": "João",
    "data_nascimento": "15/05/1990"
}
```

## Limpeza de Campo

Para remover a data de nascimento de um usuário existente, envie `null` ou string vazia:

```json
{
  "cpf": "12345678900",
  "data_nascimento": null
}
```

ou

```json
{
  "cpf": "12345678900",
  "data_nascimento": ""
}
```

## Implementação Técnica

A validação é realizada pela função `validate_data_nascimento()` em `authentication/views.py`:

```python
def validate_data_nascimento(data_nascimento_str):
    """
    Retorna: (is_valid: bool, error_message: str, data_normalizada: date)
    """
    # ... validações ...
    return True, None, data_normalizada
```

A função retorna uma tupla com:

- `is_valid`: Boolean indicando se a data é válida
- `error_message`: Mensagem de erro (ou None se válido)
- `data_normalizada`: Objeto date normalizado (ou None se inválido)
