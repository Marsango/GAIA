# Novo Database.py para software desktop (API Django)
import requests
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
import time
from backend.classes.Sample import Sample
from backend.classes.Report import Report
from backend.classes.Person import Person
from backend.classes.Address import Address
from backend.classes.Company import Company
from backend.classes.Property import Property
from backend.classes.exceptions import CNPJAlreadyExistsError
from backend.classes.utils import *

# class DatabaseAPI:
#     """Vers?o adaptada para comunica??o com API Django"""
    
#     def __init__(self, api_url: str = "http://localhost:8000"):
#         self.api_url = api_url.rstrip('/')
#         self.token: Optional[str] = None
#         self.headers = {
#             "Content-Type": "application/json",
#             "User-Agent": "GAIA Desktop/2.0"
#         }
#         self.session = requests.Session()
#         self.session.timeout = 30

#         # Credenciais padr?o para testes
#         self.TECH_CPF = "999.888.777-00"  # CPF do t?cnico
#         self.TECH_PASSWORD = "123456"
        
#     # ========== AUTENTICA??O ==========

#     def login(self, cpf: str = None, password: str = None) -> bool:
#         """Login autom?tico com credenciais t?cnicas"""
#         try:
#             # Usar credenciais padr?o se n?o fornecidas
#             login_cpf = cpf or self.TECH_CPF
#             login_password = password or self.TECH_PASSWORD
            
#             # Tentar login com CPF
#             response = self.session.post(
#                 f"{self.api_url}/api/token/",
#                 json={"cpf": login_cpf, "password": login_password}
#             )
            
#             # Se endpoint com CPF n?o existir, tentar username padr?o
#             if response.status_code == 404:
#                 response = self.session.post(
#                     f"{self.api_url}/api/token/",
#                     json={"username": "tecnico_lab", "password": login_password}
#                 )
            
#             if response.status_code == 200:
#                 data = response.json()
#                 self.token = data.get("access")
#                 self.headers["Authorization"] = f"Bearer {self.token}"
#                 print(f"[OK] Login autom?tico realizado (CPF: {login_cpf})")
#                 return True
            
#             print(f"[FAIL] Falha no login: {response.status_code}")
#             return False
            
#         except Exception as e:
#             print(f"[FAIL] Erro no login autom?tico: {e}")
#             return False
    
#     def _get_current_user(self) -> Optional[Dict]:
#         """Obt?m informa??es do usu?rio atual"""
#         try:
#             response = self.session.get(
#                 f"{self.api_url}/api/token/verify/",
#                 headers=self.headers
#             )
#             if response.status_code == 200:
#                 # Buscar detalhes completos do usu?rio
#                 response = self.session.get(
#                     f"{self.api_url}/api/usuarios/me/",  # Voc? precisa criar este endpoint
#                     headers=self.headers
#                 )
#                 if response.status_code == 200:
#                     return response.json()
#         except:
#             pass
#         return None
    
#     # ========== M?TODOS GEN?RICOS ==========
    
#     def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Any:
#         """M?todo gen?rico para requisi??es HTTP"""
#         try:
#             url = f"{self.api_url}{endpoint}"
#             headers = self.headers.copy()
            
#             response = self.session.request(
#                 method=method.upper(),
#                 url=url,
#                 headers=headers,
#                 json=data,
#                 params=params,
#                 timeout=30
#             )
            
#             # Tratar erros comuns
#             if response.status_code == 401:
#                 print("Erro 401: Token expirado ou inv?lido")
#                 return None
#             elif response.status_code == 403:
#                 print("Erro 403: Acesso negado")
#                 return None
#             elif response.status_code == 404:
#                 print(f"Erro 404: Endpoint n?o encontrado: {endpoint}")
#                 return None
#             elif response.status_code >= 500:
#                 print(f"Erro {response.status_code}: Servidor com problemas")
#                 return None
            
#             if response.status_code == 204:  # No Content
#                 return True
            
#             return response.json() if response.content else None
            
#         except Exception as e:
#             print(f"Erro na requisi??o {method} {endpoint}: {e}")
#             return None
    
#     # ========== PROPRIEDADES (COMPAT?VEL) ==========
    
#     def insert_property(self, property: Property, requester_id: int) -> Optional[int]:
#         """Insere propriedade - Mant?m compatibilidade com c?digo existente"""
#         # Converter Property para dict compat?vel com API Django
#         property_dict = to_dict(property)
        
