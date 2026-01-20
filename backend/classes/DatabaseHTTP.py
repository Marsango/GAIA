#nao sendo utilizada

import requests
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from backend.classes.Sample import Sample
from backend.classes.Report import Report
from backend.classes.Person import Person
from backend.classes.Address import Address
from backend.classes.Company import Company
from backend.classes.Property import Property
from backend.classes.exceptions import CNPJAlreadyExistsError
from backend.classes.utils import to_dict  # Assumindo que existe

class DatabaseHTTP:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.token: Optional[str] = None
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'GAIA-Software-Desktop/1.0'
        }
        self.session = requests.Session()
        
        # Credenciais fixas para software desktop
        self.TECH_CPF = "99988877700"  # ← CPF do técnico (sem formatação para API)
        self.TECH_PASSWORD = "123456"   # ← Senha do técnico
        
        # Auto login ao iniciar
        self._auto_login()
    
    def _format_date(self, date_str: str) -> str:
        """Converte data para formato YYYY-MM-DD esperado pela API"""
        if not date_str:
            return None

        try:
            # Aceita datetime/date diretamente
            if hasattr(date_str, "strftime"):
                return date_str.strftime("%Y-%m-%d")

            # Tenta parse de diferentes formatos (inclui ano com 2 dígitos)
            formats = [
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%d/%m/%y",
                "%d-%m-%Y",
                "%d-%m-%y",
                "%Y/%m/%d",
            ]

            for fmt in formats:
                try:
                    parsed = datetime.strptime(str(date_str), fmt)
                    return parsed.strftime("%Y-%m-%d")
                except ValueError:
                    continue

            # Se nenhum formato funcionou, retorna original (API validará)
            return str(date_str)
        except Exception:
            return str(date_str)
    
    def _auto_login(self) -> bool:
        """Login automático com credenciais técnicas - VERSÃO CORRIGIDA"""
        try:
            # ÚNICO endpoint que funciona: /api/login/cpf/ com campo "cpf"
            response = self.session.post(
                f"{self.base_url}/api/login/cpf/",
                json={
                    "cpf": self.TECH_CPF,  # Campo é "cpf", não "username"
                    "password": self.TECH_PASSWORD
                },
                timeout=10
            )
            
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access")
                if self.token:
                    self.headers["Authorization"] = f"Bearer {self.token}"
                    print(f"✅ Login automático realizado!")
                    print(f"   Token: {self.token[:50]}...")
                    
                    # Verificar se token funciona
                    self._verify_token()
                    return True
                else:
                    print(f"❌ Token não encontrado na resposta")
                    print(f"   Resposta: {data}")
                    return False
            
            elif response.status_code == 401:
                print(f"❌ Credenciais inválidas")
                print(f"   Verifique se o usuário existe e a senha está correta")
                
                # Debug da resposta
                try:
                    error_data = response.json()
                    print(f"   Erro detalhado: {error_data}")
                except:
                    print(f"   Resposta: {response.text[:200]}")
                    
                return False
            
            else:
                print(f"❌ Status inesperado: {response.status_code}")
                print(f"   Resposta: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no login automático: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    def _verify_token(self):
        """Verifica se o token funciona"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/health/",
                headers=self.headers,
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ Token verificado com sucesso")
                return True
            else:
                print(f"❌ Token inválido. Status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao verificar token: {e}")
            return False
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Any:
        """Método genérico para requisições HTTP - VERSÃO CORRIGIDA"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            # Se não tem token, tentar login primeiro
            if not self.token:
                print("⚠️  Sem token, tentando login...")
                if not self._auto_login():
                    return None
            
            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=30
            )
            
            print(f"[HTTP {method} {endpoint}] Status: {response.status_code}")
            
            if response.status_code == 401:
                print("🔑 Token expirado ou inválido, tentando relogin...")
                if self._auto_login():
                    # Repetir requisição com novo token
                    return self._make_request(method, endpoint, data, params)
                return None
            
            if response.status_code in [200, 201]:
                return response.json() if response.content else True
            
            if response.status_code == 204:  # No Content
                return True
            
            # Erros
            if response.status_code == 404:
                print(f"❌ Endpoint não encontrado: {endpoint}")
            elif response.status_code >= 400:
                try:
                    error_data = response.json()
                    print(f"❌ Erro {response.status_code}: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"❌ Erro {response.status_code}: {response.text[:200]}")
            
            return None
            
        except Exception as e:
            print(f"❌ Erro na requisição {method} {endpoint}: {e}")
            return None
    
    # ========== PESSOAS (CLIENTES) ==========
    
    def insert_person(self, person: Person, address: Address = None) -> Optional[int]:
        """Cadastra pessoa - VERSÃO CORRIGIDA"""
        try:
            print(f"\n➕ Cadastrando nova pessoa...")
            
            # Converter objetos para dict
            person_dict = to_dict(person)
            address_dict = to_dict(address) if address else {}
            
            # DEBUG: Verificar dados
            print(f"DEBUG Pessoa dict: {person_dict}")
            print(f"DEBUG Endereço dict: {address_dict}")
            
            # 1. Validar campos obrigatórios
            required_fields = ['name', 'cpf']
            missing_fields = [field for field in required_fields if not person_dict.get(field)]
            
            if missing_fields:
                print(f"❌ Campos obrigatórios faltando: {missing_fields}")
                return None
            
            # 2. Criar endereço primeiro (se fornecido)
            endereco_id = None
            if address_dict and any(address_dict.values()):
                print(f"🔨 Criando endereço...")
                
                endereco_data = {
                    "cep": address_dict.get("cep", ""),
                    "rua": address_dict.get("street", ""),
                    "numero": address_dict.get("address_number", ""),
                    "cidade": address_dict.get("city", ""),
                    "estado": address_dict.get("state", ""),
                    "pais": address_dict.get("country", "Brasil"),
                }
                
                # Remover campos vazios
                endereco_data = {k: v for k, v in endereco_data.items() if v}
                
                print(f"DEBUG Endereço para API: {endereco_data}")
                
                endereco_result = self._make_request("POST", "/api/enderecos/", data=endereco_data)
                
                if endereco_result and 'id' in endereco_result:
                    endereco_id = endereco_result['id']
                    print(f"✅ Endereço criado (ID: {endereco_id})")
                else:
                    print(f"❌ Falha ao criar endereço")
                    return None
            
            # 3. Criar pessoa
            print(f"👤 Criando pessoa...")
            
            pessoa_data = {
                "name": person_dict.get("name", ""),           # Campo deve ser "name"
                "cpf": person_dict.get("cpf", ""),            # Campo obrigatório
                "email": person_dict.get("email", ""),
                "phone_number": person_dict.get("phone_number", ""),
                "nascimento": self._format_date(person_dict.get("birth_date")),
            }
            
            # Adicionar endereço se criado
            if endereco_id:
                pessoa_data["endereco"] = endereco_id
            
            # Remover campos vazios
            pessoa_data = {k: v for k, v in pessoa_data.items() if v is not None and v != ""}
            
            print(f"DEBUG Pessoa para API: {pessoa_data}")
            
            pessoa_result = self._make_request("POST", "/api/pessoas/", data=pessoa_data)
            
            if pessoa_result and 'id' in pessoa_result:
                pessoa_id = pessoa_result['id']
                print(f"✅ Pessoa cadastrada com sucesso (ID: {pessoa_id})")
                return pessoa_id
            
            print(f"❌ Falha ao cadastrar pessoa")
            return None
            
        except Exception as e:
            print(f"❌ Erro ao cadastrar pessoa: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _convert_person_format(self, pessoa_data: Dict) -> Dict:
        """Converte pessoa do formato Django para formato do software"""
        if not pessoa_data:
            return {}
        
        # Buscar endereço completo se necessário
        endereco_completo = self._get_complete_address(pessoa_data.get('endereco'))
        
        # Mapeamento de campos
        return {
            'id': pessoa_data.get('id'),
            'name': pessoa_data.get('name', ''),
            'cpf': pessoa_data.get('cpf', ''),
            'email': pessoa_data.get('email', ''),
            'phone_number': pessoa_data.get('phone_number', ''),
            'birth_date': pessoa_data.get('nascimento', ''),
            
            # Endereço em formato do software
            'street': endereco_completo.get('rua', ''),
            'address_number': endereco_completo.get('numero', ''),
            'cep': endereco_completo.get('cep', ''),
            'city': endereco_completo.get('cidade', ''),
            'state': endereco_completo.get('estado', ''),
            'country': endereco_completo.get('pais', 'Brasil'),
            
            # Também manter campos originais para compatibilidade
            'rua': endereco_completo.get('rua', ''),
            'numero': endereco_completo.get('numero', ''),
            'cidade': endereco_completo.get('cidade', ''),
            'estado': endereco_completo.get('estado', ''),
            'pais': endereco_completo.get('pais', 'Brasil'),
        }
    
    def _get_complete_address(self, endereco_ref) -> Dict:
        """Obtém endereço completo, seja ID ou objeto"""
        if not endereco_ref:
            return {}
        
        # Se for um dicionário completo
        if isinstance(endereco_ref, dict):
            return endereco_ref
        
        # Se for apenas o ID (inteiro)
        if isinstance(endereco_ref, int):
            return self._make_request("GET", f"/api/enderecos/{endereco_ref}/") or {}
        
        return {}
    
    def _unwrap_results(self, response):
        """Extrai lista de resultados do DRF (paginação)"""
        if isinstance(response, dict) and "results" in response:
            return response["results"]
        if isinstance(response, list):
            return response
        if response:
            return [response]
        return []
    
    # ========== PROPRIEDADES ==========
    
    def insert_property(self, property: Property, requester_id: int) -> Optional[int]:
        """Cadastra propriedade"""
        try:
            property_dict = to_dict(property)
            
            data = {
                "nome": property_dict.get("name", ""),
                "localizacao": property_dict.get("localizacao", ""),
                "numero_registro": property_dict.get("registration_number"),
                "cpf_cnpj": property_dict.get("cpf_cnpj", ""),
                # proprietario é automaticamente o usuário logado (técnico)
            }
            
            result = self._make_request("POST", "/api/propriedades/", data=data)
            
            if result:
                prop_id = result.get("id")
                print(f"✅ Propriedade {data['nome']} cadastrada com ID: {prop_id}")
                return prop_id
            
            return None
            
        except Exception as e:
            print(f"❌ Erro ao cadastrar propriedade: {e}")
            return None
    
    def get_properties(self, **kwargs) -> List[Dict]:
        """Busca propriedades"""
        params = {}
        
        if kwargs.get('requester_id'):
            # No Django, propriedades são automaticamente filtradas por usuário
            pass
        elif kwargs.get('id'):
            # Buscar por ID específico
            result = self._make_request("GET", f"/api/propriedades/{kwargs['id']}/")
            return [result] if result else []
        
        result = self._make_request("GET", "/api/propriedades/", params=params)
        
        if result:
            converted = []
            for prop in result if isinstance(result, list) else [result]:
                converted.append({
                    'id': prop.get('id'),
                    'name': prop.get('nome'),
                    'location': prop.get('localizacao'),
                    'registration_number': prop.get('numero_registro'),
                    'cpf_cnpj': prop.get('cpf_cnpj'),
                    'proprietario': prop.get('proprietario'),
                })
            return converted
        return []
    
    # ========== AMOSTRAS ==========
    
    def insert_sample(self, sample: Sample, property_id: int, sample_number: int) -> Optional[int]:
        """Cadastra amostra (equivalente a laudo técnico)"""
        try:
            sample_dict = to_dict(sample)
            
            # Formatar data se necessário
            collection_date = sample_dict.get("collection_date")
            if collection_date and isinstance(collection_date, str):
                # Tentar converter formato brasileiro
                try:
                    from datetime import datetime
                    datetime.strptime(collection_date, "%d/%m/%Y")
                except ValueError:
                    pass  # Já está em formato correto
            
            data = {
                "propriedade": property_id,
                "numero_amostra": sample_number,
                "data_coleta": collection_date,
                "descricao": sample_dict.get("description", f"Amostra {sample_number}"),
                "ph": sample_dict.get("ph"),
                "fosforo": sample_dict.get("phosphorus"),
                "potassio": sample_dict.get("potassium"),
                "materia_organica": sample_dict.get("organic_matter"),
                "argila": sample_dict.get("clay"),
                "silte": sample_dict.get("silte"),
                "areia": sample_dict.get("sand"),
                "classificacao": sample_dict.get("classification"),
            }
            
            # Remover campos None
            data = {k: v for k, v in data.items() if v is not None}
            
            result = self._make_request("POST", "/api/amostras/criar_simples/", data=data)
            
            if result:
                amostra_id = result.get("id")
                print(f"✅ Amostra {sample_number} cadastrada com ID: {amostra_id}")
                return amostra_id
            
            return None
            
        except Exception as e:
            print(f"❌ Erro ao cadastrar amostra: {e}")
            return None
    
    def get_samples(self, **kwargs) -> List[Dict]:
        """Busca amostras"""
        params = {}
        
        if kwargs.get('property_id'):
            params['propriedade'] = kwargs['property_id']
        elif kwargs.get('sample_id'):
            # Buscar por ID específico
            result = self._make_request("GET", f"/api/amostras/{kwargs['sample_id']}/")
            return [result] if result else []
        
        result = self._make_request("GET", "/api/amostras/", params=params)
        
        if result:
            converted = []
            for amostra in result if isinstance(result, list) else [result]:
                converted.append({
                    'id': amostra.get('id'),
                    'sample_number': amostra.get('numero_amostra'),
                    'description': amostra.get('descricao'),
                    'collection_date': amostra.get('data_coleta'),
                    'ph': amostra.get('ph'),
                    'fosforo': amostra.get('fosforo'),
                    'potassio': amostra.get('potassio'),
                    'propriedade_id': amostra.get('propriedade'),
                })
            return converted
        return []
    
    # ========== LAUDOS (PDFs) ==========
    
    def insert_report(self, report: Report, sample_id: int) -> Optional[int]:
        """Cadastra laudo (PDF)"""
        try:
            report_dict = to_dict(report)
            
            # Primeiro, buscar amostra para obter dados
            amostra = self._make_request("GET", f"/api/amostras/{sample_id}/")
            if not amostra:
                print(f"❌ Amostra {sample_id} não encontrada")
                return None
            
            data = {
                "numero_amostra": amostra.get("numero_amostra"),
                "data_coleta": amostra.get("data_coleta"),
                "propriedade": amostra.get("propriedade"),
                "ativo": True,
            }
            
            result = self._make_request("POST", "/api/laudos/", data=data)
            
            if result:
                laudo_id = result.get("id")
                
                # Tentar upload do arquivo PDF se houver caminho
                file_location = report_dict.get("file_location")
                if file_location:
                    self._upload_pdf(laudo_id, file_location)
                
                print(f"✅ Laudo cadastrado com ID: {laudo_id}")
                return laudo_id
            
            return None
            
        except Exception as e:
            print(f"❌ Erro ao cadastrar laudo: {e}")
            return None
    
    def _upload_pdf(self, laudo_id: int, file_path: str) -> bool:
        """Faz upload do arquivo PDF"""
        try:
            with open(file_path, 'rb') as f:
                files = {'arquivo_pdf': f}
                
                # Remover header JSON para upload de arquivo
                headers = {k: v for k, v in self.headers.items() if k != 'Content-Type'}
                
                response = self.session.post(
                    f"{self.base_url}/api/laudos/{laudo_id}/upload_pdf/",
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 200:
                    print(f"✅ PDF enviado para laudo {laudo_id}")
                    return True
                else:
                    print(f"❌ Erro ao enviar PDF: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ Erro no upload do PDF: {e}")
            return False
    
    # ========== EMPRESAS ==========
    
    def insert_company(self, company: Company, address: Address) -> Optional[int]:
        """Cadastra empresa"""
        try:
            company_dict = to_dict(company)
            address_dict = to_dict(address)
            
            # Criar endereço
            endereco_data = {
                "cep": address_dict.get("cep", ""),
                "rua": address_dict.get("street", ""),
                "numero": address_dict.get("address_number", ""),
                "cidade": address_dict.get("city", ""),
                "estado": address_dict.get("state", ""),
                "pais": address_dict.get("country", "Brasil"),
            }
            
            endereco_result = self._make_request("POST", "/api/enderecos/", data=endereco_data)
            if not endereco_result:
                return None
            
            # Criar empresa
            empresa_data = {
                "nome": company_dict.get("company_name", ""),
                "cnpj": company_dict.get("cnpj", ""),
                "email": company_dict.get("email", ""),
                "telefone": company_dict.get("phone_number", ""),
                "endereco": endereco_result.get("id"),
            }
            
            result = self._make_request("POST", "/api/empresas/", data=empresa_data)
            
            if result:
                print(f"✅ Empresa {company_dict.get('company_name')} cadastrada")
                return result.get("id")
            
            return None
            
        except Exception as e:
            print(f"❌ Erro ao cadastrar empresa: {e}")
            return None
    
    # ========== MÉTODOS AUXILIARES ==========
    
    def create_database(self) -> None:
        """Não faz nada - banco é gerenciado pelo Django"""
        pass
    
    def close_connection(self):
        """Fecha sessão HTTP"""
        if hasattr(self, 'session'):
            self.session.close()
    
    def get_streets(self, city: str = None) -> List[str]:
        """Retorna lista de ruas (método estático - não faz requisição HTTP)"""
        # Retorna lista simplificada, compatível com interface
        return ["Rua Principal", "Avenida Central", "Travessa da Paz", 
                "Rua das Flores", "Avenida Brasil"]
    
    def test_connection(self) -> bool:
        """Testa se API está respondendo"""
        try:
            response = self.session.get(f"{self.base_url}/api/health/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    # ========== MÉTODOS DE BUSCA (simplificados) ==========
    
    def get_countries(self) -> List[str]:
        """Países - pode integrar com API depois"""
        return ["Brasil"]
    
    def get_states(self, country: str) -> List[str]:
        """Estados brasileiros"""
        estados = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
            "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", 
            "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ]
        return [f"{estado} - {self._get_state_name(estado)}" for estado in estados]
    
    def _get_state_name(self, sigla: str) -> str:
        """Retorna nome completo do estado"""
        estados = {
            "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas",
            "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo",
            "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul",
            "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná",
            "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
            "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina",
            "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins"
        }
        return estados.get(sigla, sigla)
    
    def get_cities(self, state: str) -> List[str]:
        """Cidades - pode integrar com API IBGE depois"""
        # Extrair sigla do estado
        sigla = state.split(" - ")[0] if " - " in state else state[:2]
        
        # Algumas cidades por estado (exemplos)
        cidades_por_estado = {
            "SC": ["Concórdia", "Marmeleiro", "Francisco Beltrão", "Chapecó", "Joinville", "Florianópolis"],
            "PR": ["Curitiba", "Londrina", "Maringá", "Cascavel", "Foz do Iguaçu"],
            "RS": ["Porto Alegre", "Caxias do Sul", "Pelotas", "Santa Maria", "Rio Grande"],
        }
        
        return cidades_por_estado.get(sigla, ["Cidade Principal"])
    
    # ========== Organizar depois ==========
    def get_companies(self, **kwargs) -> List[Dict]:
        """Busca empresas - CONVERTE formato Django para software"""
        print(f"🏢 Buscando empresas...")
        
        params = {}
        if kwargs.get('cnpj'):
            cnpj_clean = self._clean_cpf_cnpj(kwargs['cnpj'])
            params['cnpj'] = cnpj_clean
        elif kwargs.get('company_name'):
            params['search'] = kwargs['company_name']
        elif kwargs.get('id'):
            result = self._make_request("GET", f"/api/empresas/{kwargs['id']}/")
            return [self._convert_company_format(result)] if result else []
        
        result = self._make_request("GET", "/api/empresas/", params=params)
        
        if not result:
            print("⚠️  Nenhuma empresa encontrada")
            return []
        
        if not isinstance(result, list):
            result = [result]
        
        print(f"✅ {len(result)} empresa(s) encontrada(s)")
        
        return [self._convert_company_format(empresa) for empresa in result]

    def _convert_company_format(self, empresa_data: Dict) -> Dict:
        """Converte empresa do formato Django para software"""
        if not empresa_data:
            return {}
        
        # Buscar endereço
        endereco = self._get_address_from_company(empresa_data)
        
        return {
            'id': empresa_data.get('id'),
            'company_name': empresa_data.get('nome', ''),
            'cnpj': empresa_data.get('cnpj', ''),
            'email': empresa_data.get('email', ''),
            'phone_number': empresa_data.get('telefone', ''),
            
            # Endereço
            'street': endereco.get('rua', ''),
            'address_number': endereco.get('numero', ''),
            'cep': endereco.get('cep', ''),
            'city': endereco.get('cidade', ''),
            'state': endereco.get('estado', ''),
            'country': endereco.get('pais', 'Brasil'),
        }

    def _get_address_from_company(self, empresa_data: Dict) -> Dict:
        """Extrai endereço da empresa"""
        endereco = empresa_data.get('endereco')
        
        if not endereco:
            return {}
        
        if isinstance(endereco, int):
            return self._make_request("GET", f"/api/enderecos/{endereco}/") or {}
        
        if isinstance(endereco, dict):
            return endereco
        
        return {}

    # Atualize também o método get_persons para garantir formato correto:
    def get_persons(self, **kwargs) -> List[Dict]:
        """Busca pessoas - GARANTINDO FORMATO CORRETO"""
        print(f"👤 Buscando pessoas...")
        
        params = {"page_size": 1000}
        if kwargs.get('cpf'):
            cpf_clean = self._clean_cpf_cnpj(kwargs['cpf'])
            params['cpf'] = cpf_clean
        elif kwargs.get('name'):
            params['search'] = kwargs['name']
        elif kwargs.get('id'):
            result = self._make_request("GET", f"/api/pessoas/{kwargs['id']}/")
            return [self._format_person_for_software(result)] if result else []
        
        result = self._make_request("GET", "/api/pessoas/", params=params)
        
        if not result:
            print("⚠️  Nenhuma pessoa encontrada")
            return []
        
        if not isinstance(result, list):
            result = [result]
        
        print(f"✅ {len(result)} pessoa(s) encontrada(s)")
        
        # Formatar cada pessoa
        pessoas_formatadas = []
        for pessoa in result:
            try:
                pessoa_fmt = self._format_person_for_software(pessoa)
                if pessoa_fmt:  # Só adicionar se não estiver vazio
                    pessoas_formatadas.append(pessoa_fmt)
            except Exception as e:
                print(f"⚠️  Erro ao formatar pessoa: {e}")
                # Adicionar mesmo com erro, mas com campos mínimos
                pessoas_formatadas.append({
                    'id': pessoa.get('id'),
                    'name': pessoa.get('name', 'N/A'),
                    'cpf': pessoa.get('cpf', 'N/A'),
                    'email': pessoa.get('email', ''),
                    'phone_number': pessoa.get('phone_number', ''),
                    'birth_date': pessoa.get('nascimento', ''),
                    'street': '', 'address_number': '', 'cep': '', 
                    'city': '', 'state': '', 'country': 'Brasil'
                })
        
        return pessoas_formatadas

    def _format_person_for_software(self, pessoa_data: Dict) -> Dict:
        """Formata pessoa para o software - VERSÃO ROBUSTA"""
        if not pessoa_data:
            return {}
        
        # Garantir que temos os campos básicos
        pessoa_formatada = {
            'id': pessoa_data.get('id'),
            'name': pessoa_data.get('name', ''),
            'cpf': pessoa_data.get('cpf', ''),
            'email': pessoa_data.get('email', ''),
            'phone_number': pessoa_data.get('phone_number', ''),
            'birth_date': pessoa_data.get('nascimento', ''),
            
            # Inicializar endereço vazio
            'street': '',
            'address_number': '',
            'cep': '',
            'city': '',
            'state': '',
            'country': 'Brasil',
        }
        
        # Buscar endereço
        endereco = self._get_complete_address(pessoa_data.get('endereco'))
        if endereco:
            pessoa_formatada.update({
                'street': endereco.get('rua', ''),
                'address_number': endereco.get('numero', ''),
                'cep': endereco.get('cep', ''),
                'city': endereco.get('cidade', ''),
                'state': endereco.get('estado', ''),
                'country': endereco.get('pais', 'Brasil'),
            })
        
        return pessoa_formatada

    def _get_complete_address(self, endereco_ref) -> Dict:
        """Obtém endereço completo de forma segura"""
        if not endereco_ref:
            return {}
        
        try:
            if isinstance(endereco_ref, dict):
                return endereco_ref
            elif isinstance(endereco_ref, int):
                return self._make_request("GET", f"/api/enderecos/{endereco_ref}/") or {}
            elif isinstance(endereco_ref, str):
                # Tentar converter string para int
                try:
                    end_id = int(endereco_ref)
                    return self._make_request("GET", f"/api/enderecos/{end_id}/") or {}
                except ValueError:
                    return {}
        except Exception as e:
            print(f"⚠️  Erro ao buscar endereço: {e}")
        
        return {}
    

    def get_requesters(self, **kwargs) -> List[Dict]:
        """Método de compatibilidade para código antigo"""
        requester_id = kwargs.get('requester_id')
        
        if requester_id:
            # Tentar buscar como pessoa primeiro
            persons = self.get_persons(id=requester_id)
            if persons:
                person = persons[0]
                return [{
                    'requester_id': person['id'],
                    'name': person['name'],
                    'document_number': person['cpf'],
                    'requester_type': 'person'
                }]
            
            # Tentar buscar como empresa
            companies = self.get_companies(id=requester_id)
            if companies:
                company = companies[0]
                return [{
                    'requester_id': company['id'],
                    'name': company['company_name'],
                    'document_number': company['cnpj'],
                    'requester_type': 'company'
                }]
        
        return []
    # ============Organizar depois fim===========
    


# ========== WRAPPER PARA COMPATIBILIDADE ==========

class Database:
    """Wrapper para manter compatibilidade com código existente"""
    
    def __init__(self, use_http: bool = True):
        if use_http:
            self.db = DatabaseHTTP()
            print("🌐 Usando API HTTP Django")
        else:
            # Fallback para SQLite original
            try:
                from .DatabaseSQLite import Database as DatabaseSQLite
                self.db = DatabaseSQLite()
                print("💾 Usando SQLite local")
            except ImportError:
                raise ImportError("Não foi possível carregar SQLite ou HTTP")
    
    def __getattr__(self, name):
        """Delega métodos para o backend atual"""
        return getattr(self.db, name)
    
    