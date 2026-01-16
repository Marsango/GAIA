#!/usr/bin/env python3
"""
Script de teste completo para DatabaseAPI
Testa compatibilidade com DatabaseSQLite original
"""

from random import random
import sys
import os
from datetime import datetime

# Adicionar diretório pai ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'classes'))

from backend.classes.Sample import Sample
from backend.classes.Report import Report
from backend.classes.Person import Person
from backend.classes.Address import Address
from backend.classes.Company import Company
from backend.classes.Property import Property
from backend.classes.exceptions import CNPJAlreadyExistsError
from backend.classes.DatabaseHTTPWrapper import DatabaseHTTPWrapper
from backend.classes.Database import create_database 

class DatabaseTester:
    """Classe para testar todas as funções do Database"""
    
    def __init__(self, use_api=True, verbose=True):
        self.use_api = use_api
        self.verbose = verbose
        self.test_results = []
        self.test_data = {}
        
        # Criar instância do database
        self.db = create_database(force_api=use_api)
        
        if verbose:
            mode = "API Django" if use_api else "SQLite Local"
            print(f"[ROCKET] Iniciando testes em modo: {mode}")
            print("=" * 60)
    
    def log_test(self, test_name, result, message=""):
        """Registra resultado de um teste"""
        status = "[OK] PASS" if result else "[FAIL] FAIL"
        self.test_results.append({
            'name': test_name,
            'passed': result,
            'message': message
        })
        
        if self.verbose:
            print(f"{status} - {test_name}")
            if message and not result:
                print(f"   {message}")

    def gerar_cpf_valido(self) -> str:
        import random
        def calc_digitos(cpf):
            soma = sum((len(cpf)+1-i)*int(num) for i, num in enumerate(cpf))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)

        cpf = [str(random.randint(0, 9)) for _ in range(9)]
        cpf.append(calc_digitos(cpf))
        cpf.append(calc_digitos(cpf))
        return ''.join(cpf)
    
    def gerar_cnpj(self) -> str:
        import random
        """
        Gera um CNPJ válido (14 dígitos) com dígitos verificadores corretos
        """
        def calcula_digito(cnpj_parcial: list[int]) -> int:
            pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            soma = 0

            # Para o primeiro dígito, ignora o peso 6
            if len(cnpj_parcial) == 12:
                pesos = pesos[1:]

            for digito, peso in zip(cnpj_parcial, pesos):
                soma += digito * peso

            resto = soma % 11
            return 0 if resto < 2 else 11 - resto

        # Gera os 12 primeiros dígitos
        cnpj = [random.randint(0, 9) for _ in range(12)]

        # Calcula os dois dígitos verificadores
        cnpj.append(calcula_digito(cnpj))
        cnpj.append(calcula_digito(cnpj))

        return ''.join(map(str, cnpj))
    
    def setup_test_data(self):
        """Cria dados de teste"""
        print("\n Configurando dados de teste...")
        
        # Endereço de teste
        self.test_address = Address(
            cep="12345678",
            street="Rua das Flores",
            address_number="123",
            city="São Paulo",
            state="SP",
            country="Brasil"
        )
        
        # Pessoa de teste
        self.test_person = Person(
            name="João Silva Teste",
            birth_date="15/05/1980",
            cpf=self.gerar_cpf_valido(),
            email="joao.teste@email.com",
            phone_number="(11) 99999-8888",
            address=self.test_address
        )
        
        # Empresa de teste
        self.test_company = Company(
            company_name="Empresa Teste LTDA",
            cnpj=self.gerar_cnpj(),
            email="contato@empresateste.com",
            phone_number="(11) 3333-4444",
            address=self.test_address
        )
        
        # Propriedade de teste
        self.test_property = Property(
            name="Fazenda Teste",
            registration_number="999999",
        )

        
        # Amostra de teste
        self.test_sample = Sample(
            description="Amostra de teste do solo",
            collection_date=datetime.now().strftime("%Y-%m-%d"),
            total_area=10.5,
            latitude=-23.5505,
            longitude=-46.6333,
            depth=0.2,
            phosphorus=15.5,
            potassium=120.0,
            organic_matter=3.2,
            ph=6.5,
            aluminum=0.5,
            calcium=3.8,
            magnesium=1.2,
            copper=0.03,
            iron=25.0,
            manganese=12.5,
            zinc=1.8,
            clay=35.0,
            silte=40.0,
            sand=25.0,
            is_editing=False,
            sample_id=1,
            smp=6.0,
        )
        
        print("[OK] Dados de teste configurados")
    
    # ========== TESTES DE CONEXÃO ==========
    
    def test_connection(self):
        """Testa conexão com o banco/API"""
        test_name = "Teste de Conexão"
        try:
            if self.use_api:
                # Testar conexão com API
                if callable(getattr(self.db.db, 'test_connection', None)):
                    result = self.db.db.test_connection()
                    self.log_test(test_name, result, "API responde" if result else "API não responde")
                else:
                    # Tentar login automático
                    result = self.db.login()
                    self.log_test(test_name, result, "Login automático" if result else "Falha no login")
            else:
                # Para SQLite, testar se consegue executar uma query simples
                self.db.db._Database__cur.execute("SELECT 1")
                self.log_test(test_name, True, "SQLite conectado")
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    def test_login(self):
        """Testa função de login"""
        test_name = "Teste de Login"
        try:
            if self.use_api:
                # Testar login com credenciais técnicas
                result = self.db.db.login(cpf="99988877700", password="123456")
                self.log_test(test_name, result, 
                           "Login técnico OK" if result else "Falha no login técnico")
            else:
                # Para SQLite, marcar como passou (não tem login)
                self.log_test(test_name, True, "SQLite não requer login")
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    # ========== TESTES DE CRIAÇÃO ==========
    
    def test_insert_person(self):
        test_name = "Inserir Pessoa"

        try:
            print(f"\n Iniciando teste: {test_name}")

            name = self.test_person.name
            cpf_original = self.test_person.cpf
            cpf_limpo = self._clean_cpf(cpf_original)

            print(f"  Inserindo pessoa: {name} | CPF: {cpf_original}")

            # 1. Inserir
            self.db.insert_person(self.test_person, self.test_address)

            # 2. Buscar EXATAMENTE pelo CPF criado
            persons = self.db.get_persons(cpf=cpf_original)

            if not persons:
                raise AssertionError("Pessoa não encontrada após inserção")

            pessoa = persons[0]
            self.test_data["requester_id"] = pessoa['id']

            inserted_id = pessoa["id"]
            inserted_name = pessoa["name"]
            inserted_cpf = self._clean_cpf(pessoa["cpf"])
            # 3. Validar
            assert inserted_name == name, "Nome não confere"
            assert inserted_cpf == cpf_limpo, "CPF não confere"

            self.test_data["person_id"] = inserted_id

            message = f"[OK] Pessoa '{name}' inserida com sucesso (ID: {inserted_id})"
            print(f"  {message}")
            self.log_test(test_name, True, message)

        except Exception as e:
            error_msg = f"[FAIL] Erro no teste: {str(e)}"
            print(f"  {error_msg}")
            self.log_test(test_name, False, error_msg)

    
    def _clean_cpf(self, cpf: str) -> str:
        """Remove formatação do CPF (pontos, traços, espaços)"""
        if not cpf:
            return ""
        # Remove tudo que não é dígito
        import re
        return re.sub(r'[^\d]', '', str(cpf))

    def test_insert_company(self):
        """Testa inserção de empresa"""
        test_name = "Inserir Empresa"
        try:
            company = self.db.insert_company(self.test_company, self.test_address)
            self.test_data['id'] = company['id']
            
            # Verificar se foi inserida
            companies = self.db.get_companies(id=self.test_data['id'])
            
            if companies and len(companies) > 0:
                inserted = companies[0]
                match = (
                    inserted['name'] == self.test_company.get_company_name() and
                    inserted['cnpj'] == self.test_company.get_cnpj()
                )
                self.test_data['id'] = inserted['id']
                self.log_test(test_name, match,
                           f"Empresa inserida: ID {inserted['id']}" if match else "Empresa não encontrada")
            else:
                self.log_test(test_name, False, "Empresa não encontrada após inserção")
                
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    def test_insert_property(self):
        """Testa inserção de propriedade"""
        test_name = "Inserir Propriedade"
        try:
            requester_id = self.test_data.get('requester_id')
            if not requester_id:
                raise Exception("requester_id não configurado")

            self.db.insert_property(self.test_property, requester_id, self.test_address)

            properties = self.db.get_properties()
            
            # Procurar exatamente a propriedade inserida
            test_name_val = self.test_property.get_name()
            test_reg_val = str(self.test_property.get_registration_number())
            
            inserted = next(
                (
                    p for p in properties
                    if p['name'] == test_name_val
                    and str(p['registration_number']) == test_reg_val
                ),
                None
            )

            if inserted:
                self.test_data['property_id'] = inserted['id']
                self.log_test(
                    test_name,
                    True,
                    f"Propriedade inserida: ID {inserted['id']}"
                )
            else:
                self.log_test(
                    test_name,
                    False,
                    "Propriedade inserida não encontrada"
                )

        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")


    def test_insert_sample(self):
        """Testa inserção de amostra"""
        test_name = "Inserir Amostra"
        try:
            property_id = self.test_data.get('property_id')
            sample_number = 1001  # Número de amostra de teste
            
            self.db.insert_sample(self.test_sample, property_id, sample_number)
            
            # Verificar se foi inserida
            samples = self.db.get_samples(property_id=property_id)
            
            if samples and len(samples) > 0:
                inserted = samples[0]
                match = (
                    inserted['description'] == self.test_sample.get_description and
                    inserted['sample_number'] == sample_number
                )
                self.test_data['sample_id'] = inserted['id']
                self.test_data['sample_number'] = sample_number
                self.log_test(test_name, match,
                           f"Amostra inserida: ID {inserted['id']}" if match else "Amostra não encontrada")
            else:
                self.log_test(test_name, False, "Amostra não encontrada após inserção")
                
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    # ========== TESTES DE CONSULTA ==========
    
    def test_get_persons(self):
        """Testa consulta de pessoas"""
        test_name = "Consultar Pessoas"
        try:
            # Testar diferentes tipos de consulta
            tests = [
                ("Por ID", self.db.get_persons(id=self.test_data.get('person_id', 1))),
                ("Por Nome", self.db.get_persons(name="João")),
                ("Por CPF", self.db.get_persons(cpf="111.222")),
                ("Todas", self.db.get_persons())
            ]
            
            all_pass = True
            for test_type, result in tests:
                is_list = isinstance(result, list)
                has_data = len(result) > 0 if is_list else False
                
                if not is_list:
                    self.log_test(f"{test_name} - {test_type}", False, f"Resultado não é lista: {type(result)}")
                    all_pass = False
                elif test_type == "Por ID" and not has_data:
                    self.log_test(f"{test_name} - {test_type}", False, "Nenhuma pessoa encontrada por ID")
                    all_pass = False
            
            self.log_test(test_name, all_pass, 
                       f"Consultas OK: {len([r for _, r in tests if isinstance(r, list)])}/{len(tests)}")
            
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    def test_get_companies(self):
        """Testa consulta de empresas"""
        test_name = "Consultar Empresas"
        try:
            tests = [
                ("Por ID", self.db.get_companies(id=self.test_data.get('company_id', 1))),
                ("Por Nome", self.db.get_companies(company_name="Empresa")),
                ("Por CNPJ", self.db.get_companies(cnpj="12.345")),
                ("Todas", self.db.get_companies())
            ]
            
            all_pass = True
            for test_type, result in tests:
                is_list = isinstance(result, list)
                
                if not is_list:
                    self.log_test(f"{test_name} - {test_type}", False, f"Resultado não é lista: {type(result)}")
                    all_pass = False
            
            self.log_test(test_name, all_pass, "Consultas de empresas realizadas")
            
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    def test_get_requesters(self):
        """Testa consulta de solicitantes"""
        test_name = "Consultar Solicitantes"
        try:
            if callable(getattr(self.db, 'get_requesters', None)):
                requesters = self.db.get_requesters()
                
                is_list = isinstance(requesters, list)
                has_data = len(requesters) > 0 if is_list else False
                
                self.log_test(test_name, is_list and has_data,
                           f"Encontrados {len(requesters)} solicitantes" if has_data else "Nenhum solicitante encontrado")
            else:
                self.log_test(test_name, False, "Método get_requesters não implementado")
                
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    def test_get_properties(self):
        """Testa consulta de propriedades"""
        test_name = "Consultar Propriedades"
        try:
            property_id = self.test_data.get('property_id')
            person_id = self.test_data.get('person_id')
            
            tests = [
                ("Por Requester", self.db.get_properties(requester_id=person_id)),
                ("Todas", self.db.get_properties())
            ]
            
            if property_id:
                tests.insert(0, ("Por ID", self.db.get_properties(id=property_id)))
            
            all_pass = True
            for test_type, result in tests:
                is_list = isinstance(result, list)
                
                if not is_list:
                    self.log_test(f"{test_name} - {test_type}", False, f"Resultado não é lista: {type(result)}")
                    all_pass = False
            
            self.log_test(test_name, all_pass, "Consultas de propriedades realizadas")
            
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    def test_get_samples(self):
        """Testa consulta de amostras"""
        test_name = "Consultar Amostras"
        try:
            property_id = self.test_data.get('property_id')
            sample_id = self.test_data.get('sample_id')
            
            tests = []
            
            if property_id:
                tests.append(("Por Propriedade", self.db.get_samples(property_id=property_id)))
            
            if sample_id:
                tests.append(("Por ID", self.db.get_samples(sample_id=sample_id)))
            
            tests.append(("Todas", self.db.get_samples()))
            
            all_pass = True
            for test_type, result in tests:
                is_list = isinstance(result, list)
                
                if not is_list:
                    self.log_test(f"{test_name} - {test_type}", False, f"Resultado não é lista: {type(result)}")
                    all_pass = False
            
            self.log_test(test_name, all_pass, "Consultas de amostras realizadas")
            
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    def test_get_sample_info(self):
        """Testa obtenção de informações detalhadas da amostra"""
        test_name = "Informações da Amostra"
        try:
            sample_id = self.test_data.get('sample_id')
            
            if sample_id:
                info = self.db.get_sample_info(sample_id)
                
                if info:
                    # Verificar se tem os campos básicos
                    has_basic_fields = all([
                        'sample_description' in info,
                        'sample_number' in info,
                        'collection_date' in info,
                        'property_name' in info
                    ])
                    
                    self.log_test(test_name, has_basic_fields,
                               f"Informações obtidas: {list(info.keys())}" if has_basic_fields else "Campos faltando")
                else:
                    self.log_test(test_name, False, "Nenhuma informação retornada")
            else:
                self.log_test(test_name, False, "ID da amostra não disponível para teste")
                
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    # ========== TESTES DE EDIÇÃO ==========
    
    def test_edit_person(self):
        """Testa edição de pessoa"""
        test_name = "Editar Pessoa"
        try:
            person_id = self.test_data.get('person_id')
            
            if person_id:
                # Criar pessoa editada
                edited_person = Person(
                    name="João Silva Editado",
                    birth_date="20/06/1985",
                    cpf="111.222.333-44",  # Mesmo CPF
                    email="joao.editado@email.com",
                    phone_number="(11) 98888-7777"
                )
                
                # Para SQLite, precisamos do requester_id
                if not self.use_api:
                    persons = self.db.get_persons(id=person_id)
                    if persons:
                        requester_id = persons[0]['requester_id']
                        self.db.edit_person(edited_person, self.test_address, person_id, requester_id)
                else:
                    # Para API, assumir que edit_person funciona sem requester_id
                    if callable(getattr(self.db, 'edit_person', None)):
                        self.db.edit_person(edited_person, self.test_address, person_id, 0)
                
                # Verificar se foi editada
                persons = self.db.get_persons(id=person_id)
                if persons and len(persons) > 0:
                    updated = persons[0]
                    match = updated['name'] == "João Silva Editado"
                    self.log_test(test_name, match, 
                               f"Nome atualizado: {updated['name']}" if match else "Nome não atualizado")
                else:
                    self.log_test(test_name, False, "Pessoa não encontrada após edição")
            else:
                self.log_test(test_name, False, "ID da pessoa não disponível para teste")
                
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    def test_edit_property(self):
        """Testa edição de propriedade"""
        test_name = "Editar Propriedade"
        try:
            property_id = self.test_data.get('property_id')
            
            if property_id:
                # Criar propriedade editada
                edited_property = Property(
                    name="Fazenda Teste Editada",
                    location="Rodovia Editada, km 20",
                    registration_number=888888
                )
                
                self.db.edit_property(edited_property, property_id)
                
                # Verificar se foi editada
                properties = self.db.get_properties(id=property_id)
                if properties and len(properties) > 0:
                    updated = properties[0]
                    match = updated['name'] == "Fazenda Teste Editada"
                    self.log_test(test_name, match,
                               f"Nome atualizado: {updated['name']}" if match else "Nome não atualizado")
                else:
                    self.log_test(test_name, False, "Propriedade não encontrada após edição")
            else:
                self.log_test(test_name, False, "ID da propriedade não disponível para teste")
                
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    def test_edit_sample(self):
        """Testa edição de amostra"""
        test_name = "Editar Amostra"
        try:
            sample_id = self.test_data.get('sample_id')
            
            if sample_id:
                # Criar amostra editada
                edited_sample = Sample(
                    description="Amostra editada do solo",
                    collection_date=datetime.now().strftime("%Y-%m-%d"),
                    total_area=12.0,
                    latitude=-23.5605,
                    longitude=-46.6433,
                    depth=0.25,
                    phosphorus=16.0,
                    potassium=125.0,
                    organic_matter=3.5,
                    ph=6.8,
                    aluminum=0.6,
                    h_al=2.2,
                    calcium=4.0,
                    magnesium=1.3,
                    copper=0.04,
                    iron=26.0,
                    manganese=13.0,
                    zinc=2.0,
                    base_sum=6.0,
                    clay=36.0,
                    silte=41.0,
                    sand=23.0,
                    classification="Argiloso Médio",
                    ctc=11.0,
                    v_percent=55.0,
                    aluminum_saturation=6.0,
                    effective_ctc=9.0,
                    smp=6.5,
                    used_config="Editado"
                )
                
                self.db.edit_sample(edited_sample, sample_id)
                
                # Verificar se foi editada
                samples = self.db.get_samples(sample_id=sample_id)
                if samples and len(samples) > 0:
                    updated = samples[0]
                    match = updated['description'] == "Amostra editada do solo"
                    self.log_test(test_name, match,
                               f"Descrição atualizada: {updated['description']}" if match else "Descrição não atualizada")
                else:
                    self.log_test(test_name, False, "Amostra não encontrada após edição")
            else:
                self.log_test(test_name, False, "ID da amostra não disponível para teste")
                
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    # ========== TESTES DE EXCLUSÃO ==========
    
    def test_delete_sample(self):
        """Testa exclusão de amostra"""
        test_name = "Excluir Amostra"
        try:
            sample_id = self.test_data.get('sample_id')
            
            if sample_id:
                self.db.delete_sample(sample_id)
                
                # Verificar se foi excluída
                # Nota: Em API, pode ser apenas desativada
                samples = self.db.get_samples(sample_id=sample_id)
                
                if self.use_api:
                    # Para API, a exclusão pode ser apenas desativação
                    self.log_test(test_name, True, f"Amostra {sample_id} marcada como inativa")
                else:
                    # Para SQLite, deve ter sido excluída
                    is_deleted = len(samples) == 0
                    self.log_test(test_name, is_deleted,
                               f"Amostra excluída" if is_deleted else "Amostra ainda encontrada")
            else:
                self.log_test(test_name, False, "ID da amostra não disponível para teste")
                
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    def test_delete_property(self):
        """Testa exclusão de propriedade"""
        test_name = "Excluir Propriedade"
        try:
            property_id = self.test_data.get('property_id')
            
            if property_id:
                self.db.delete_property(property_id)
                
                # Verificar se foi excluída
                properties = self.db.get_properties(id=property_id)
                
                if self.use_api:
                    # Para API, a exclusão pode ser apenas desativação
                    self.log_test(test_name, True, f"Propriedade {property_id} marcada como inativa")
                else:
                    # Para SQLite, deve ter sido excluída
                    is_deleted = len(properties) == 0
                    self.log_test(test_name, is_deleted,
                               f"Propriedade excluída" if is_deleted else "Propriedade ainda encontrada")
            else:
                self.log_test(test_name, False, "ID da propriedade não disponível para teste")
                
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    # ========== TESTES AUXILIARES ==========
    
    def test_get_countries(self):
        """Testa obtenção de países"""
        test_name = "Obter Países"
        try:
            countries = self.db.get_countries()
            
            is_list = isinstance(countries, list)
            has_data = len(countries) > 0 if is_list else False
            
            self.log_test(test_name, is_list and has_data,
                       f"{len(countries)} países encontrados" if has_data else "Nenhum país encontrado")
            
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    def test_get_states(self):
        """Testa obtenção de estados"""
        test_name = "Obter Estados"
        try:
            states = self.db.get_states("Brasil")
            
            is_list = isinstance(states, list)
            has_data = len(states) > 0 if is_list else False
            
            self.log_test(test_name, is_list and has_data,
                       f"{len(states)} estados encontrados" if has_data else "Nenhum estado encontrado")
            
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    def test_get_cities(self):
        """Testa obtenção de cidades"""
        test_name = "Obter Cidades"
        try:
            cities = self.db.get_cities("SP")
            
            is_list = isinstance(cities, list)
            
            self.log_test(test_name, is_list,
                       f"{len(cities)} cidades encontradas" if is_list and len(cities) > 0 else "Consulta realizada")
            
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    # ========== TESTES DE FUNCIONALIDADE EXTRA ==========
    
    def test_report_functionality(self):
        """Testa funcionalidades relacionadas a laudos"""
        test_name = "Funcionalidades de Laudo"
        
        try:
            # Testar get_next_report_id se existir
            if callable(getattr(self.db, 'get_next_report_id', None)):
                next_id = self.db.get_next_report_id()
                is_int = isinstance(next_id, int)
                self.log_test(f"{test_name} - Próximo ID", is_int, f"Próximo ID: {next_id}")
            else:
                self.log_test(f"{test_name} - Próximo ID", False, "Método get_next_report_id não implementado")
            
            # Testar get_report_info se existir
            if callable(getattr(self.db, 'get_report_info', None)):
                reports = self.db.get_report_info()
                is_list = isinstance(reports, list)
                self.log_test(f"{test_name} - Listar Laudos", is_list,
                           f"{len(reports)} laudos encontrados" if is_list else "Falha ao listar laudos")
            else:
                self.log_test(f"{test_name} - Listar Laudos", False, "Método get_report_info não implementado")
                
        except Exception as e:
            self.log_test(test_name, False, f"Erro: {e}")
    
    # ========== FUNÇÕES DE LIMPEZA ==========
    
    def cleanup_test_data(self):
        """Limpa todos os dados de teste criados durante os testes"""
        print("\n Limpando dados de teste...")
        
        cleanup_count = 0
        cleanup_errors = []
        
        # DEBUG: Mostrar o que vamos limpar
        print(f"  Dados de teste registrados: {self.test_data}")
        
        # ========== 1. LIMPAR AMOSTRAS ==========
        sample_id = self.test_data.get('sample_id')
        if sample_id:
            try:
                print(f"  Tentando remover amostra ID: {sample_id}")
                if callable(getattr(self.db, 'delete_sample', None)):
                    self.db.delete_sample(sample_id)
                    print(f"  [OK] Amostra {sample_id} removida")
                    cleanup_count += 1
                else:
                    print(f"   Método delete_sample não disponível")
            except Exception as e:
                error_msg = f"Amostra {sample_id}: {e}"
                print(f"  [FAIL] {error_msg}")
                cleanup_errors.append(error_msg)
        
        # ========== 2. LIMPAR PROPRIEDADES ==========
        property_id = self.test_data.get('property_id')
        if property_id:
            try:
                print(f"  Tentando remover propriedade ID: {property_id}")
                if callable(getattr(self.db, 'delete_property', None)):
                    self.db.delete_property(property_id)
                    print(f"  [OK] Propriedade {property_id} removida")
                    cleanup_count += 1
                else:
                    print(f"   Método delete_property não disponível")
            except Exception as e:
                error_msg = f"Propriedade {property_id}: {e}"
                print(f"  [FAIL] {error_msg}")
                cleanup_errors.append(error_msg)
        
        # ========== 3. LIMPAR EMPRESAS ==========
        company_id = self.test_data.get('company_id')
        if company_id:
            try:
                print(f"  Tentando remover empresa ID: {company_id}")
                if callable(getattr(self.db, 'delete_company', None)):
                    self.db.delete_company(company_id)
                    print(f"  [OK] Empresa {company_id} removida")
                    cleanup_count += 1
                else:
                    # Tentar buscar e deletar por CNPJ
                    print(f"   Tentando limpar empresa por CNPJ...")
                    self._cleanup_company_by_cnpj()
            except Exception as e:
                error_msg = f"Empresa {company_id}: {e}"
                print(f"  [FAIL] {error_msg}")
                cleanup_errors.append(error_msg)
        
        # ========== 4. LIMPAR PESSOAS ==========
        person_id = self.test_data.get('person_id')
        if person_id:
            try:
                print(f"  Tentando remover pessoa ID: {person_id}")
                if callable(getattr(self.db, 'delete_person', None)):
                    self.db.delete_person(person_id)
                    print(f"  [OK] Pessoa {person_id} removida")
                    cleanup_count += 1
                else:
                    print(f"   Método delete_person não disponível")
            except Exception as e:
                error_msg = f"Pessoa {person_id}: {e}"
                print(f"  [FAIL] {error_msg}")
                cleanup_errors.append(error_msg)

        # ========== 5. LIMPEZA EMPRESA POR CNPJ (MÉTODO AUXILIAR) ==========
        company_id = self.test_data.get('company_id')
        if not company_id:
            try:
                print(f"  Tentando limpar empresa por CNPJ (método auxiliar)...")
                cnpj_removed = self._cleanup_by_cnpj_backup()
                cleanup_count += cnpj_removed
            except Exception as e:
                error_msg = f"Limpeza por CNPJ auxiliar: {e}"
                print(f"  [FAIL] {error_msg}")
                cleanup_errors.append(error_msg)     
        
        # ========== 5. LIMPEZA POR CPF (BACKUP) ==========
        try:
            print(f"  Executando limpeza por CPF (backup)...")
            cpf_removed = self._cleanup_by_cpf_backup()
            cleanup_count += cpf_removed
        except Exception as e:
            error_msg = f"Limpeza por CPF backup: {e}"
            print(f"  [FAIL] {error_msg}")
            cleanup_errors.append(error_msg)
        
        # ========== 6. LIMPEZA POR CNPJ (BACKUP) ==========
        try:
            print(f"  Executando limpeza por CNPJ (backup)...")
            cnpj_removed = self._cleanup_by_cnpj_backup()
            cleanup_count += cnpj_removed
        except Exception as e:
            error_msg = f"Limpeza por CNPJ backup: {e}"
            print(f"  [FAIL] {error_msg}")
            cleanup_errors.append(error_msg)
        
        # ========== 7. LIMPEZA POR NOME (EXTRA) ==========
        try:
            print(f"  Executando limpeza por nome 'Teste'...")
            nome_removed = self._cleanup_by_name_test()
            cleanup_count += nome_removed
        except Exception as e:
            error_msg = f"Limpeza por nome: {e}"
            print(f"  [FAIL] {error_msg}")
            cleanup_errors.append(error_msg)
        
        print(f"\n[OK] Limpeza concluída: {cleanup_count} itens removidos")
        
        if cleanup_errors:
            print(f"\n Erros durante a limpeza ({len(cleanup_errors)}):")
            for error in cleanup_errors:
                print(f"  [FAIL] {error}")
        
        # Limpar dicionário de dados de teste
        self.test_data.clear()
        
        return cleanup_count, cleanup_errors

    def _cleanup_by_cpf_backup(self):
        """Limpa por CPF de teste (método auxiliar)"""
        removed = 0
        
        # Tentar obter CPF da pessoa de teste de forma segura
        test_cpf = None
        
        if callable(getattr(self, 'test_person', None)):
            try:
                # Tenta acessar via property
                test_cpf = self.test_person.cpf
            except AttributeError:
                # Tenta acessar atributo privado
                test_cpf = getattr(self.test_person, '_Person__cpf', None)
        
        if not test_cpf:
            print(f"     Nenhum CPF de teste disponível")
            return 0
        
        print(f"    Procurando por CPF: {test_cpf}")
        
        try:
            # Buscar com formatação
            persons = self.db.get_persons(cpf=test_cpf)
            if not persons:
                # Tentar sem formatação
                import re
                cpf_clean = re.sub(r'[^\d]', '', test_cpf)
                if len(cpf_clean) == 11:
                    persons = self.db.get_persons(cpf=cpf_clean)
            
            for person in persons:
                try:
                    # Acesso seguro ao ID do SQLiteRow
                    person_id = None
                    
                    # Método 1: Tentar acessar como dicionário
                    try:
                        person_id = person['id']
                    except (KeyError, TypeError):
                        pass
                    
                    # Método 2: Tentar acessar como atributo
                    if person_id is None:
                        try:
                            person_id = person.id
                        except AttributeError:
                            pass
                    
                    # Método 3: Tentar acessar via _data (se for SQLiteRow)
                    if person_id is None and callable(getattr(person, '_data', None)):
                        person_id = person._data.get('id')
                    
                    if person_id and callable(getattr(self.db, 'delete_person', None)):
                        name = ""
                        try:
                            name = person['name'] if 'name' in person else getattr(person, 'name', 'N/A')
                        except:
                            pass
                        
                        print(f"    Removendo pessoa ID: {person_id} - {name}")
                        self.db.delete_person(person_id)
                        removed += 1
                        
                except Exception as e:
                    print(f"    [FAIL] Erro ao remover pessoa: {e}")
                    import traceback
                    traceback.print_exc()
                    
        except Exception as e:
            print(f"    [FAIL] Erro na busca por CPF: {e}")
        
        return removed

    def _cleanup_by_cnpj_backup(self):
        """Limpa por CNPJ de teste (método auxiliar)"""
        removed = 0
        
        # Tentar obter CNPJ da empresa de teste de forma segura
        test_cnpj = None
        if callable(getattr(self, 'test_company', None)):
            try:
                test_cnpj = self.test_company.get_cnpj()
            except:
                test_cnpj = getattr(self.test_company, 'cnpj', None)
        
        if not test_cnpj:
            print(f"     Nenhum CNPJ de teste disponível")
            return 0
        
        print(f"    Procurando por CNPJ: {test_cnpj}")
        
        try:
            companies = self.db.get_companies(cnpj=test_cnpj)
            for company in companies:
                try:
                    if 'id' in company and callable(getattr(self.db, 'delete_company', None)):
                        print(f"    Removendo empresa ID: {company['id']} - {company.get('company_name', 'N/A')}")
                        self.db.delete_company(company['id'])
                        removed += 1
                except Exception as e:
                    print(f"    [FAIL] Erro ao remover empresa {company.get('id')}: {e}")
                    
        except Exception as e:
            print(f"    [FAIL] Erro na busca por CNPJ: {e}")
        
        return removed

    def _cleanup_by_name_test(self):
        """Limpa por nomes que contém 'Teste'"""
        removed = 0
        
        try:
            # Buscar pessoas com "Teste" no nome
            all_persons = self.db.get_persons()
            for person in all_persons:
                name = person.get('name', '')
                if name and ('Teste' in name or 'teste' in name.lower() or 'TEST' in name.upper()):
                    try:
                        delete_fn = getattr(self.db, 'delete_person', None)
                        if 'id' in person and callable(delete_fn):
                            delete_fn(person['id'])
                            print(f"    Removendo pessoa teste: {name} (ID: {person['id']})")
                            self.db.delete_person(person['id'])
                            removed += 1
                    except Exception as e:
                        print(f"    [FAIL] Erro ao remover pessoa {person['id']}: {e}")
            
            # Buscar empresas com "Teste" no nome
            all_companies = self.db.get_companies()
            for company in all_companies:
                name = company.get('company_name', '')
                if name and ('Teste' in name or 'teste' in name.lower() or 'TEST' in name.upper()):
                    try:
                        if 'id' in company and callable(getattr(self.db, 'delete_company', None)):
                            print(f"    Removendo empresa teste: {name} (ID: {company['id']})")
                            self.db.delete_company(company['id'])
                            removed += 1
                    except Exception as e:
                        print(f"    [FAIL] Erro ao remover empresa {company['id']}: {e}")
                        
        except Exception as e:
            print(f"    [FAIL] Erro na limpeza por nome: {e}")
        
        return removed

    def _cleanup_company_by_cnpj(self):
        """Limpa empresa usando CNPJ quando ID não funciona"""
        if not callable(getattr(self, 'test_company', None)):
            return 0
        
        try:
            cnpj = None
            try:
                cnpj = self.test_company.get_cnpj()
            except:
                cnpj = getattr(self.test_company, '_Company__cnpj', None)
            
            if cnpj and callable(getattr(self.db, 'get_companies', None)):
                companies = self.db.get_companies(cnpj=cnpj)
                for company in companies:
                    if 'Teste' in company.get('company_name', ''):
                        try:
                            if callable(getattr(self.db, 'delete_company', None)):
                                self.db.delete_company(company['id'])
                                return 1
                        except:
                            pass
        except:
            pass
        return 0
    
    def cleanup_specific_person(self, person_id=None):
        """Limpa uma pessoa específica ou a pessoa de teste"""
        target_id = person_id or self.test_data.get('person_id')
        
        if not target_id:
            print(" Nenhum ID de pessoa fornecido para limpeza")
            return False
        
        print(f" Limpando pessoa ID: {target_id}")
        
        try:
            # Tentar deletar diretamente se o método existir
            if callable(getattr(self.db, 'delete_person', None)):
                result = self.db.delete_person(target_id)
                print(f"  [OK] Pessoa {target_id} deletada")
                return True
            
            # Alternativa: editar para marcar como removida
            persons = self.db.get_persons(id=target_id)
            if persons and len(persons) > 0:
                person_data = persons[0]
                if callable(getattr(self.db, 'edit_person', None)):
                    # Criar pessoa "removida"
                    removed_person = Person(
                        name=f"[REMOVIDO TESTE] {person_data.get('name', '')}",
                        birth_date=person_data.get('birth_date', '01/01/1900'),
                        cpf="00000000000",  # CPF inválido para evitar conflitos
                        email=f"removido.{target_id}@teste.com",
                        phone_number="(00) 0000-0000"
                    )
                    
                    # Para SQLite, precisamos do requester_id
                    requester_id = person_data.get('requester_id', 0)
                    
                    # Tentar editar
                    self.db.edit_person(removed_person, self.test_address, target_id, requester_id)
                    print(f"  [OK] Pessoa {target_id} marcada como removida")
                    return True
            
            print(f"   Não foi possível limpar pessoa {target_id}")
            return False
            
        except Exception as e:
            print(f"  [FAIL] Erro ao limpar pessoa {target_id}: {e}")
            return False

    # ========== EXECUÇÃO DE TODOS OS TESTES ==========
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("\n" + "="*60)
        print("[ROCKET] INICIANDO TESTES COMPLETOS DO DATABASE")
        print("="*60)
        
        # Configurar dados de teste
        self.setup_test_data()
        
        # Executar testes na ordem
        tests = [
            # Testes básicos
            self.test_connection,
            self.test_login,
            
            # Testes de criação
            self.test_insert_person,
            self.test_insert_company,
            self.test_insert_property,
            self.test_insert_sample,
            
            # Testes de consulta
            self.test_get_persons,
            self.test_get_companies,
            self.test_get_requesters,
            self.test_get_properties,
            self.test_get_samples,
            self.test_get_sample_info,
            
            # Testes de edição
            self.test_edit_person,
            self.test_edit_property,
            self.test_edit_sample,
            
            # Testes auxiliares
            self.test_get_countries,
            self.test_get_states,
            self.test_get_cities,
            
            # Testes de laudo
            self.test_report_functionality,
            
            # Testes de exclusão (executar por último)
            self.test_delete_sample,
            self.test_delete_property,
        ]
        
        # Executar cada teste
        for test_func in tests:
            test_func()
        
        # Gerar relatório
        cleanup_count, cleanup_errors = self.cleanup_test_data()
        print(f"[OK] Limpeza concluída: {cleanup_count} itens removidos")
    
    def generate_report(self):
        """Gera relatório final dos testes"""
        print("\n" + "="*60)
        print(" RELATÓRIO FINAL DE TESTES")
        print("="*60)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['passed'])
        failed = total - passed
        
        print(f"\n ESTATÍSTICAS:")
        print(f"   Total de testes: {total}")
        print(f"   Testes passados: {passed} ({passed/total*100:.1f}%)")
        print(f"   Testes falhados: {failed} ({failed/total*100:.1f}%)")
        
        if failed > 0:
            print(f"\n[FAIL] TESTES QUE FALHARAM:")
            for test in self.test_results:
                if not test['passed']:
                    print(f"   [FAIL] {test['name']}")
                    if test['message']:
                        print(f"     Mensagem: {test['message']}")
        
        print(f"\n[OK] TESTES QUE PASSARAM ({passed}):")
        passed_tests = [t['name'] for t in self.test_results if t['passed']]
        for i, name in enumerate(passed_tests[:10]):  # Mostrar apenas os primeiros 10
            print(f"   [OK] {name}")
        
        if passed > 10:
            print(f"   ... e mais {passed - 10} testes")
        
        print("\n" + "="*60)
        
        # Salvar relatório em arquivo
        self.save_report_to_file()
        
        return passed == total
    
    def save_report_to_file(self):
        """Salva relatório em arquivo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{'API' if self.use_api else 'SQLite'}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"RELATÓRIO DE TESTES - {'API Django' if self.use_api else 'SQLite Local'}\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            
            total = len(self.test_results)
            passed = sum(1 for r in self.test_results if r['passed'])
            
            f.write(f"ESTATÍSTICAS:\n")
            f.write(f"  Total de testes: {total}\n")
            f.write(f"  Testes passados: {passed}\n")
            f.write(f"  Testes falhados: {total - passed}\n")
            f.write(f"  Taxa de sucesso: {passed/total*100:.1f}%\n\n")
            
            f.write("DETALHES DOS TESTES:\n")
            for test in self.test_results:
                status = "PASS" if test['passed'] else "FAIL"
                f.write(f"  [{status}] {test['name']}\n")
                if test['message']:
                    f.write(f"      {test['message']}\n")
        
        print(f" Relatório salvo em: {filename}")


# ========== FUNÇÃO PRINCIPAL ==========

def main():
    """Função principal para executar testes"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Testar compatibilidade do Database")
    parser.add_argument('--mode', choices=['api', 'sqlite', 'both'], default='api',
                       help='Modo de teste: api, sqlite ou ambos')
    parser.add_argument('--verbose', action='store_true', default=True,
                       help='Mostrar detalhes dos testes')
    parser.add_argument('--clean', action='store_true',
                       help='Limpar dados de teste após execução')
    parser.add_argument('--no-clean', dest='clean', action='store_false',
                       help='Não limpar dados de teste após execução')
    
    args = parser.parse_args()

    testers = []
    
    if args.mode in ['api', 'both']:
        print("\n" + "="*60)
        print(" TESTANDO MODO API DJANGO")
        print("="*60)
        
        tester_api = DatabaseTester(use_api=True, verbose=args.verbose)
        success_api = tester_api.run_all_tests()
        testers.append(tester_api)
        
    
    if args.mode in ['sqlite', 'both']:
        print("\n" + "="*60)
        print(" TESTANDO MODO SQLITE LOCAL")
        print("="*60)
        
        tester_sqlite = DatabaseTester(use_api=False, verbose=args.verbose)
        success_sqlite = tester_sqlite.run_all_tests()
        testers.append(tester_sqlite)
    
     # Limpar dados se solicitado
    if args.clean and testers:
        print("\n" + "="*60)
        print(" LIMPEZA DE DADOS DE TESTE")
        print("="*60)
        
        for tester in testers:
            mode = "API Django" if tester.use_api else "SQLite Local"
            print(f"\nLimpando dados do modo: {mode}")
            cleanup_count, cleanup_errors = tester.cleanup_test_data()
    
    if args.mode == 'both':
        print("\n" + "="*60)
        print(" COMPARAÇÃO ENTRE MODOS")
        print("="*60)
        
        print("\nComparação concluída. Verifique os relatórios individuais.")


if __name__ == "__main__":
    # Executar em modo API por padrão
    print("[ROCKET] Iniciando testes do Database...")
    
    # Teste rápido apenas com API
    tester = DatabaseTester(use_api=True, verbose=True)
    tester.run_all_tests()