#         # Mapear campos do sistema antigo para o novo
#         data = {
#             "name": property_dict.get("name", ""),
#             "localizacao": property_dict.get("location", ""),
#             "registration_number": property_dict.get("registration_number"),
#             "cpf_cnpj": property_dict.get("cpf_cnpj", ""),  # Se houver no Property
#         }
        
#         result = self._make_request("POST", "/api/propriedades/", data=data)
#         return result.get("id") if result else None
    
#     def get_properties(self, **kwargs) -> List[Dict]:
#         """Busca propriedades - Mant?m mesma interface"""
#         params = {}
        
#         # Mapear par?metros do sistema antigo para novo
#         if kwargs.get('requester_id'):
#             # No Django, propriedades s?o automaticamente filtradas pelo usu?rio logado
#             pass
#         elif kwargs.get('id'):
#             params['id'] = kwargs['id']
        
#         result = self._make_request("GET", "/api/propriedades/", params=params)
        
#         if result and isinstance(result, list):
#             # Converter formato Django para formato compat?vel
#             converted = []
#             for prop in result:
#                 converted.append({
#                     'id': prop.get('id'),
#                     'name': prop.get('name'),
#                     'location': prop.get('localizacao'),
#                     'registration_number': prop.get('registration_number'),
#                     'city': prop.get('localizacao'),
#                     'state': '', 
#                     'country': 'Brasil'
#                 })
#             return converted
#         return []
    
#     def edit_property(self, property: Property, property_id: int) -> bool:
#         """Edita propriedade"""
#         property_dict = to_dict(property)
        
#         data = {
#             "name": property_dict.get("name", ""),
#             "localizacao": property_dict.get("location", ""),
#             "registration_number": property_dict.get("registration_number"),
#             "cpf_cnpj": property_dict.get("cpf_cnpj", ""),
#         }
        
#         result = self._make_request("PUT", f"/api/propriedades/{property_id}/", data=data)
#         return result is not None
    
#     def delete_property(self, id: int) -> bool:
#         """Exclui propriedade (na verdade desativa)"""
#         # Em vez de DELETE, vamos desativar
#         result = self._make_request("PATCH", f"/api/propriedades/{id}/", data={"ativo": False})
#         return result is not None
    
#     # ========== AMOSTRAS (SAMPLES) - Equivalente a Laudos ==========
    
#     def insert_sample(self, sample: Sample, property_id: int, sample_number: int) -> Optional[int]:
#         """Insere amostra - Equivalente ao insert_sample antigo"""
#         sample_dict = to_dict(sample)
        
#         # Converter data se necess?rio
#         collection_date = sample_dict.get("collection_date")
#         if collection_date and isinstance(collection_date, str):
#             try:
#                 # Tenta converter formato
#                 datetime.strptime(collection_date, "%d/%m/%Y")
#             except ValueError:
#                 pass
        
#         # Mapear campos para API Django
#         data = {
#             "propriedade": property_id,
#             "numero_amostra": sample_number,
#             "data_coleta": collection_date,
#             "descricao": sample_dict.get("description", ""),
#             "ph": sample_dict.get("ph"),
#             "fosforo": sample_dict.get("phosphorus"),
#             "potassio": sample_dict.get("potassium"),
#             "materia_organica": sample_dict.get("organic_matter"),
#             "argila": sample_dict.get("clay"),
#             "silte": sample_dict.get("silte"),
#             "areia": sample_dict.get("sand"),
#             "classificacao": sample_dict.get("classification"),
#             # Adicionar outros campos conforme necess?rio
#         }
        
#         result = self._make_request("POST", "/api/amostras/criar_simples/", data=data)
#         return result.get("id") if result else None
    
#     def get_samples(self, **kwargs) -> List[Dict]:
#         """Busca amostras - Mant?m mesma interface"""
#         params = {}
        
#         if kwargs.get('property_id'):
#             params['propriedade'] = kwargs['property_id']
#         elif kwargs.get('sample_id'):
#             params['id'] = kwargs['sample_id']
#         elif kwargs.get('id_list'):
#             # Buscar m?ltiplas amostras
#             samples = []
#             for sample_id in kwargs['id_list']:
#                 result = self._make_request("GET", f"/api/amostras/{sample_id}/")
#                 if result:
#                     samples.append(self._convert_sample_format(result))
#             return samples
        
#         result = self._make_request("GET", "/api/amostras/", params=params)
        
#         if result and isinstance(result, list):
#             return [self._convert_sample_format(sample) for sample in result]
#         return []
    
