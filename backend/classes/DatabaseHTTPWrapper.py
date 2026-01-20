"""
DatabaseHTTPWrapper.py - Wrapper 100% compatível com DatabaseSQLite antigo
"""
from unittest import result
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
from backend.classes.exceptions import CNPJAlreadyExistsError, CPFAlreadyExistsError
from backend.classes.utils import to_dict

class SQLiteRow:
    """Classe que simula sqlite3.Row para manter compatibilidade"""
    def __init__(self, data: Dict):
        self._data = data
    
    def __getitem__(self, key):
        return self._data.get(key)
    
    def __contains__(self, key):
        """Suporta operador 'in' para verificar se uma chave existe"""
        return key in self._data
    
    def get(self, key, default=None):
        """Método get() compatível com dict"""
        return self._data.get(key, default)
    
    def __getattr__(self, name):
        return self._data.get(name)
    
    def keys(self):
        return self._data.keys()
    
    def __repr__(self):
        return f"SQLiteRow({self._data})"

class DatabaseHTTPWrapper:
    """Wrapper 100% compatível com o DatabaseSQLite antigo"""
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.base_url = api_url.rstrip('/')
        self.token: Optional[str] = None
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'GAIA-Software-Desktop/Compat'
        }
        self.session = requests.Session()
        
        # Credenciais do técnico
        self.TECH_CPF = "99988877700"
        self.TECH_PASSWORD = "123456"
        
        # Auto login
        self._auto_login()
    
    # ========== AUXILIARES ==========
    
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
    
    # ========== AUTENTICAÇÃO ==========
    
    def _auto_login(self) -> bool:
        """Login automático"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/login/cpf/",
                json={"cpf": self.TECH_CPF, "password": self.TECH_PASSWORD},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access")
                if self.token:
                    self.headers["Authorization"] = f"Bearer {self.token}"
                    print("✅ Login automático realizado")
                    return True
            return False
        except:
            return False
        
    def login(self, cpf: str = None, password: str = None) -> bool:
        """Login usando o mesmo endpoint do teste simples"""
        try:
            login_cpf = cpf or self.TECH_CPF
            login_password = password or self.TECH_PASSWORD

            response = self.session.post(
                f"{self.base_url}/api/login/cpf/",
                json={"cpf": login_cpf, "password": login_password},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access")
                if self.token:
                    self.headers["Authorization"] = f"Bearer {self.token}"
                    print(f"✅ Login automático realizado (CPF: {login_cpf})")
                    return True

            print(f"❌ Falha no login: {response.status_code}")
            return False

        except Exception as e:
            print(f"❌ Erro no login automático: {e}")
            return False

    def _make_request(self, method: str, endpoint: str,
                  data: Dict = None, params: Dict = None,
                  _retry=False) -> Any:
        try:
            url = f"{self.base_url}{endpoint}"

            if not self.token:
                print("⚠️ Sem token, tentando login automático...")
                if not self._auto_login():
                    raise RuntimeError("Falha no auto-login")

            headers = self.headers.copy()
            headers["Authorization"] = f"Bearer {self.token}"

            print(f"\n REQUEST:")
            print(f"  {method.upper()} {url}")
            if data:
                print(json.dumps(data, indent=2, ensure_ascii=False))

            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=data,
                params=params,
                timeout=30
            )

            print(f"\n RESPONSE:")
            print(f"  Status: {response.status_code}")
            print(f"  Text: {response.text[:300]}")

            if response.status_code == 204:
                return True

            if response.status_code in (200, 201):
                if response.content:
                    try:
                        return response.json()
                    except ValueError:
                        raise RuntimeError("Resposta não é JSON válido")
                return True

            if response.status_code == 401 and not _retry:
                print("🔑 Token expirado, renovando...")
                if self._auto_login():
                    return self._make_request(
                        method, endpoint, data, params, _retry=True
                    )
                raise RuntimeError("Falha ao renovar token")

            raise RuntimeError(
                f"Erro HTTP {response.status_code}: {response.text[:200]}"
            )

        except Exception as e:
            print(f" ERRO em _make_request: {e}")
            raise   

    
    # ========== TESTE DE CONEXÃO ==========
    def test_connection(self) -> bool:
        """Testa se a API está respondendo"""
        try:
            response = self.session.get(f"{self.base_url}/api/health/", timeout=5)
            return response.status_code == 200
        except:
            return False
        
    # ========== MÉTODOS COMPATÍVEIS COM SQLite ANTIGO ==========
    
    def insert_person(self, person: Person, address: Address) -> dict:
        """MESMA ASSINATURA DO SQLITE ANTIGO - VERSÃO DEBUG"""
        try:
            address_dict = to_dict(address)
            
            name = person.name 
            cpf = person.cpf 
            email = person.email
            birth_date = person.birth_date

            if hasattr(person, 'get_phone_number'):
                phone = person.get_phone_number()
            
            # 1. Criar endereço
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
                print(f"❌ FALHA: Não foi possível criar endereço")
                endereco_id = None
            else:
                endereco_id = endereco_result.get("id")
                print(f"✅ Endereço criado com ID: {endereco_id}")
            
            # 2. Criar pessoa
            pessoa_data = {
                "name": name,
                "cpf": cpf,
                "email": email,
                "phone_number": phone,
                "nascimento": self._format_date(birth_date),
            }
            
            if endereco_id:
                pessoa_data["endereco"] = endereco_id
            
            pessoa_result = self._make_request("POST", "/api/pessoas/", data=pessoa_data)
            
            if pessoa_result and 'id' in pessoa_result:
                print(f"✅ Pessoa '{name}' inserida com sucesso (ID: {pessoa_result['id']})")
                return pessoa_result
            else:
                print(f"❌ FALHA AO CRIAR PESSOA")
                raise Exception("Falha ao criar pessoa - Verifique logs acima")
                    
        except Exception as e:
            print(f"❌ ERRO GERAL: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def edit_person(self, person: Person, address: Address, id: int, requester_id: int) -> None:
        """MESMA ASSINATURA DO SQLITE ANTIGO"""
        try:
            person_dict = to_dict(person)
            address_dict = to_dict(address)

            # Recupera dados atuais para manter campos obrigatórios
            current = self._make_request("GET", f"/api/pessoas/{id}/") or {}
            endereco_id = current.get("endereco")

            # Atualiza ou cria endereço
            endereco_payload = {
                "cep": address_dict.get("cep", ""),
                "rua": address_dict.get("street", ""),
                "numero": address_dict.get("address_number", ""),
                "cidade": address_dict.get("city", ""),
                "estado": address_dict.get("state", ""),
                "pais": address_dict.get("country", "Brasil"),
            }

            if endereco_id:
                self._make_request("PUT", f"/api/enderecos/{endereco_id}/", data=endereco_payload)
            else:
                endereco_result = self._make_request("POST", "/api/enderecos/", data=endereco_payload)
                endereco_id = endereco_result.get("id") if endereco_result else None

            phone = person_dict.get("phone_number") or person_dict.get("phone") or person_dict.get("telefone")

            pessoa_payload = {
                "name": person_dict.get("name", current.get("name", "")),
                "cpf": person_dict.get("cpf", current.get("cpf", "")),
                "email": person_dict.get("email", current.get("email", "")),
                "phone_number": phone or current.get("phone_number", ""),
                "nascimento": self._format_date(person_dict.get("birth_date") or current.get("nascimento")),
            }

            if endereco_id:
                pessoa_payload["endereco"] = endereco_id

            self._make_request("PUT", f"/api/pessoas/{id}/", data=pessoa_payload)
            print(f"✅ Pessoa {id} atualizada")

        except Exception as e:
            print(f"❌ Erro ao editar pessoa: {e}")
            raise
    
    def delete_person(self, id: int) -> None:
        """MESMA ASSINATURA DO SQLITE ANTIGO"""
        try:
            result = self._make_request("DELETE", f"/api/pessoas/{id}/")
            if result:
                print(f"✅ Pessoa {id} excluída")
            else:
                raise Exception("Falha ao excluir pessoa")
        except Exception as e:
            print(f"❌ Erro ao excluir pessoa: {e}")
            raise
    
    def insert_company(self, company: Company, address: Address) -> dict:
        """MESMA ASSINATURA DO SQLITE ANTIGO"""
        try:
            company_dict = to_dict(company)
            address_dict = to_dict(address)
            
            # 1. Criar endereço
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
                raise Exception("Falha ao criar endereço")
            
            endereco_id = endereco_result.get("id")
            
            # 2. Criar empresa
            empresa_data = {
                "name": company_dict.get("company_name", ""),
                "cnpj": company_dict.get("cnpj", ""),
                "email": company_dict.get("email", ""),
                "telefone": company_dict.get("phone_number", ""),
                "endereco": endereco_id,
            }
            
            empresa_result = self._make_request("POST", "/api/empresas/", data=empresa_data)
            
            if empresa_result and 'id' in empresa_result:
                print(f"✅ Empresa {company_dict.get('company_name')} cadastrada")
                return empresa_result
            else:
                raise Exception("Falha ao criar empresa")
                
        except Exception as e:
            print(f"❌ Erro ao cadastrar empresa: {e}")
            raise
    
    def edit_company(self, company: Company, address: Address, id: int, requester_id: int) -> None:
        """MESMA ASSINATURA DO SQLITE ANTIGO"""
        try:
            company_dict = to_dict(company)
            address_dict = to_dict(address)

            current = self._make_request("GET", f"/api/empresas/{id}/") or {}
            endereco_id = current.get("endereco")

            endereco_payload = {
                "cep": address_dict.get("cep", ""),
                "rua": address_dict.get("street", ""),
                "numero": address_dict.get("address_number", ""),
                "cidade": address_dict.get("city", ""),
                "estado": address_dict.get("state", ""),
                "pais": address_dict.get("country", "Brasil"),
            }

            if endereco_id:
                self._make_request("PUT", f"/api/enderecos/{endereco_id}/", data=endereco_payload)
            else:
                endereco_result = self._make_request("POST", "/api/enderecos/", data=endereco_payload)
                endereco_id = endereco_result.get("id") if endereco_result else None

            empresa_payload = {
                "name": company_dict.get("company_name", current.get("name", "")),
                "cnpj": company_dict.get("cnpj", current.get("cnpj", "")),
                "email": company_dict.get("email", current.get("email", "")),
                "telefone": company_dict.get("phone_number", current.get("telefone", "")),
            }

            if endereco_id:
                empresa_payload["endereco"] = endereco_id

            self._make_request("PUT", f"/api/empresas/{id}/", data=empresa_payload)
            print(f"✅ Empresa {id} atualizada")

        except Exception as e:
            print(f"❌ Erro ao editar empresa: {e}")
            raise
    
    def delete_company(self, id: int) -> None:
        """MESMA ASSINATURA DO SQLITE ANTIGO"""
        try:
            result = self._make_request("DELETE", f"/api/empresas/{id}/")
            if result:
                print(f"✅ Empresa {id} excluída")
            else:
                raise Exception("Falha ao excluir empresa")
        except Exception as e:
            print(f"❌ Erro ao excluir empresa: {e}")
            raise
    
    def insert_property(self, property: Property, requester_id: int, address: Address) -> dict:
        property_dict = to_dict(property)
        address_dict = to_dict(address)

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
            raise Exception("Falha ao criar endereço")
        endereco_id = endereco_result.get("id")

        data = {
            "name": property_dict["name"],
            "endereco": endereco_id,  
            "registration_number": property_dict["registration_number"],
            "localizacao": property_dict.get("localizacao", ""),
            "proprietario_id": requester_id,
        }
        print(f"DEBUG DatabaseHTTPWrapper.insert_property - enviando: {data}")

        result = self._make_request("POST", "/api/propriedades/", data=data)

        if not result or "id" not in result:
            raise Exception("Falha ao criar propriedade")

        print(f"✅ Propriedade '{property_dict['name']}' cadastrada")
        print(f"   ID: {result['id']}")
        return result
        
    def edit_property(self, property: Property, property_id: int, address: Address = None) -> None:
        """MESMA ASSINATURA DO SQLITE ANTIGO"""
        try:
            property_dict = to_dict(property)

            current = self._make_request("GET", f"/api/propriedades/{property_id}/") or {}

            endereco_id = None
            endereco = current.get("endereco") or current.get("endereco_id")
            endereco_id = endereco if isinstance(endereco, int) else None

            # Usar endereço passado como parâmetro, se disponível
            address_dict = to_dict(address) if address else {}
            
            # Atualizar endereço só se recebermos novos dados; evita PUT com campos em branco
            has_new_address = address and any(
                address_dict.get(field)
                for field in ("cep", "street", "address_number", "city", "state", "country")
            )

            if endereco_id and has_new_address:
                endereco_atual = self._get_complete_address(endereco_id) or {}
                endereco_payload = {
                    "cep": address_dict.get("cep") or endereco_atual.get("cep", ""),
                    "rua": address_dict.get("street") or endereco_atual.get("rua", ""),
                    "numero": address_dict.get("address_number") or endereco_atual.get("numero", ""),
                    "cidade": address_dict.get("city") or endereco_atual.get("cidade", ""),
                    "estado": address_dict.get("state") or endereco_atual.get("estado", ""),
                    "pais": address_dict.get("country") or endereco_atual.get("pais", "Brasil"),
                }
                self._make_request("PUT", f"/api/enderecos/{endereco_id}/", data=endereco_payload)

            # A API exige sempre 'proprietario_id' no PUT. Buscar do payload
            # ou derivar do recurso atual (proprietario_pessoa/empresa)
            proprietario_id = (
                property_dict.get("proprietario_id")
                or current.get("proprietario_pessoa")
                or current.get("proprietario_empresa")
            )

            # Alguns backends podem retornar um objeto em vez do ID (pouco provável
            # com ModelSerializer padrão). Garantir que se for dict pegue o ID.
            if isinstance(proprietario_id, dict):
                proprietario_id = proprietario_id.get("id")

            if not proprietario_id:
                raise Exception(
                    "Proprietário da propriedade não identificado para atualização"
                )

            data = {
                "name": property_dict.get("name", current.get("name", "")),
                "registration_number": property_dict.get("registration_number", current.get("registration_number", "")),
                "localizacao": property_dict.get("localizacao", current.get("localizacao", "")),
            }

            # Enviar sempre o proprietario_id para atender o serializer
            data["proprietario_id"] = proprietario_id
            if endereco_id:
                data["endereco"] = endereco_id

            result = self._make_request("PUT", f"/api/propriedades/{property_id}/", data=data)

            if result:
                print(f"✅ Propriedade {property_id} atualizada")
            else:
                raise Exception("Falha ao atualizar propriedade")

        except Exception as e:
            print(f"❌ Erro ao editar propriedade: {e}")
            raise
    
    def delete_property(self, id: int) -> None:
        """MESMA ASSINATURA DO SQLITE ANTIGO"""
        try:
            result = self._make_request("DELETE", f"/api/propriedades/{id}/")
            if result:
                print(f"✅ Propriedade {id} excluída")
            else:
                raise Exception("Falha ao excluir propriedade")
        except Exception as e:
            print(f"❌ Erro ao excluir propriedade: {e}")
            raise
    
    def insert_sample(self, sample: Sample, property_id: int, sample_number: int) -> dict:
        """MESMA ASSINATURA DO SQLITE ANTIGO"""
        try:
            sample_dict = to_dict(sample)

            # DEBUG: Verificar ID da propriedade
            print(f"🔍 Validando propriedade ID: {property_id}")
            
            # Primeiro, tentar verificar se a propriedade existe e pertence ao usuário
            try:
                # Verificar propriedade via API
                propriedade_info = self._make_request("GET", f"/api/propriedades/{property_id}/")
                if not propriedade_info:
                    raise Exception(f"Propriedade ID {property_id} não encontrada")
                print(f"✅ Propriedade encontrada: {propriedade_info.get('name', 'N/A')}")
            except Exception as e:
                print(f"❌ Erro ao buscar propriedade {property_id}: {e}")
                raise         
                
            data = {
                # Endpoint criar_simples espera "propriedade_id"; manter só este nome para evitar 400
                "propriedade_id": property_id,
                "numero_amostra": sample_number,
                "data_coleta": self._format_date(sample_dict.get("collection_date")),
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
            
            result = self._make_request("POST", "/api/amostras/criar_simples/", data=data)
            
            if result and 'id' in result:
                print(f"✅ Amostra {sample_number} cadastrada (ID: {result['id']})")
                return result
            elif isinstance(result, dict):
                # Pode ter retornado dados mas sem 'id' diretamente - verificar
                print(f"⚠️ Resposta da API: {result}")
                raise Exception("Resposta da API sem ID da amostra")
            else:
                raise Exception("Falha ao criar amostra")
                
        except Exception as e:
            print(f"❌ Erro ao cadastrar amostra: {e}")
            raise
    
    def edit_sample(self, sample: Sample, sample_id: int) -> None:
        """MESMA ASSINATURA DO SQLITE ANTIGO"""
        try:
            sample_dict = to_dict(sample) or {}

            current = self._make_request("GET", f"/api/amostras/{sample_id}/") or {}
            propriedade_id = current.get("propriedade") or sample_dict.get("fk_property_id")
            numero_amostra = current.get("numero_amostra") or sample_dict.get("sample_number")

            # Construir payload com fallbacks seguros para todos os campos
            data = {
                "propriedade_id": propriedade_id,
                "numero_amostra": numero_amostra,
                "descricao": sample_dict.get("description") or current.get("descricao", ""),
                "data_coleta": self._format_date(sample_dict.get("collection_date") or current.get("data_coleta")),
                "ph": sample_dict.get("ph") or current.get("ph"),
                "fosforo": sample_dict.get("phosphorus") or current.get("fosforo"),
                "potassio": sample_dict.get("potassium") or current.get("potassio"),
                "materia_organica": sample_dict.get("organic_matter") or current.get("materia_organica"),
                "argila": sample_dict.get("clay") or current.get("argila"),
                "silte": sample_dict.get("silte") or current.get("silte"),
                "areia": sample_dict.get("sand") or current.get("areia"),
                "classificacao": sample_dict.get("classification") or current.get("classificacao"),
            }

            result = self._make_request("PUT", f"/api/amostras/{sample_id}/", data=data)

            if result:
                print(f"✅ Amostra {sample_id} atualizada")
            else:
                raise Exception("Falha ao atualizar amostra")

        except Exception as e:
            print(f"❌ Erro ao editar amostra: {e}")
            raise
    
    def delete_sample(self, id: int) -> None:
        """MESMA ASSINATURA DO SQLITE ANTIGO"""
        try:
            result = self._make_request("DELETE", f"/api/amostras/{id}/")
            if result:
                print(f"✅ Amostra {id} excluída")
            else:
                raise Exception("Falha ao excluir amostra")
        except Exception as e:
            print(f"❌ Erro ao excluir amostra: {e}")
            raise

    def insert_report(self, report: Report, sample_id: int) -> Optional[int]:
        """Insere laudo (PDF)"""
        report_dict = to_dict(report)
        
        data = {
            "numero_amostra": sample_id,
            "data_coleta": datetime.now().strftime("%Y-%m-%d"),
            "propriedade": self._get_property_from_sample(sample_id),
            "ativo": True
        }
        
        result = self._make_request("POST", "/api/laudos/", data=data)
        
        if result and 'id' in result:
            # Fazer upload do arquivo PDF se houver
            file_location = report_dict.get("file_location")
            if file_location:
                self._upload_report_pdf(result['id'], file_location)
            
            print(f"✅ Laudo criado com ID: {result['id']}")
            return result['id']
        
        return None
    
    # ========== MÉTODOS DE CONSULTA (RETORNAM SQLiteRow) ==========
    
    def get_persons(self, **kwargs) -> list:
        """RETORNA LISTA DE SQLiteRow COMPATÍVEL"""
        try:
            params = {}

            # Busca por ID (detalhe)
            if kwargs.get('id'):
                response = self._make_request("GET", f"/api/pessoas/{kwargs['id']}/")
            else:
                # Filtros de lista
                cpf_in = kwargs.get('cpf')
                name = kwargs.get('name')

                if cpf_in:
                    cpf_digits = ''.join(ch for ch in str(cpf_in) if ch.isdigit())
                    # CPF completo usa filtro exato, parcial usa busca textual
                    if len(cpf_digits) == 11:
                        params['cpf'] = cpf_digits
                    else:
                        params['search'] = cpf_digits
                elif name:
                    params['search'] = name

                response = self._make_request("GET", "/api/pessoas/", params=params)

            pessoas = self._unwrap_results(response)

            formatted = []

            for pessoa in pessoas:
                endereco = self._get_complete_address(pessoa.get('endereco'))

                # Normaliza 'nascimento' para formato dd/mm/YYYY esperado pela interface
                nascimento = pessoa.get('nascimento')
                try:
                    nascimento_br = datetime.strptime(nascimento, "%Y-%m-%d").strftime("%d/%m/%Y") if nascimento else ''
                except Exception:
                    nascimento_br = nascimento or ''

                row_data = {
                    'id': pessoa.get('id'),
                    'name': pessoa.get('name', ''),
                    'birth_date': nascimento_br,
                    'cpf': pessoa.get('cpf', ''),
                    'email': pessoa.get('email', ''),
                    'phone_number': pessoa.get('phone_number', ''),
                    'requester_id': pessoa.get('id'),
                    'cep': endereco.get('cep', ''),
                    'address_number': endereco.get('numero', ''),
                    'address_id': endereco.get('id'),
                    'street': endereco.get('rua', ''),
                    'city': endereco.get('cidade', ''),
                    'state': endereco.get('estado', ''),
                    'country': endereco.get('pais', 'Brasil'),
                }

                formatted.append(SQLiteRow(row_data))

            return formatted

        except Exception as e:
            print(f"❌ Erro ao buscar pessoas: {e}")
            import traceback
            traceback.print_exc()
            return []

    
    def get_companies(self, **kwargs) -> list:
        """RETORNA LISTA DE SQLiteRow COMPATÍVEL"""
        try:
            params = {}

            if kwargs.get('id'):
                response = self._make_request("GET", f"/api/empresas/{kwargs['id']}/")
            else:
                cnpj_in = kwargs.get('cnpj')
                company_name = kwargs.get('company_name')

                if cnpj_in:
                    cnpj_digits = ''.join(ch for ch in str(cnpj_in) if ch.isdigit())
                    # CNPJ completo usa filtro exato, parcial usa busca textual
                    if len(cnpj_digits) == 14:
                        params['cnpj'] = cnpj_digits
                    else:
                        params['search'] = cnpj_digits
                elif company_name:
                    params['search'] = company_name

                response = self._make_request("GET", "/api/empresas/", params=params)

            empresas = self._unwrap_results(response)

            # Fallback: se filtrou por CNPJ exato e não retornou nada, tenta busca textual
            if kwargs.get('cnpj') and not empresas:
                alt_params = {'search': ''.join(ch for ch in str(kwargs.get('cnpj')) if ch.isdigit())}
                response = self._make_request("GET", "/api/empresas/", params=alt_params)
                empresas = self._unwrap_results(response)

            formatted = []

            for empresa in empresas:
                if not empresa:
                    continue

                endereco = self._get_complete_address(empresa.get('endereco'))

                row_data = {
                    'id': empresa.get('id'),
                    'name': empresa.get('name', ''),
                    'company_name': empresa.get('name', ''),  # Compatibilidade com interface antiga
                    'cnpj': empresa.get('cnpj', ''),
                    'phone_number': empresa.get('telefone', ''),
                    'email': empresa.get('email', ''),
                    'requester_id': empresa.get('id'),
                    'cep': endereco.get('cep', ''),
                    'address_number': endereco.get('numero', ''),
                    'address_id': endereco.get('id'),
                    'street': endereco.get('rua', ''),
                    'city': endereco.get('cidade', ''),
                    'state': endereco.get('estado', ''),
                    'country': endereco.get('pais', 'Brasil'),
                }

                formatted.append(SQLiteRow(row_data))

            return formatted

        except Exception as e:
            print(f"❌ Erro ao buscar empresas: {e}")
            return []

    
    def get_requesters(self, **kwargs) -> list:
        """RETORNA LISTA DE SQLiteRow COMPATÍVEL"""
        try:
            requesters = []

            persons = self.get_persons()
            for person in persons:
                requesters.append(SQLiteRow({
                    'requester_id': person['id'],
                    'phone_number': person['phone_number'],
                    'email': person['email'],
                    'name': person['name'],
                    'id': person['id'],
                    'document_number': person['cpf'],
                    'requester_type': 'person'
                }))

            companies = self.get_companies()
            for company in companies:
                requesters.append(SQLiteRow({
                    'requester_id': company['id'],
                    'phone_number': company['phone_number'],
                    'email': company['email'],
                    'name': company['name'],
                    'id': company['id'],
                    'document_number': company['cnpj'],
                    'requester_type': 'company'
                }))

            requester_id = kwargs.get('requester_id')
            if requester_id:
                requesters = [r for r in requesters if r['requester_id'] == requester_id]

            return requesters

        except Exception as e:
            print(f"❌ Erro ao buscar solicitantes: {e}")
            return []

    
    def get_properties(self, **kwargs) -> list:
        """RETORNA LISTA DE SQLiteRow COMPATÍVEL"""
        try:
            if kwargs.get('id'):
                result = self._make_request("GET", f"/api/propriedades/{kwargs['id']}/")
                propriedades = [result] if result else []
            else:
                result = self._make_request("GET", "/api/propriedades/")
                propriedades = self._unwrap_results(result)

            formatted = []
            for prop in propriedades:
                endereco = prop.get("endereco_detalhes") or {}

                # Filtrar por proprietário quando requester_id é informado
                requester_filter = kwargs.get('requester_id')
                proprietario = prop.get('proprietario_pessoa') or prop.get('proprietario_empresa')
                if requester_filter and requester_filter != proprietario:
                    continue

                location_value = (
                    prop.get('localizacao')
                    or f"{endereco.get('rua', '')}, {endereco.get('numero', '')}"
                ).strip(', ')

                row_data = {
                    'id': prop.get('id'),
                    'name': prop.get('name', ''),
                    'registration_number': prop.get('registration_number', ''),
                    # Preferir o campo "localizacao" da API; se vier vazio, cair para rua/numero
                    'localizacao': location_value,
                    # Alias usado pela UI (PropertyWindow)
                    'location': location_value,
                    'city': endereco.get('cidade', ''),
                    'state': endereco.get('estado', ''),
                    'country': endereco.get('pais', 'Brasil'),
                }

                formatted.append(SQLiteRow(row_data))

            return formatted

        except Exception as e:
            print(f"❌ Erro ao buscar propriedades: {e}")
            return []
        
    def _get_property_from_sample(self, sample_id: int) -> Optional[int]:
        """Obtém ID da propriedade a partir da amostra"""
        sample = self._make_request("GET", f"/api/amostras/{sample_id}/")
        return sample.get('propriedade') if sample else None
    
    def get_samples(self, **kwargs) -> list:
        """RETORNA LISTA DE SQLiteRow COMPATÍVEL"""
        try:
            params = {}
            if kwargs.get('sample_id'):
                result = self._make_request("GET", f"/api/amostras/{kwargs['sample_id']}/")
                result_list = [result] if result else []
            elif kwargs.get('property_id'):
                params['propriedade'] = kwargs['property_id']
                response = self._make_request("GET", "/api/amostras/", params=params)
                result_list = self._unwrap_results(response)
            elif kwargs.get('id_list'):
                result_list = []
                for sample_id in kwargs['id_list']:
                    result = self._make_request("GET", f"/api/amostras/{sample_id}/")
                    if result:
                        result_list.append(result)
            else:
                response = self._make_request("GET", "/api/amostras/")
                result_list = self._unwrap_results(response)
            
            # Garantir que result_list é uma lista
            if not isinstance(result_list, list):
                result_list = [result_list] if result_list else []
            
            formatted = []
            for amostra in result_list:
                if not amostra:
                    continue
                
                row_data = {
                    'id': amostra.get('id'),
                        'description': amostra.get('descricao', ''),
                        'sample_number': amostra.get('numero_amostra'),
                        'collection_date': amostra.get('data_coleta'),
                        'total_area': amostra.get('area_total'),
                        'latitude': amostra.get('latitude'),
                        'longitude': amostra.get('longitude'),
                        'depth': amostra.get('profundidade'),
                        'phosphorus': amostra.get('fosforo'),
                        'potassium': amostra.get('potassio'),
                        'organic_matter': amostra.get('materia_organica'),
                        'ph': amostra.get('ph'),
                        'aluminum': amostra.get('aluminio'),
                        'h_al': amostra.get('h_al'),
                        'calcium': amostra.get('calcio'),
                        'magnesium': amostra.get('magnesio'),
                        'copper': amostra.get('cobre'),
                        'iron': amostra.get('ferro'),
                        'manganese': amostra.get('manganes'),
                        'zinc': amostra.get('zinco'),
                        'base_sum': amostra.get('soma_bases'),
                        'clay': amostra.get('argila'),
                        'silte': amostra.get('silte'),
                        'sand': amostra.get('areia'),
                        'classification': amostra.get('classificacao'),
                        'ctc': amostra.get('ctc'),
                        'v_percent': amostra.get('v_percent'),
                        'aluminum_saturation': amostra.get('al_saturation'),
                        'effective_ctc': amostra.get('ctc_efetiva'),
                        'used_config': amostra.get('config_usada'),
                        'smp': amostra.get('smp'),
                        'fk_property_id': amostra.get('propriedade'),
                    }
                formatted.append(SQLiteRow(row_data))
            
            return formatted
            
        except Exception as e:
            print(f"❌ Erro ao buscar amostras: {e}")
            return []
    
    def get_sample_info(self, sample_id: int) -> SQLiteRow:
        """RETORNA SQLiteRow COMPATÍVEL"""
        try:
            
            amostra = self._make_request("GET", f"/api/amostras/{sample_id}/")
            if not amostra:
                return SQLiteRow({})
            
            propriedade_id = amostra.get('propriedade')
            propriedade = None
            
            if propriedade_id:
                try:
                    propriedade = self._make_request("GET", f"/api/propriedades/{propriedade_id}/")
                except Exception as e:
                    print(f" DEBUG: Erro ao buscar propriedade {propriedade_id}: {e}")
            
            row_data = {
                'sample_description': amostra.get('descricao', ''),
                'sample_number': amostra.get('numero_amostra'),
                'collection_date': amostra.get('data_coleta'),
                'depth': amostra.get('profundidade'),
                'total_area': amostra.get('area_total'),
                'property_name': propriedade.get('name', '') if propriedade else '',
                'registration_number': propriedade.get('registration_number', '') if propriedade else '',
            }
            
            return SQLiteRow(row_data)
            
        except Exception as e:
            print(f"❌ Erro ao buscar informações da amostra: {e}")
            import traceback
            traceback.print_exc()
            return SQLiteRow({})
    
    def get_report_info(self) -> list:
        """RETORNA LISTA DE SQLiteRow COMPATÍVEL"""
        try:
            result_list = self._make_request("GET", "/api/laudos/") or []
            
            formatted = []
            for laudo in result_list if isinstance(result_list, list) else [result_list]:
                if laudo:
                    row_data = {
                        'id': laudo.get('id'),
                        'requester_name': 'A definir',
                        'date': laudo.get('data_coleta'),
                        'property': 'A definir',
                    }
                    formatted.append(SQLiteRow(row_data))
            
            return formatted
            
        except Exception as e:
            print(f"❌ Erro ao buscar laudos: {e}")
            return []
    
    def get_next_report_id(self) -> int:
        """Método compatível - retorna número incremental"""
        try:
            laudos = self._make_request("GET", "/api/laudos/") or []
            if isinstance(laudos, list):
                return len(laudos) + 1
            return 1
        except:
            return 1
    
    # ========== MÉTODOS AUXILIARES ==========
    
    def _get_complete_address(self, endereco_ref) -> Dict:
        """Obtém endereço completo"""
        if not endereco_ref:
            return {}
        
        try:
            if isinstance(endereco_ref, dict):
                return endereco_ref
            elif isinstance(endereco_ref, int):
                return self._make_request("GET", f"/api/enderecos/{endereco_ref}/") or {}
        except:
            return {}
        
    def _upload_report_pdf(self, laudo_id: int, file_path: str) -> bool:
        """Faz upload do arquivo PDF para o laudo"""
        try:
            with open(file_path, 'rb') as f:
                files = {'arquivo_pdf': f}
                
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
                    print(f"❌ Falha ao enviar PDF: {response.status_code}")
                    return False
        except Exception as e:
            print(f"❌ Erro ao fazer upload do PDF: {e}")
            return False
        
    def _unwrap_results(self, response):
        """Extrai lista de resultados do DRF"""
        if isinstance(response, dict) and "results" in response:
            return response["results"]
        if isinstance(response, list):
            return response
        if response:
            return [response]
        return []
    
    # ========== MÉTODOS SIMPLIFICADOS ==========
    
    def create_database(self) -> None:
        """Não faz nada - banco é gerenciado pelo Django"""
        pass
    
    def close_connection(self):
        """Fecha sessão HTTP"""
        self.session.close()
    
    def get_countries(self) -> list[str]:
        return ["Brasil"]
    
    def get_states(self, country: str) -> list[str]:
        return ["Santa Catarina", "Paraná", "Rio Grande do Sul", "São Paulo"]
    
    def get_cities(self, state: str) -> list[str]:
        return ["Concórdia", "Marmeleiro", "Francisco Beltrão", "Chapecó", "Joinville"]
    
    def get_streets(self, city: str) -> list[str]:
        return ["Rua Principal", "Avenida Central", "Travessa da Paz", "Rua das Flores"]

# ========== FÁBRICA PARA COMPATIBILIDADE ==========

class Database:
    """Classe final 100% compatível com o código antigo"""
    
    def __init__(self, use_http: bool = True):
        if use_http:
            self.db = DatabaseHTTPWrapper()
            print("🌐 Usando API HTTP Django (modo compatível)")
        else:
            try:
                from .DatabaseSQLite import Database as DatabaseSQLite
                self.db = DatabaseSQLite()
                print("💾 Usando SQLite local")
            except ImportError:
                raise ImportError("Não foi possível carregar SQLite")
    
    def __getattr__(self, name):
        """Delega todos os métodos para o backend"""
        return getattr(self.db, name)


# Teste rápido
if __name__ == "__main__":
    print("=== Teste de compatibilidade ===")
    db = Database(use_http=True)
    
    persons = db.get_persons()
    print(f"📊 {len(persons)} pessoa(s) encontrada(s)")
    
    if persons:
        first_person = persons[0]
        print(f"📋 Formato: {type(first_person)}")
        print(f"👤 Nome: {first_person['name']}")