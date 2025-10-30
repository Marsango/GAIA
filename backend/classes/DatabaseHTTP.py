import requests
import json
from backend.classes.Sample import Sample
from backend.classes.Report import Report
from backend.classes.Person import Person
from backend.classes.Address import Address
from backend.classes.Company import Company
from backend.classes.Property import Property
from backend.classes.exceptions import CNPJAlreadyExistsError

class DatabaseHTTP:
    def __init__(self):
        self.base_url = "http://localhost:8000/api"  # URL do seu Django
        self.headers = {'Content-Type': 'application/json'}
    
    # ========== PESSOAS ==========
    
    def insert_person(self, person: Person, address: Address) -> None:
        """Cadastra pessoa via API (substitui SQLite)"""
        try:
            data = {
                'username': person.cpf,
                'cpf': person.cpf,
                'first_name': person.name.split(' ')[0] if person.name else '',
                'last_name': ' '.join(person.name.split(' ')[1:]) if person.name else '',
                'email': getattr(person, 'email', ''),
                'telefone': getattr(person, 'phone_number', ''),
                'password': '123456'  # Senha padrão
            }
            
            response = requests.post(
                f"{self.base_url}/auth/sync/usuario/",
                json=data,
                headers=self.headers
            )
            
            result = response.json()
            
            if response.status_code == 201:
                print(f"✅ Pessoa {person.name} cadastrada com sucesso")
            elif response.status_code == 200 and result.get('status') == 'exists':
                print(f"⚠️ Pessoa {person.name} já existe")
            else:
                raise Exception(f"Erro API: {result.get('error', 'Erro desconhecido')}")
                
        except Exception as e:
            print(f"❌ Erro ao cadastrar pessoa: {e}")
            raise

    def get_persons(self, **kwargs) -> list:
        """Busca pessoas - por enquanto retorna lista vazia"""
        # Implementar depois quando criar API de consulta
        return []

    # ========== PROPRIEDADES ==========
    
    def insert_property(self, property: Property, requester_id: int) -> None:
        """Cadastra propriedade via API"""
        try:
            # PRECISAMOS DO CPF DO PROPRIETÁRIO
            # Por enquanto, vamos usar um CPF fixo ou pedir no software
            proprietario_cpf = "12345678901"  # ← TEMPORÁRIO - ajustar depois
            
            data = {
                'nome': property.name,
                'localizacao': property.location,
                'proprietario_cpf': proprietario_cpf
            }
            
            response = requests.post(
                f"{self.base_url}/sync/propriedade/",
                json=data,
                headers=self.headers
            )
            
            result = response.json()
            
            if response.status_code == 201:
                print(f"✅ Propriedade {property.name} cadastrada com sucesso")
                return result['id']
            else:
                raise Exception(f"Erro API: {result.get('error', 'Erro desconhecido')}")
                
        except Exception as e:
            print(f"❌ Erro ao cadastrar propriedade: {e}")
            raise

    def get_properties(self, **kwargs) -> list:
        """Busca propriedades - por enquanto retorna lista vazia"""
        return []

    # ========== AMOSTRAS/LAUDOS ==========
    
    def insert_sample(self, sample: Sample, property_id: int, sample_number: int) -> None:
        """Cadastra amostra/laudo via API"""
        try:
            # PRECISAMOS DO NOME DA PROPRIEDADE E CPF DO PROPRIETÁRIO
            # Por enquanto, vamos usar valores temporários
            propriedade_nome = "Fazenda Temporária"  # ← TEMPORÁRIO
            proprietario_cpf = "12345678901"         # ← TEMPORÁRIO
            
            data = {
                'numero_amostra': sample_number,
                'data_coleta': sample.collection_date,
                'propriedade_nome': propriedade_nome,
                'proprietario_cpf': proprietario_cpf,
                'arquivo_pdf': f"/laudos/amostra_{sample_number}.pdf"  # ← Caminho temporário
            }
            
            response = requests.post(
                f"{self.base_url}/sync/laudo/",
                json=data,
                headers=self.headers
            )
            
            result = response.json()
            
            if response.status_code == 201:
                print(f"✅ Amostra {sample_number} cadastrada com sucesso")
                return result['id']
            else:
                raise Exception(f"Erro API: {result.get('error', 'Erro desconhecido')}")
                
        except Exception as e:
            print(f"❌ Erro ao cadastrar amostra: {e}")
            raise

    def insert_report(self, report: Report, sample_id: int) -> None:
        """Cadastra relatório PDF - por enquanto só log"""
        print(f"📄 Relatório para amostra {sample_id} - Arquivo: {report.file_location}")
        # Implementar upload de arquivo depois

    # ========== EMPRESAS ==========
    
    def insert_company(self, company: Company, address: Address) -> None:
        """Cadastra empresa - por enquanto não implementado"""
        print(f"🏢 Empresa {company.company_name} - Implementar depois")
        # Implementar quando criar API para empresas

    # ========== MÉTODOS QUE NÃO PRECISAM DE HTTP ==========
    
    def create_database(self) -> None:
        """Não precisa mais criar banco local"""
        pass

    def close_connection(self):
        """Conexões HTTP são stateless"""
        pass

    def get_countries(self) -> list[str]:
        """Países - retorna lista fixa por enquanto"""
        return ["Brasil"]

    def get_states(self, country: str) -> list[str]:
        """Estados - retorna lista fixa por enquanto"""
        return ["Santa Catarina", "Paraná", "Rio Grande do Sul"]

    def get_cities(self, state: str) -> list[str]:
        """Cidades - retorna lista fixa por enquanto"""
        return ["Concórdia", "Marmeleiro", "Francisco Beltrão"]
    
    def get_streets(self, city: str) -> list[str]:
        """Ruas - retorna lista fixa por enquanto"""
        return ["Rua Principal", "Avenida Central", "Travessa da Paz", "Rua das Flores", "Avenida Brasil"]