#     def _convert_sample_format(self, sample: Dict) -> Dict:
#         """Converte formato Django para formato compat?vel"""
#         return {
#             'id': sample.get('id'),
#             'sample_number': sample.get('numero_amostra'),
#             'description': sample.get('descricao'),
#             'collection_date': sample.get('data_coleta'),
#             'total_area': sample.get('area_total'),
#             'latitude': sample.get('latitude'),
#             'longitude': sample.get('longitude'),
#             'depth': sample.get('profundidade'),
#             'phosphorus': sample.get('fosforo'),
#             'potassium': sample.get('potassio'),
#             'organic_matter': sample.get('materia_organica'),
#             'ph': sample.get('ph'),
#             'clay': sample.get('argila'),
#             'silte': sample.get('silte'),
#             'sand': sample.get('areia'),
#             'classification': sample.get('classificacao'),
#             'fk_property_id': sample.get('propriedade')
#         }
    
#     def edit_sample(self, sample: Sample, sample_id: int) -> bool:
#         """Edita amostra"""
#         sample_dict = to_dict(sample)
        
#         data = {
#             "descricao": sample_dict.get("description", ""),
#             "data_coleta": sample_dict.get("collection_date"),
#             "ph": sample_dict.get("ph"),
#             "fosforo": sample_dict.get("phosphorus"),
#             "potassio": sample_dict.get("potassium"),
#             "materia_organica": sample_dict.get("organic_matter"),
#             "argila": sample_dict.get("clay"),
#             "silte": sample_dict.get("silte"),
#             "areia": sample_dict.get("sand"),
#             "classificacao": sample_dict.get("classification"),
#         }
        
#         result = self._make_request("PUT", f"/api/amostras/{sample_id}/", data=data)
#         return result is not None
    
#     def delete_sample(self, id: int) -> bool:
#         """Exclui amostra (desativa)"""
#         result = self._make_request("PATCH", f"/api/amostras/{id}/", data={"ativo": False})
#         return result is not None
    
#     def get_sample_info(self, sample_id: int) -> Optional[Dict]:
#         """Obt?m informa??es completas da amostra"""
#         # Primeiro pega a amostra
#         sample = self._make_request("GET", f"/api/amostras/{sample_id}/")
#         if not sample:
#             return None
        
#         # Pega a propriedade associada
#         property_id = sample.get('propriedade')
#         if property_id:
#             property_info = self._make_request("GET", f"/api/propriedades/{property_id}/")
#         else:
#             property_info = None
        
#         # Formatar resposta compat?vel
#         return {
#             'sample_description': sample.get('descricao'),
#             'sample_number': sample.get('numero_amostra'),
#             'collection_date': sample.get('data_coleta'),
#             'depth': sample.get('profundidade'),
#             'total_area': sample.get('area_total'),
#             'property_name': property_info.get('name') if property_info else '',
#             'registration_number': property_info.get('registration_number') if property_info else None,
#             # Adicionar mais campos conforme necess?rio
#         }
    
#     # ========== LAUDOS (REPORTS - PDFs) ==========
    
#     def insert_report(self, report: Report, sample_id: int) -> Optional[int]:
#         """Insere laudo (PDF)"""
#         report_dict = to_dict(report)
        
#         data = {
#             "numero_amostra": sample_id,  # Usar n?mero da amostra
#             "data_coleta": datetime.now().strftime("%Y-%m-%d"),
#             "propriedade": self._get_property_from_sample(sample_id),
#             "ativo": True
#         }
        
#         result = self._make_request("POST", "/api/laudos/", data=data)
        
#         if result and 'id' in result:
#             # Fazer upload do arquivo PDF se houver
#             file_location = report_dict.get("file_location")
#             if file_location:
#                 self._upload_report_pdf(result['id'], file_location)
            
#             return result['id']
        
#         return None
    
#     def _get_property_from_sample(self, sample_id: int) -> Optional[int]:
#         """Obt?m ID da propriedade a partir da amostra"""
#         sample = self._make_request("GET", f"/api/amostras/{sample_id}/")
#         return sample.get('propriedade') if sample else None
    
#     def _upload_report_pdf(self, laudo_id: int, file_path: str) -> bool:
#         """Faz upload do arquivo PDF para o laudo"""
#         try:
#             with open(file_path, 'rb') as f:
#                 files = {'arquivo_pdf': f}
                
#                 # Remover header JSON para upload de arquivo
#                 headers = {k: v for k, v in self.headers.items() if k != 'Content-Type'}
                
#                 response = self.session.post(
#                     f"{self.api_url}/api/laudos/{laudo_id}/upload_pdf/",
#                     files=files,
#                     headers=headers
#                 )
                
#                 return response.status_code == 200
#         except Exception as e:
#             print(f"Erro ao fazer upload do PDF: {e}")
#             return False
    
#     def get_report_info(self) -> List[Dict]:
#         """Obt?m informa??es dos laudos"""
#         result = self._make_request("GET", "/api/laudos/")
        
#         if result and isinstance(result, list):
#             converted = []
#             for report in result:
#                 converted.append({
#                     'id': report.get('id'),
#                     'requester_name': 'A definir',  # Precisa buscar do relacionamento
#                     'date': report.get('data_coleta'),
#                     'property': 'A definir'  # Precisa buscar do relacionamento
#                 })
#             return converted
#         return []
    
#     # ========== PESSOAS E EMPRESAS ==========
    
#     def insert_person(self, person: Person, address: Address) -> Optional[int]:
#         """No Django, usu?rios s?o criados via admin ou API de registro"""
#         print("??  Cria??o de pessoas deve ser feita via interface web ou admin Django")
#         print(f"   Pessoa: {to_dict(person)}")
#         print(f"   Endere?o: {to_dict(address)}")
#         return None
    
#     def insert_person(self, person: Person, address: Address = None) -> Optional[Dict]:
#         """Cadastra pessoa com endere?o (como no software original)"""
#         try:
#             # Converter objetos para dict
#             person_dict = to_dict(person) if hasattr(person, '__dict__') else person
#             address_dict = to_dict(address) if address and hasattr(address, '__dict__') else address
            
#             # Preparar dados para API
#             data = {
#                 "name": person_dict.get("name", ""),
#                 "cpf": person_dict.get("cpf", ""),
#                 "email": person_dict.get("email", ""),
#                 "telefone": person_dict.get("phone_number", ""),
#                 "data_nascimento": person_dict.get("birth_date"),
#             }
            
#             # Se tem endere?o, adicionar
#             if address_dict:
#                 data["endereco"] = {
#                     "cep": address_dict.get("cep", ""),
#                     "rua": address_dict.get("street", address_dict.get("rua", "")),
#                     "numero": address_dict.get("address_number", address_dict.get("numero", "")),
#                     "cidade": address_dict.get("city", address_dict.get("cidade", "")),
#                     "estado": address_dict.get("state", address_dict.get("estado", "")),
#                     "pais": address_dict.get("country", "Brasil"),
#                 }
                
#                 # Usar endpoint que cria pessoa com endere?o
#                 result = self._make_request("POST", "/api/pessoas/criar_com_endereco/", data=data)
#             else:
#                 # Criar apenas pessoa
#                 result = self._make_request("POST", "/api/pessoas/", data=data)
            
#             return result if result else None
            
#         except Exception as e:
#             print(f"Erro ao cadastrar pessoa: {e}")
#             return None
    
#     def insert_company(self, company: Company, address: Address) -> Optional[Dict]:
#         """Cadastra empresa com endere?o"""
#         try:
#             company_dict = to_dict(company)
#             address_dict = to_dict(address)
            
#             # Criar endere?o primeiro
#             endereco_data = {
#                 "cep": address_dict.get("cep", ""),
#                 "rua": address_dict.get("street", ""),
#                 "numero": address_dict.get("address_number", ""),
#                 "cidade": address_dict.get("city", ""),
#                 "estado": address_dict.get("state", ""),
#                 "pais": address_dict.get("country", "Brasil"),
#             }
            
#             endereco_result = self._make_request("POST", "/api/enderecos/", data=endereco_data)
            
#             if not endereco_result:
#                 print("[FAIL] Falha ao criar endere?o")
#                 return None
            
#             endereco_id = endereco_result.get("id")
            
#             # Criar empresa
#             empresa_data = {
#                 "name": company_dict.get("company_name", ""),
#                 "cnpj": company_dict.get("cnpj", ""),
#                 "email": company_dict.get("email", ""),
#                 "telefone": company_dict.get("phone_number", ""),
#                 "endereco": endereco_id,
#             }
            
#             empresa_result = self._make_request("POST", "/api/empresas/", data=empresa_data)
            
#             return empresa_result if empresa_result else None
            
#         except Exception as e:
#             print(f"Erro ao cadastrar empresa: {e}")
#             return None
    
#     # ========== M?TODOS DE COMPATIBILIDADE ==========
    
#     def close_connection(self) -> None:
#         """Fecha sess?o HTTP"""
#         self.session.close()
    
#     def get_countries(self) -> List[str]:
#         """Pa?ses dispon?veis"""
#         # Pode retornar lista fixa ou buscar do Django
#         return ["Brasil"]
    
#     def get_states(self, country: str) -> List[str]:
#         """Estados dispon?veis"""
#         # Lista de estados brasileiros
#         return [
#             "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
#             "MT", "MS", "MG", "PA", "PB", "Paran?", "PR", "PE", "PI", "RJ", "RN", 
#             "Rio Grande do Sul", "RS", "RO", "RR", "SC", "Santa Catarina", "SP", "SE", "TO"
#         ]
    
#     def get_cities(self, state: str) -> List[str]:
#         """Cidades dispon?veis - pode ser simplificado"""
#         # Retorna lista gen?rica ou busca de API externa
#         return ["Cidade Principal", "Outra Cidade"]
    
#     def get_streets(self, city: str) -> List[str]:
#         """Ruas dispon?veis - simplificado"""
#         return ["Rua Principal", "Avenida Central"]
    
#     # ========== TESTE DE CONEX?O ==========
    
#     def test_connection(self) -> bool:
#         """Testa se a API est? respondendo"""
#         try:
#             response = self.session.get(f"{self.api_url}/api/health/", timeout=5)
#             return response.status_code == 200
#         except:
#             return False


# ========== WRAPPER PARA COMPATIBILIDADE ==========

class Database:
    """Wrapper para manter compatibilidade total com código existente"""
    
    def __init__(self, use_api: bool = True, api_url: str = "http://localhost:8000"):
        self.use_api = use_api
        
        if use_api:
            from backend.classes.DatabaseHTTPWrapper import DatabaseHTTPWrapper
            self.db = DatabaseHTTPWrapper()
            print("[API] Modo API Django ativado")
    
    # ========== DELEGA??O DE M?TODOS ==========
    
    def login(self, cpf: str, password: str) -> bool:
        """Login compat?vel"""
        if hasattr(self.db, 'login'):
            return self.db.login(cpf, password)
        return False
    
    def insert_property(self, property: Property, requester_id: int, address: Address) -> None:
        """Insere propriedade - Mant?m assinatura original"""
        if hasattr(self.db, 'insert_property'):
            result = self.db.insert_property(property, requester_id, address)
            # O m?todo original n?o retorna nada, apenas commit
            return
        raise NotImplementedError("M?todo n?o implementado")
    
    def get_properties(self, **kwargs) -> list:
        """Busca propriedades - Mant?m formato original"""
        if hasattr(self.db, 'get_properties'):
            result = self.db.get_properties(**kwargs)
            # Converter para sqlite3.Row se necess?rio
            return self._convert_to_sqlite_format(result)
        return []
    def _convert_to_sqlite_format(self, data: List[Dict]) -> list:
        """Converte dict para formato similar a sqlite3.Row"""
        # Se j? s?o objetos com __getitem__, retorna como est?
        if data and hasattr(data[0], '__getitem__'):
            return data

        # Esta ? uma simplifica??o. Pode precisar de mais ajustes.
        class MockRow:
            def __init__(self, data):
                self._data = data

            def __getitem__(self, key):
                return self._data.get(key)

            def keys(self):
                return self._data.keys()

        return [MockRow(item) for item in data]
    # ========== DELEGAR TODOS OS OUTROS M?TODOS ==========
    
    def __getattr__(self, name):
        """Delega métodos não implementados para o backend atual"""
        return getattr(self.db, name)


# ========== FÁBRICA PARA ESCOLHA AUTOMÁTICA ==========
def create_database(force_api: bool = False) -> Database:
        """Usa sempre o wrapper compativel"""
        return Database(use_api=True) 


# ========== TESTE ==========
if __name__ == "__main__":
    print("=== Teste do Database API ===")
    
    # Criar inst?ncia
    db = create_database()
    
    # Testar conex?o
    if hasattr(db.db, 'test_connection'):
        if db.db.test_connection():
            print("[OK] Conexao com API OK")
        else:
            print("[FAIL] API nao responde")
    
    # Testar login
    if db.login("admin", "admin123"):
        print("[OK] Login realizado")
        
        # Testar propriedades
        props = db.get_properties()
        print(f"[OK] {len(props)} propriedade(s) encontrada(s)")
    else:
        print("[FAIL] Falha no login")