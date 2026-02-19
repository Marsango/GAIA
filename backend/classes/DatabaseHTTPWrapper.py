"""
DatabaseHTTPWrapper.py - Wrapper 100% compatível com DatabaseSQLite antigo
"""
from unittest import result
import requests
import json
import os
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
        
        # Credenciais do tecnico (arquivo local, nao versionado)
        self.TECH_CPF, self.TECH_PASSWORD = self._load_credentials()
        
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
                "%y/%m/%d",  # compatível com Sample.verify_valid_date (yy/mm/dd)
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
    
    def _normalize_cpf(self, cpf: str) -> str:
        """Remove formatação do CPF, deixando apenas 11 dígitos"""
        if not cpf:
            return ""
        return ''.join(filter(str.isdigit, str(cpf)))
    
    def _normalize_cnpj(self, cnpj: str) -> str:
        """Remove formatação do CNPJ, deixando apenas 14 dígitos"""
        if not cnpj:
            return ""
        return ''.join(filter(str.isdigit, str(cnpj)))

    def _load_credentials(self) -> tuple[str, str]:
        """Carrega credenciais do arquivo de configuracao local."""
        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'auth_config.json'
        )

        if not os.path.exists(config_path):
            raise RuntimeError(
                "Arquivo auth_config.json nao encontrado. "
                "Copie auth_config.json.example para auth_config.json e configure suas credenciais."
            )

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('admin_cpf', ''), config.get('admin_password', '')
    
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
                    return True
            elif response.status_code == 429:
                # Rate limited - aguardar e tentar novamente
                print("⚠️ Taxa de requisições excedida. Aguardando 60 segundos...")
                import time
                time.sleep(60)
                return self._auto_login()  # Retry após aguardar
            else:
                print(f"❌ Auto-login falhou: Status {response.status_code}")
                print(f"   Resposta: {response.text[:200]}")
                return False
        except Exception as e:
            print(f"❌ Erro no auto-login: {str(e)}")
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
                    return True

            return False

        except Exception as e:
            return False

    def _make_request(self, method: str, endpoint: str,
                  data: Dict = None, params: Dict = None,
                  _retry=False) -> Any:
        try:
            url = f"{self.base_url}{endpoint}"
            
            print(f"🌐 HTTP {method} {url}", flush=True)
            if data:
                print(f"📤 Payload: {data}", flush=True)

            if not self.token:
                if not self._auto_login():
                    raise RuntimeError(
                        f"Falha no auto-login. Verifique:\n"
                        f"1. Se o servidor está rodando em {self.base_url}\n"
                        f"2. Se auth_config.json está configurado corretamente\n"
                        f"3. Se o usuário existe no banco de dados"
                    )

            headers = self.headers.copy()
            headers["Authorization"] = f"Bearer {self.token}"

            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=data,
                params=params,
                timeout=30
            )

            print(f"📥 Status: {response.status_code}", flush=True)

            if response.status_code == 204:
                print(f"✅ Sucesso (204 No Content)", flush=True)
                return True

            if response.status_code in (200, 201, 209):
                if response.content:
                    try:
                        result = response.json()
                        print(f"✅ Sucesso - Resposta: {result}", flush=True)
                        return result
                    except ValueError:
                        print(f"⚠️ Resposta não é JSON: {response.text[:200]}", flush=True)
                        raise RuntimeError("Resposta não é JSON válido")
                return True

            if response.status_code == 401 and not _retry:
                print(f"🔐 Token expirado, renovando...", flush=True)
                if self._auto_login():
                    return self._make_request(
                        method, endpoint, data, params, _retry=True
                    )
                raise RuntimeError("Falha ao renovar token")
            
            # Tratamento especial para 404 em DELETE - é normal (já foi deletado)
            if response.status_code == 404 and method.upper() == "DELETE":
                print(f"⚠️ DELETE retornou 404 (recurso já deletado?) - considerando como sucesso", flush=True)
                return True  # Tratamos como sucesso - recurso não existe ou já foi deletado
            
            # Tratamento especial para erro 400 (Bad Request) - validação
            if response.status_code == 400:
                try:
                    error_data = response.json()
                    print(f"❌ Erro de validação (400):", flush=True)
                    print(f"   Detalhes: {error_data}", flush=True)
                    
                    # Extrai mensagens de erro por campo
                    if isinstance(error_data, dict):
                        for field, errors in error_data.items():
                            if isinstance(errors, list):
                                for error in errors:
                                    print(f"   • {field}: {error}", flush=True)
                            else:
                                print(f"   • {field}: {errors}", flush=True)
                    
                    raise RuntimeError(f"Erro de validação: {error_data}")
                except ValueError:
                    # Se não for JSON, mostra texto bruto
                    print(f"❌ Erro 400 (texto): {response.text[:500]}", flush=True)
                    raise RuntimeError(f"Erro HTTP 400: {response.text[:200]}")

            # Outros erros HTTP
            error_msg = f"Erro HTTP {response.status_code}: {response.text[:200]}"
            print(f"❌ {error_msg}", flush=True)
            raise RuntimeError(error_msg)

        except Exception as e:
            print(f"💥 Exceção em _make_request: {e}", flush=True)
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
        """MESMA ASSINATURA DO SQLITE ANTIGO - Cria Usuário + Pessoa"""
        try:
            print(f"\n📝 Inserindo nova pessoa...")
            
            name = person.name 
            cpf = person.cpf 
            email = person.email
            birth_date = person.birth_date if hasattr(person, 'birth_date') else ''
            
            if hasattr(person, 'get_phone_number'):
                phone = person.get_phone_number()
            else:
                phone = getattr(person, 'phone_number', '')
            
            # Validar dados obrigatórios
            if not name or not cpf:
                raise ValueError("Nome e CPF são obrigatórios")
            
            if not email:
                raise ValueError("Email é obrigatório")
            
            print(f"   Nome: {name}")
            print(f"   CPF: {cpf}")
            print(f"   Email: {email}")
            print(f"   Telefone: {phone}")
            print(f"   Data de Nascimento: {birth_date}")
            
            # PASSO 1: Criar usuário e enviar email via /api/register/
            usuario_data = {
                "first_name": name,
                "cpf": cpf,
                "email": email,
                "phone_number": phone,
            }
            
            print(f"\n🔄 Criando usuário em /api/register/ (com envio de email)...")
            usuario_result = self._make_request("POST", "/api/register/", data=usuario_data)
            
            print(f"   Resposta: {usuario_result}")
            
            # Verificar se foi criado com sucesso
            if not (usuario_result and isinstance(usuario_result, dict)):
                raise Exception(f"Falha ao criar usuário. Resposta: {usuario_result}")
            
            if 'error' in usuario_result:
                raise ValueError(usuario_result.get('error'))
            
            print("✅ Usuário criado com sucesso e email enviado!")
            
            # PASSO 2: Criar endereço (se fornecido)
            endereco_id = None
            if address:
                endereco_data = to_dict(address)
                if any(endereco_data.values()):
                    endereco_payload = {
                        "cep": endereco_data.get("cep", ""),
                        "rua": endereco_data.get("street", ""),
                        "numero": endereco_data.get("address_number", ""),
                        "cidade": endereco_data.get("city", ""),
                        "estado": endereco_data.get("state", ""),
                        "pais": endereco_data.get("country", "Brasil"),
                    }
                    
                    endereco_result = self._make_request("POST", "/api/enderecos/", data=endereco_payload)
                    if endereco_result and 'id' in endereco_result:
                        endereco_id = endereco_result['id']
                        print(f"✅ Endereço criado! ID: {endereco_id}")
            
            # PASSO 3: Criar registro completo em /api/pessoas/ com nascimento
            print(f"\n🔄 Criando Pessoa em /api/pessoas/...")
            
            pessoa_payload = {
                "name": name,
                "cpf": cpf,
                "email": email,
                "phone_number": phone,
                "nascimento": self._format_date(birth_date) if birth_date else None,
            }
            
            if endereco_id:
                pessoa_payload["endereco"] = endereco_id
            
            # Remover None values
            pessoa_payload = {k: v for k, v in pessoa_payload.items() if v is not None and v != ""}
            
            pessoa_result = self._make_request("POST", "/api/pessoas/", data=pessoa_payload)
            
            if pessoa_result and 'id' in pessoa_result:
                print(f"✅ Pessoa cadastrada com sucesso! ID: {pessoa_result['id']}")
                return pessoa_result
            else:
                # Se falhar, tentar buscar se já existe (pode ter CPF duplicado)
                persons = self._make_request("GET", "/api/pessoas/", params={'cpf': cpf})
                if persons and isinstance(persons, dict) and 'results' in persons:
                    if persons['results']:
                        print(f"✅ Pessoa já existe! ID: {persons['results'][0]['id']}")
                        return persons['results'][0]
                
                raise Exception(f"Falha ao criar Pessoa. Resposta: {pessoa_result}")
                    
        except Exception as e:
            print(f"❌ Erro ao inserir pessoa: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def edit_person(self, person: Person, address: Address, id: int, requester_id: int) -> bool:
        """
        Edita uma Pessoa existente no banco de dados via API Django.
        
        Args:
            person: Objeto Person com os novos dados
            address: Objeto Address com os novos dados de endereço
            id: ID da pessoa a ser editada
            requester_id: ID do usuário que está fazendo a requisição
            
        Returns:
            bool: True se a edição foi bem sucedida, False caso contrário
        """
        print(f"\n🔵 edit_person CHAMADO - ID: {id}", flush=True)
        
        try:
            # Converte objetos para dicionários
            person_dict = to_dict(person)
            address_dict = to_dict(address)
            
            print(f"📋 person_dict: {person_dict}", flush=True)
            print(f"📋 address_dict: {address_dict}", flush=True)

            # Recupera dados atuais para manter campos obrigatórios
            print(f"🔍 Buscando dados atuais de pessoa ID {id}...", flush=True)
            current = self._make_request("GET", f"/api/pessoas/{id}/") or {}
            print(f"📊 Dados atuais: {current}", flush=True)
            endereco_id = current.get("endereco")
            
            # Salva CPF antigo ANTES de normalizar o novo (para sync)
            cpf_antigo = current.get("cpf", "")
            print(f"🔖 CPF antigo no banco: '{cpf_antigo}'", flush=True)

            # Atualiza ou cria endereço
            endereco_payload = {
                "cep": address_dict.get("cep", ""),
                "rua": address_dict.get("street", ""),
                "numero": address_dict.get("address_number", ""),
                "cidade": address_dict.get("city", ""),
                "estado": address_dict.get("state", ""),
                "pais": address_dict.get("country", "Brasil"),
            }
            
            print(f"📍 Payload de endereço: {endereco_payload}", flush=True)

            if endereco_id:
                print(f"✏️ Atualizando endereço ID {endereco_id}...", flush=True)
                self._make_request("PATCH", f"/api/enderecos/{endereco_id}/", data=endereco_payload)
            else:
                print(f"➕ Criando novo endereço...", flush=True)
                endereco_result = self._make_request("POST", "/api/enderecos/", data=endereco_payload)
                endereco_id = endereco_result.get("id") if endereco_result else None
                print(f"✅ Novo endereço criado - ID: {endereco_id}", flush=True)

            # Prepara telefone
            phone = person_dict.get("phone_number") or person_dict.get("phone") or person_dict.get("telefone")

            # Normaliza CPF (remove formatação)
            cpf_raw = person_dict.get("cpf", current.get("cpf", ""))
            cpf_normalized = self._normalize_cpf(cpf_raw)
            print(f"🆔 CPF - Original: '{cpf_raw}' → Normalizado: '{cpf_normalized}'", flush=True)
            
            # Formata data de nascimento
            birth_date_raw = person_dict.get("birth_date") or current.get("nascimento")
            birth_date_formatted = self._format_date(birth_date_raw)
            print(f"📅 Data - Original: '{birth_date_raw}' → Formatada: '{birth_date_formatted}'", flush=True)

            # Monta payload da pessoa
            pessoa_payload = {
                "name": person_dict.get("name", current.get("name", "")),
                "cpf": cpf_normalized,
                "email": person_dict.get("email", current.get("email", "")),
                "phone_number": phone or current.get("phone_number", ""),
                "nascimento": birth_date_formatted,
            }

            if endereco_id:
                pessoa_payload["endereco"] = endereco_id

            print(f"👤 Payload final da pessoa: {pessoa_payload}", flush=True)
            print(f"� Comparação ANTES vs DEPOIS:", flush=True)
            print(f"   name: '{current.get('name')}' → '{pessoa_payload['name']}'", flush=True)
            print(f"   cpf: '{current.get('cpf')}' → '{pessoa_payload['cpf']}'", flush=True)
            print(f"   email: '{current.get('email')}' → '{pessoa_payload['email']}'", flush=True)
            print(f"   phone_number: '{current.get('phone_number')}' → '{pessoa_payload['phone_number']}'", flush=True)
            print(f"   nascimento: '{current.get('nascimento')}' → '{pessoa_payload['nascimento']}'", flush=True)
            
            print(f"🔄 Enviando PATCH para /api/pessoas/{id}/", flush=True)
            
            # Usa PATCH ao invés de PUT para atualização parcial
            result = self._make_request("PATCH", f"/api/pessoas/{id}/", data=pessoa_payload)
            
            if result:
                print(f"✅ Pessoa editada com sucesso! Resultado: {result}", flush=True)
                
                # VALIDAÇÃO CRÍTICA: Comparar ANTES vs DEPOIS
                print(f"🔍 Verificando persistência...", flush=True)
                updated = self._make_request("GET", f"/api/pessoas/{id}/")
                print(f"📊 Dados após edição: {updated}", flush=True)
                
                # Verificar se campos críticos realmente mudaram
                print(f"\n🔎 VALIDAÇÃO DE PERSISTÊNCIA:", flush=True)
                campos_criticos = ['name', 'cpf', 'email', 'phone_number', 'nascimento']
                
                mudancas_confirmadas = []
                mudancas_nao_confirmadas = []
                
                for campo in campos_criticos:
                    valor_antes = current.get(campo)
                    valor_depois = updated.get(campo)
                    valor_solicitado = pessoa_payload.get(campo)
                    
                    if valor_antes != valor_depois:
                        mudancas_confirmadas.append(f"✅ {campo}: '{valor_antes}' → '{valor_depois}'")
                    elif valor_solicitado and valor_antes == valor_depois and valor_solicitado != valor_antes:
                        mudancas_nao_confirmadas.append(f"❌ {campo}: solicitado '{valor_solicitado}' mas permanece '{valor_depois}'")
                
                for msg in mudancas_confirmadas:
                    print(f"   {msg}", flush=True)
                
                for msg in mudancas_nao_confirmadas:
                    print(f"   {msg}", flush=True)
                
                if mudancas_nao_confirmadas:
                    print(f"\n⚠️  ALERTA: Algumas mudanças NÃO foram persistidas no backend!", flush=True)
                    print(f"   Isso indica um problema na API Django (serializer não está salvando)", flush=True)
                    print(f"   Tentando com PUT completo como fallback...", flush=True)
                    
                    # PUT completo como fallback
                    print(f"🔄 Enviando PUT para /api/pessoas/{id}/", flush=True)
                    result_put = self._make_request("PUT", f"/api/pessoas/{id}/", data=pessoa_payload)
                    
                    if result_put:
                        # Verificar novamente após PUT
                        updated_put = self._make_request("GET", f"/api/pessoas/{id}/")
                        print(f"📊 Dados após PUT: {updated_put}", flush=True)
                        
                        # Revisar
                        print(f"\n✅ Revisão após PUT:", flush=True)
                        for campo in campos_criticos:
                            valor_agora = updated_put.get(campo)
                            valor_solicitado = pessoa_payload.get(campo)
                            if valor_agora == valor_solicitado:
                                print(f"   ✅ {campo}: '{valor_agora}' (confirmado)", flush=True)
                            else:
                                print(f"   ❌ {campo}: solicitado '{valor_solicitado}' mas é '{valor_agora}'", flush=True)
                
                # NOVO: Sincronizar Usuario (usa CPF ANTIGO para encontrar o Usuario)
                # Se CPF mudou, primeiro atualiza o Usuario com CPF antigo, depois atualiza o CPF dele também
                if cpf_antigo:
                    self._sync_usuario_by_cpf(
                        cpf=cpf_antigo,  # ← USA CPF ANTIGO para encontrar!
                        email=person_dict.get("email"),
                        name=person_dict.get("name"),
                        phone=phone,
                        new_cpf=cpf_normalized if cpf_normalized != cpf_antigo else None  # ← Se mudou, passa o novo
                    )
                
                return len(mudancas_nao_confirmadas) == 0
            else:
                print(f"❌ Falha ao editar pessoa - resultado vazio", flush=True)
                return False

        except Exception as e:
            print(f"❌ ERRO em edit_person: {e}", flush=True)
            import traceback
            traceback.print_exc()
            raise
    
    def _sync_usuario_by_cpf(self, cpf: str, email: str = None, name: str = None, phone: str = None, new_cpf: str = None) -> bool:
        """
        Sincroniza dados do Usuario quando Person é editada
        Atualiza name, email, phone do Usuario que tem o mesmo CPF
        
        Args:
            cpf: CPF ANTIGO para encontrar o Usuario no banco
            email: Novo email (opcional)
            name: Novo nome (opcional)
            phone: Novo telefone (opcional)
            new_cpf: Novo CPF se foi alterado (opcional)
        """
        if not cpf:
            print(f"⚠️ CPF vazio, não sincronizando Usuario", flush=True)
            return False
        
        cpf_normalized = self._normalize_cpf(cpf)
        print(f"\n🔄 SYNC Usuario (CPF) - Original: '{cpf}' → Normalizado: '{cpf_normalized}'", flush=True)
        
        if not cpf_normalized or len(cpf_normalized) != 11:
            print(f"⚠️ CPF normalizado inválido (tem {len(cpf_normalized) if cpf_normalized else 0} dígitos, esperado 11)", flush=True)
            return False
        
        try:
            print(f"📤 Enviando PATCH /api/sync/usuario/cpf/", flush=True)
            print(f"   CPF (antigo): {cpf_normalized}", flush=True)
            if new_cpf:
                print(f"   CPF (novo): {new_cpf}", flush=True)
            if email:
                print(f"   Email: {email}", flush=True)
            if name:
                print(f"   Nome: {name}", flush=True)
            if phone:
                print(f"   Telefone: {phone}", flush=True)
            
            sync_data = {"cpf": cpf_normalized}
            if email:
                sync_data["email"] = email
            if name:
                sync_data["first_name"] = name
            if phone:
                sync_data["telefone"] = phone
            if new_cpf:
                sync_data["new_cpf"] = new_cpf  # ← Novo campo para atualizar CPF
            
            result = self._make_request("PATCH", "/api/sync/usuario/cpf/", data=sync_data)
            
            if result and 'id' in result:
                print(f"✅ Usuario ID {result['id']} sincronizado com sucesso", flush=True)
                return True
            else:
                print(f"⚠️ Sincronização retornou: {result}", flush=True)
                return False
        
        except Exception as e:
            print(f"⚠️ Erro ao sincronizar Usuario (CPF): {str(e)[:150]}", flush=True)
            # NÃO bloqueia a edição se sync falhar
            return False
    
    def delete_person(self, id: int) -> bool:
        """MESMA ASSINATURA DO SQLITE ANTIGO - Deleta Pessoa"""
        print(f"\n🔵 delete_person CHAMADO - ID: {id}", flush=True)
        
        try:
            # Recuperar dados da pessoa antes de deletar
            print(f"🔍 Buscando dados da pessoa ID {id}...", flush=True)
            person = self._make_request("GET", f"/api/pessoas/{id}/") or {}
            cpf = person.get("cpf")
            name = person.get("name")
            print(f"📊 Pessoa encontrada: {name} (CPF: {cpf})", flush=True)

            # DELETAR PESSOA
            print(f"🗑️ Deletando Pessoa ID {id}...", flush=True)
            result = self._make_request("DELETE", f"/api/pessoas/{id}/")
            
            if result is False or result is None:
                print(f"❌ API retornou FALSE/None para DELETE", flush=True)
                raise Exception("Falha ao excluir pessoa - API retornou false")
            
            print(f"✅ Pessoa deletada com sucesso!", flush=True)

            # Tentar deletar usuario associado (opcional, não bloqueia)
            if cpf:
                cpf_limpo = ''.join(filter(str.isdigit, cpf))
                try:
                    print(f"🗑️ Tentando deletar Usuario com CPF {cpf_limpo}...", flush=True)
                    usuario_result = self._make_request("DELETE", "/api/delete/usuario/cpf/", params={"cpf": cpf_limpo})
                    if usuario_result:
                        print(f"✅ Usuario deletado", flush=True)
                except Exception as e:
                    print(f"⚠️ Aviso: Usuario talvez já tenha sido deletado: {str(e)[:100]}", flush=True)
                    # NÃO bloqueia a deleção da pessoa
            
            return True

        except Exception as e:
            print(f"❌ ERRO em delete_person: {e}", flush=True)
            import traceback
            traceback.print_exc()
            raise
    
    def insert_company(self, company: Company, address: Address) -> dict:
        """MESMA ASSINATURA DO SQLITE ANTIGO"""
        try:
            print("\n" + "="*60)
            print("🏢 INSERT_COMPANY - Iniciando inserção de empresa")
            print("="*60)
            
            company_dict = to_dict(company)
            address_dict = to_dict(address)
            
            print(f"Empresa: {company_dict.get('company_name')}")
            print(f"CNPJ: {company_dict.get('cnpj')}")
            print(f"Email: {company_dict.get('email')}")
            
            # 1. Criar endereço
            endereco_data = {
                "cep": address_dict.get("cep", ""),
                "rua": address_dict.get("street", ""),
                "numero": address_dict.get("address_number", ""),
                "cidade": address_dict.get("city", ""),
                "estado": address_dict.get("state", ""),
                "pais": address_dict.get("country", "Brasil"),
            }
            
            print("📍 Criando endereço...")
            endereco_result = self._make_request("POST", "/api/enderecos/", data=endereco_data)
            
            if not endereco_result:
                raise Exception("Falha ao criar endereço")
            
            endereco_id = endereco_result.get("id")
            print(f"✅ Endereço criado: ID={endereco_id}")
            
            # 2. Criar empresa
            empresa_data = {
                "name": company_dict.get("company_name", ""),
                "cnpj": company_dict.get("cnpj", ""),
                "email": company_dict.get("email", ""),
                "telefone": company_dict.get("phone_number", ""),
                "endereco": endereco_id,
            }
            
            print("🏢 Criando empresa na API...")
            empresa_result = self._make_request("POST", "/api/empresas/", data=empresa_data)
            
            if not empresa_result or 'id' not in empresa_result:
                raise Exception("Falha ao criar empresa")
            
            print(f"✅ Empresa criada: ID={empresa_result.get('id')}")
            
            # 3. Registrar Usuario com CNPJ para permitir login (só se tiver email)
            if company_dict.get("email"):
                try:
                    registro_usuario_data = {
                        "first_name": company_dict.get("company_name", ""),
                        "email": company_dict.get("email", ""),
                        "cnpj": company_dict.get("cnpj", ""),
                        "phone_number": company_dict.get("phone_number", ""),  # ← Adiciona telefone!
                    }
                    
                    # print("🔐 Registrando usuario/envio de email...")
                    # print(f"   Endpoint: /api/register/empresa/")
                    # print(f"   Dados: {registro_usuario_data}")
                    
                    registro_result = self._make_request(
                        "POST", 
                        "/api/register/empresa/",
                        data=registro_usuario_data
                    )
                    
                    print(f"✅ Empresa e Usuario criados com sucesso")
                    print(f"   Email de acesso enviado para: {company_dict.get('email')}")
                    print("="*60 + "\n")
                    
                except Exception as user_error:
                    # Se falhar ao criar usuario, a empresa já foi criada
                    # Informar mas não quebrar o fluxo
                    print(f"⚠️ Aviso: Empresa criada mas erro ao registrar usuario/enviar email")
                    print(f"   Erro: {str(user_error)}")
                    print("="*60 + "\n")
                    
            return empresa_result
                
        except Exception as e:
            print(f"❌ ERRO em INSERT_COMPANY: {str(e)}")
            print("="*60 + "\n")
            raise
    
    def edit_company(self, company: Company, address: Address, id: int, requester_id: int) -> bool:
        """
        Edita uma Empresa existente no banco de dados via API Django.
        
        Args:
            company: Objeto Company com os novos dados
            address: Objeto Address com os novos dados de endereço
            id: ID da empresa a ser editada
            requester_id: ID do usuário que está fazendo a requisição
            
        Returns:
            bool: True se a edição foi bem sucedida, False caso contrário
        """
        print(f"\n🔵 edit_company CHAMADO - ID: {id}", flush=True)
        
        try:
            # Converte objetos para dicionários
            company_dict = to_dict(company)
            address_dict = to_dict(address)
            
            print(f"📋 company_dict: {company_dict}", flush=True)
            print(f"📋 address_dict: {address_dict}", flush=True)

            # Recupera dados atuais
            print(f"🔍 Buscando dados atuais de empresa ID {id}...", flush=True)
            current = self._make_request("GET", f"/api/empresas/{id}/") or {}
            print(f"📊 Dados atuais: {current}", flush=True)
            endereco_id = current.get("endereco")
            
            # Salva CNPJ antigo ANTES de normalizar o novo (para sync)
            cnpj_antigo = current.get("cnpj", "")
            print(f"🔖 CNPJ antigo no banco: '{cnpj_antigo}'", flush=True)

            # Atualiza ou cria endereço
            endereco_payload = {
                "cep": address_dict.get("cep", ""),
                "rua": address_dict.get("street", ""),
                "numero": address_dict.get("address_number", ""),
                "cidade": address_dict.get("city", ""),
                "estado": address_dict.get("state", ""),
                "pais": address_dict.get("country", "Brasil"),
            }
            
            print(f"📍 Payload de endereço: {endereco_payload}", flush=True)

            if endereco_id:
                print(f"✏️ Atualizando endereço ID {endereco_id}...", flush=True)
                self._make_request("PATCH", f"/api/enderecos/{endereco_id}/", data=endereco_payload)
            else:
                print(f"➕ Criando novo endereço...", flush=True)
                endereco_result = self._make_request("POST", "/api/enderecos/", data=endereco_payload)
                endereco_id = endereco_result.get("id") if endereco_result else None
                print(f"✅ Novo endereço criado - ID: {endereco_id}", flush=True)

            # Normaliza CNPJ (remove formatação)
            cnpj_raw = company_dict.get("cnpj", current.get("cnpj", ""))
            cnpj_normalized = self._normalize_cnpj(cnpj_raw)
            print(f"🆔 CNPJ - Original: '{cnpj_raw}' → Normalizado: '{cnpj_normalized}'", flush=True)

            # Monta payload da empresa
            empresa_payload = {
                "name": company_dict.get("company_name", current.get("name", "")),
                "cnpj": cnpj_normalized,
                "email": company_dict.get("email", current.get("email", "")),
                "telefone": company_dict.get("phone_number", current.get("telefone", "")),
            }

            if endereco_id:
                empresa_payload["endereco"] = endereco_id

            print(f"🏢 Payload final da empresa: {empresa_payload}", flush=True)
            print(f"🔄 Enviando PATCH para /api/empresas/{id}/", flush=True)
            
            # Usa PATCH ao invés de PUT
            result = self._make_request("PATCH", f"/api/empresas/{id}/", data=empresa_payload)
            
            if result:
                print(f"✅ Empresa editada com sucesso! Resultado: {result}", flush=True)
                
                # Verifica persistência
                print(f"🔍 Verificando persistência...", flush=True)
                updated = self._make_request("GET", f"/api/empresas/{id}/")
                print(f"📊 Dados após edição: {updated}", flush=True)
                
                # NOVO: Sincronizar Usuario (usa CNPJ ANTIGO para encontrar o Usuario)
                # Se CNPJ mudou, primeiro atualiza o Usuario com CNPJ antigo, depois atualiza o CNPJ dele também
                if cnpj_antigo:
                    self._sync_usuario_by_cnpj(
                        cnpj=cnpj_antigo,  # ← USA CNPJ ANTIGO para encontrar!
                        email=company_dict.get("email"),
                        name=company_dict.get("company_name"),
                        phone=company_dict.get("phone_number"),
                        new_cnpj=cnpj_normalized if cnpj_normalized != cnpj_antigo else None  # ← Se mudou, passa o novo
                    )
                
                return True
            else:
                print(f"❌ Falha ao editar empresa - resultado vazio", flush=True)
                return False

        except Exception as e:
            print(f"❌ ERRO em edit_company: {e}", flush=True)
            import traceback
            traceback.print_exc()
            raise
    
    def delete_company(self, id: int) -> bool:
        """MESMA ASSINATURA DO SQLITE ANTIGO - Deleta Empresa"""
        print(f"\n🔵 delete_company CHAMADO - ID: {id}", flush=True)
        
        try:
            # Recuperar dados da empresa antes de deletar
            print(f"🔍 Buscando dados da empresa ID {id}...", flush=True)
            empresa = self._make_request("GET", f"/api/empresas/{id}/") or {}
            cnpj = empresa.get("cnpj")
            name = empresa.get("name")
            print(f"📊 Empresa encontrada: {name} (CNPJ: {cnpj})", flush=True)

            # DELETAR EMPRESA
            print(f"🗑️ Deletando Empresa ID {id}...", flush=True)
            result = self._make_request("DELETE", f"/api/empresas/{id}/")
            
            if result is False or result is None:
                print(f"❌ API retornou FALSE/None para DELETE", flush=True)
                raise Exception("Falha ao excluir empresa - API retornou false")
            
            print(f"✅ Empresa deletada com sucesso!", flush=True)

            # Tentar deletar usuario associado (opcional, não bloqueia)
            if cnpj:
                cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
                try:
                    print(f"🗑️ Tentando deletar Usuario com CNPJ {cnpj_limpo}...", flush=True)
                    usuario_result = self._make_request("DELETE", "/api/delete/usuario/cnpj/", params={"cnpj": cnpj_limpo})
                    if usuario_result:
                        print(f"✅ Usuario deletado", flush=True)
                except Exception as e:
                    print(f"⚠️ Aviso: Usuario talvez já tenha sido deletado: {str(e)[:100]}", flush=True)
                    # NÃO bloqueia a deleção da empresa
            
            return True

        except Exception as e:
            print(f"❌ ERRO em delete_company: {e}", flush=True)
            import traceback
            traceback.print_exc()
            raise
    
    def _sync_usuario_by_cnpj(self, cnpj: str, email: str = None, name: str = None, phone: str = None, new_cnpj: str = None) -> bool:
        """
        Sincroniza dados do Usuario quando Empresa é editada
        Atualiza name, email, phone do Usuario que tem o mesmo CNPJ
        
        Args:
            cnpj: CNPJ ANTIGO para encontrar o Usuario no banco
            email: Novo email (opcional)
            name: Novo nome (opcional) 
            phone: Novo telefone (opcional)
            new_cnpj: Novo CNPJ se foi alterado (opcional)
        """
        if not cnpj:
            print(f"⚠️ CNPJ vazio, não sincronizando Usuario", flush=True)
            return False
        
        cnpj_normalized = self._normalize_cnpj(cnpj)
        print(f"\n🔄 SYNC Usuario (CNPJ) - Original: '{cnpj}' → Normalizado: '{cnpj_normalized}'", flush=True)
        
        if not cnpj_normalized or len(cnpj_normalized) != 14:
            print(f"⚠️ CNPJ normalizado inválido (tem {len(cnpj_normalized) if cnpj_normalized else 0} dígitos, esperado 14)", flush=True)
            return False
        
        try:
            print(f"📤 Enviando PATCH /api/sync/usuario/cnpj/", flush=True)
            print(f"   CNPJ (antigo): {cnpj_normalized}", flush=True)
            if new_cnpj:
                print(f"   CNPJ (novo): {new_cnpj}", flush=True)
            if email:
                print(f"   Email: {email}", flush=True)
            if name:
                print(f"   Nome: {name}", flush=True)
            if phone:
                print(f"   Telefone: {phone}", flush=True)
            
            sync_data = {"cnpj": cnpj_normalized}
            if email:
                sync_data["email"] = email
            if name:
                sync_data["first_name"] = name
            if phone:
                sync_data["telefone"] = phone
            if new_cnpj:
                sync_data["new_cnpj"] = new_cnpj  # ← Novo campo para atualizar CNPJ
            
            result = self._make_request("PATCH", "/api/sync/usuario/cnpj/", data=sync_data)
            
            if result and 'id' in result:
                print(f"✅ Usuario ID {result['id']} sincronizado com sucesso", flush=True)
                return True
            else:
                print(f"⚠️ Sincronização retornou: {result}", flush=True)
                return False
        
        except Exception as e:
            print(f"⚠️ Erro ao sincronizar Usuario (CNPJ): {str(e)[:150]}", flush=True)
            # NÃO bloqueia a edição se sync falhar
            return False
    
    def insert_property(self, property: Property, requester_id: int, address: Address) -> dict:
        """Cadastra propriedade - vinculada a uma Person OU Empresa"""
        print(f"\n🏠 Cadastrando propriedade...")
        
        # VALIDAÇÃO CRÍTICA: Requester é obrigatório
        if not requester_id:
            raise ValueError("❌ ERRO CRÍTICO: Propriedade DEVE ter um proprietário (pessoa ou empresa)!")
        
        print(f"   Proprietário ID: {requester_id}")
        
        property_dict = to_dict(property)
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
        
        print(f"   Criando endereço: {endereco_data.get('cidade')}/{endereco_data.get('estado')}")
        endereco_result = self._make_request("POST", "/api/enderecos/", data=endereco_data)

        if not endereco_result or 'id' not in endereco_result:
            raise Exception("❌ Falha ao criar endereço da propriedade")
        
        endereco_id = endereco_result.get("id")
        print(f"   ✅ Endereço criado: ID {endereco_id}")

        try:
            # 2. DETECTAR TIPO DE PROPRIETÁRIO: Person ou Empresa
            print(f"   Detectando tipo de proprietário (ID: {requester_id})...")
            
            proprietario_pessoa = None
            proprietario_empresa = None
            
            # Tentar primeiro como Person ID direto
            print(f"   Tentando como Person ID...")
            try:
                pessoa_response = self._make_request("GET", f"/api/pessoas/{requester_id}/")
                if pessoa_response and pessoa_response.get('id'):
                    print(f"   ✅ Detectado: PERSON (Pessoa) ID {requester_id}")
                    proprietario_pessoa = requester_id
            except Exception as e:
                print(f"   ✗ Não é Person ID: {e}")
            
            # Se não for Person, tentar como Empresa ID
            if proprietario_pessoa is None:
                print(f"   Tentando como Empresa ID...")
                try:
                    empresa_response = self._make_request("GET", f"/api/empresas/{requester_id}/")
                    if empresa_response and empresa_response.get('id'):
                        print(f"   ✅ Detectado: EMPRESA (Pessoa Jurídica) ID {requester_id}")
                        proprietario_empresa = requester_id
                except Exception as e:
                    print(f"   ✗ Não é Empresa ID: {e}")
            
            # Se não for Person nem Empresa direto, tentar converter Usuario ID
            if proprietario_pessoa is None and proprietario_empresa is None:
                print(f"   Tentando converter Usuario ID {requester_id} para Person...")
                try:
                    usuario_response = self._make_request("GET", f"/api/list/usuarios/{requester_id}/")
                    
                    if not usuario_response:
                        raise ValueError(
                            f"❌ ERRO CRÍTICO: Proprietário ID {requester_id} não encontrado "
                            f"como Person, Empresa ou Usuario! Propriedade NÃO PODE ser cadastrada."
                        )
                    
                    cpf = usuario_response.get('cpf')
                    if not cpf:
                        raise ValueError(f"❌ ERRO: Usuário {requester_id} não tem CPF cadastrado!")
                    
                    # Buscar Person pelo CPF
                    persons_response = self._make_request("GET", "/api/pessoas/", params={'cpf': cpf})
                    persons = self._unwrap_results(persons_response)
                    
                    if persons:
                        proprietario_pessoa = persons[0].get('id')
                        print(f"   ✅ Person encontrada para Usuario ID {requester_id}: Person ID {proprietario_pessoa}")
                    else:
                        # Criar nova Person no modelo report
                        print(f"   Criando Person no modelo report para Usuario {requester_id} (CPF {cpf})...")
                        usuario_data = usuario_response
                        person_payload = {
                            "name": usuario_data.get('name') or f"{usuario_data.get('first_name', '')} {usuario_data.get('last_name', '')}".strip(),
                            "cpf": cpf,
                            "email": usuario_data.get('email', ''),
                            "phone_number": usuario_data.get('telefone', ''),
                            "endereco": endereco_id,
                        }
                        
                        try:
                            person_response = self._make_request("POST", "/api/pessoas/", data=person_payload)
                            
                            # VALIDAÇÃO CRÍTICA: Person DEVE ser criada
                            if not person_response or 'id' not in person_response:
                                raise Exception("Resposta inválida ao criar Person")
                            
                            proprietario_pessoa = person_response.get('id')
                            print(f"   ✅ Person criada no modelo report: ID {proprietario_pessoa}")
                            
                        except Exception as e:
                            # Se falhar por CPF duplicado, tentar buscar novamente
                            if 'já está cadastrado' in str(e).lower() or 'cpf' in str(e).lower():
                                print(f"   ⚠️  CPF já existe, buscando Person existente...")
                                persons_retry = self._make_request("GET", "/api/pessoas/", params={'cpf': cpf})
                                persons_list = self._unwrap_results(persons_retry)
                                
                                if persons_list:
                                    proprietario_pessoa = persons_list[0].get('id')
                                    print(f"   ✅ Person encontrada: ID {proprietario_pessoa}")
                                else:
                                    raise Exception(
                                        f"❌ ERRO: Falha ao criar Person e não foi possível encontrá-la. "
                                        f"Erro original: {e}"
                                    )
                            else:
                                raise
                except Exception as e:
                    raise
            
            # VALIDAÇÃO FINAL: Garantir que temos um proprietário (Person OU Empresa)
            if proprietario_pessoa is None and proprietario_empresa is None:
                raise Exception(
                    f"❌ ERRO CRÍTICO: Não foi possível obter um proprietário válido! "
                    f"Propriedade NÃO PODE ser cadastrada."
                )

            # 3. Criar propriedade COM proprietário obrigatório
            proprietario_nome = proprietario_pessoa if proprietario_pessoa else proprietario_empresa
            proprietario_tipo = "Person" if proprietario_pessoa else "Empresa"
            proprietario_id = proprietario_pessoa if proprietario_pessoa else proprietario_empresa
            
            print(f"   Criando propriedade '{property_dict.get('name')}' para {proprietario_tipo} ID {proprietario_nome}...")
            
            data = {
                "name": property_dict["name"],
                "endereco": endereco_id,  
                "registration_number": property_dict.get("registration_number"),
                "localizacao": property_dict.get("localizacao", ""),
                "proprietario_id": proprietario_id,  # Campo genérico que aceita Person ou Empresa
            }
            
            print(f"   📤 Enviando para API: {data}")
            result = self._make_request("POST", "/api/propriedades/", data=data)

            if not result or "id" not in result:
                raise Exception("❌ Falha ao criar propriedade no servidor")

            print(f"✅ Propriedade cadastrada com sucesso!")
            print(f"   - Propriedade ID: {result.get('id')}")
            print(f"   - Proprietário ({proprietario_tipo}): {proprietario_nome}")
            return result
            
        except Exception as e:
            # Se falhar após criar endereço, logar o problema
            print(f"⚠️  AVISO: Endereço ID {endereco_id} foi criado mas propriedade falhou")
            raise
        
    def edit_property(self, property: Property, property_id: int, address: Address = None) -> bool:
        """
        Edita uma Propriedade existente no banco de dados via API Django.
        
        Args:
            property: Objeto Property com os novos dados
            property_id: ID da propriedade a ser editada
            address: Objeto Address opcional com os novos dados de endereço
            
        Returns:
            bool: True se a edição foi bem sucedida, False caso contrário
        """
        print(f"\n🔵 edit_property CHAMADO - ID: {property_id}", flush=True)
        
        try:
            # Converte objetos para dicionários
            property_dict = to_dict(property)
            print(f"📋 property_dict: {property_dict}", flush=True)

            # Recupera dados atuais
            print(f"🔍 Buscando dados atuais de propriedade ID {property_id}...", flush=True)
            current = self._make_request("GET", f"/api/propriedades/{property_id}/") or {}
            print(f"📊 Dados atuais: {current}", flush=True)

            endereco_id = None
            endereco = current.get("endereco") or current.get("endereco_id")
            endereco_id = endereco if isinstance(endereco, int) else None

            # Usar endereço passado como parâmetro, se disponível
            address_dict = to_dict(address) if address else {}
            
            # Atualizar endereço só se recebermos novos dados
            has_new_address = address and any(
                address_dict.get(field)
                for field in ("cep", "street", "address_number", "city", "state", "country")
            )

            if endereco_id and has_new_address:
                print(f"📍 Atualizando endereço da propriedade...", flush=True)
                endereco_atual = self._get_complete_address(endereco_id) or {}
                endereco_payload = {
                    "cep": address_dict.get("cep") or endereco_atual.get("cep", ""),
                    "rua": address_dict.get("street") or endereco_atual.get("rua", ""),
                    "numero": address_dict.get("address_number") or endereco_atual.get("numero", ""),
                    "cidade": address_dict.get("city") or endereco_atual.get("cidade", ""),
                    "estado": address_dict.get("state") or endereco_atual.get("estado", ""),
                    "pais": address_dict.get("country") or endereco_atual.get("pais", "Brasil"),
                }
                print(f"📍 Payload de endereço: {endereco_payload}", flush=True)
                self._make_request("PATCH", f"/api/enderecos/{endereco_id}/", data=endereco_payload)

            # Manter proprietário atual (Person ou Empresa)
            proprietario_pessoa = current.get("proprietario_pessoa")
            proprietario_empresa = current.get("proprietario_empresa")
            
            # Se vier dict, extrair ID
            if isinstance(proprietario_pessoa, dict):
                proprietario_pessoa = proprietario_pessoa.get("id")
            if isinstance(proprietario_empresa, dict):
                proprietario_empresa = proprietario_empresa.get("id")

            # Determinar qual proprietário usar (genérico)
            proprietario_id = proprietario_pessoa if proprietario_pessoa else proprietario_empresa
            
            if not proprietario_id:
                raise Exception(
                    "Proprietário da propriedade não identificado para atualização"
                )

            print(f"👤 Proprietário ID: {proprietario_id}", flush=True)

            # Monta payload da propriedade
            data = {
                "name": property_dict.get("name", current.get("name", "")),
                "registration_number": property_dict.get("registration_number", current.get("registration_number", "")),
                "localizacao": property_dict.get("localizacao", current.get("localizacao", "")),
                "proprietario_id": proprietario_id,  # Campo genérico
            }
            
            if endereco_id:
                data["endereco"] = endereco_id

            print(f"🏠 Payload final da propriedade: {data}", flush=True)
            print(f"🔄 Enviando PATCH para /api/propriedades/{property_id}/", flush=True)

            # Usa PATCH ao invés de PUT
            result = self._make_request("PATCH", f"/api/propriedades/{property_id}/", data=data)

            if result:
                print(f"✅ Propriedade editada com sucesso! Resultado: {result}", flush=True)
                
                # Verifica persistência
                print(f"🔍 Verificando persistência...", flush=True)
                updated = self._make_request("GET", f"/api/propriedades/{property_id}/")
                print(f"📊 Dados após edição: {updated}", flush=True)
                
                return True
            else:
                print(f"❌ Falha ao editar propriedade - resultado vazio", flush=True)
                return False

        except Exception as e:
            print(f"❌ ERRO em edit_property: {e}", flush=True)
            import traceback
            traceback.print_exc()
            raise

        except Exception as e:
            raise
    
    def delete_property(self, id: int) -> bool:
        """MESMA ASSINATURA DO SQLITE ANTIGO - Deleta Propriedade"""
        print(f"\n🔵 delete_property CHAMADO - ID: {id}", flush=True)
        
        try:
            # Recuperar dados da propriedade antes de deletar
            print(f"🔍 Buscando dados da propriedade ID {id}...", flush=True)
            propriedade = self._make_request("GET", f"/api/propriedades/{id}/") or {}
            name = propriedade.get("name")
            print(f"📊 Propriedade encontrada: {name}", flush=True)

            # DELETAR PROPRIEDADE
            print(f"🗑️ Deletando Propriedade ID {id}...", flush=True)
            result = self._make_request("DELETE", f"/api/propriedades/{id}/")
            
            if result is False or result is None:
                print(f"❌ API retornou FALSE/None para DELETE", flush=True)
                raise Exception("Falha ao excluir propriedade - API retornou false")
            
            print(f"✅ Propriedade deletada com sucesso!", flush=True)
            return True

        except Exception as e:
            print(f"❌ ERRO em delete_property: {e}", flush=True)
            import traceback
            traceback.print_exc()
            raise
    
    def insert_sample(self, sample: Sample, property_id: int, sample_number: int) -> dict:
        """MESMA ASSINATURA DO SQLITE ANTIGO"""
        try:
            sample_dict = to_dict(sample)

            # Verificar se a propriedade existe
            try:
                propriedade_info = self._make_request("GET", f"/api/propriedades/{property_id}/")
                if not propriedade_info:
                    raise Exception(f"Propriedade ID {property_id} não encontrada")
            except Exception as e:
                raise         
                
            # Enviar para o endpoint completo para persistir todos os campos
            data = {
                "propriedade_id": property_id,
                "numero_amostra": sample_number,
                "data_coleta": self._format_date(sample_dict.get("collection_date")),
                "descricao": sample_dict.get("description", f"Amostra {sample_number}"),
                # Parâmetros químicos
                "ph": sample_dict.get("ph"),
                "smp": sample_dict.get("smp"),
                "fosforo": sample_dict.get("phosphorus"),
                "potassio": sample_dict.get("potassium"),
                "materia_organica": sample_dict.get("organic_matter"),
                "aluminio": sample_dict.get("aluminum"),
                "h_al": sample_dict.get("h_al"),
                "calcio": sample_dict.get("calcium"),
                "magnesio": sample_dict.get("magnesium"),
                "cobre": sample_dict.get("copper"),
                "ferro": sample_dict.get("iron"),
                "manganes": sample_dict.get("manganese"),
                "zinco": sample_dict.get("zinc"),
                "soma_bases": sample_dict.get("base_sum"),
                "ctc": sample_dict.get("ctc"),
                "v_percent": sample_dict.get("v_percent"),
                "saturacao_aluminio": sample_dict.get("aluminum_saturation"),
                "ctc_efetiva": sample_dict.get("effective_ctc"),
                # Parâmetros físicos
                "argila": sample_dict.get("clay"),
                "silte": sample_dict.get("silte"),
                "areia": sample_dict.get("sand"),
                "classificacao": sample_dict.get("classification"),
                # Geo/metadata
                "area_total": sample_dict.get("total_area"),
                "latitude": sample_dict.get("latitude"),
                "longitude": sample_dict.get("longitude"),
                "profundidade": sample_dict.get("depth"),
            }

            result = self._make_request("POST", "/api/amostras/", data=data)
            
            if result and 'id' in result:
                return result
            elif isinstance(result, dict):
                raise Exception("Resposta da API sem ID da amostra")
            else:
                raise Exception("Falha ao criar amostra")
                
        except Exception as e:
            raise
    
    def edit_sample(self, sample: Sample, sample_id: int) -> bool:
        """
        Edita uma Amostra existente no banco de dados via API Django.
        
        Args:
            sample: Objeto Sample com os novos dados
            sample_id: ID da amostra a ser editada
            
        Returns:
            bool: True se a edição foi bem sucedida, False caso contrário
        """
        print(f"\n🔵 edit_sample CHAMADO - ID: {sample_id}", flush=True)
        
        try:
            # Converte objeto para dicionário
            sample_dict = to_dict(sample) or {}
            print(f"📋 sample_dict: {sample_dict}", flush=True)

            # Recupera dados atuais
            print(f"🔍 Buscando dados atuais de amostra ID {sample_id}...", flush=True)
            current = self._make_request("GET", f"/api/amostras/{sample_id}/") or {}
            print(f"📊 Dados atuais: {current}", flush=True)
            
            propriedade_id = current.get("propriedade") or sample_dict.get("fk_property_id")
            numero_amostra = current.get("numero_amostra") or sample_dict.get("sample_number")

            # Formata data de coleta
            collection_date_raw = sample_dict.get("collection_date") or current.get("data_coleta")
            collection_date_formatted = self._format_date(collection_date_raw)
            print(f"📅 Data coleta - Original: '{collection_date_raw}' → Formatada: '{collection_date_formatted}'", flush=True)

            # Construir payload com fallbacks seguros para todos os campos
            data = {
                "propriedade_id": propriedade_id,
                "numero_amostra": numero_amostra,
                "descricao": sample_dict.get("description") or current.get("descricao", ""),
                "data_coleta": collection_date_formatted,
                "ph": sample_dict.get("ph") or current.get("ph"),
                "smp": sample_dict.get("smp") or current.get("smp"),
                "fosforo": sample_dict.get("phosphorus") or current.get("fosforo"),
                "potassio": sample_dict.get("potassium") or current.get("potassio"),
                "materia_organica": sample_dict.get("organic_matter") or current.get("materia_organica"),
                "aluminio": sample_dict.get("aluminum") or current.get("aluminio"),
                "h_al": sample_dict.get("h_al") or current.get("h_al"),
                "calcio": sample_dict.get("calcium") or current.get("calcio"),
                "magnesio": sample_dict.get("magnesium") or current.get("magnesio"),
                "cobre": sample_dict.get("copper") or current.get("cobre"),
                "ferro": sample_dict.get("iron") or current.get("ferro"),
                "manganes": sample_dict.get("manganese") or current.get("manganes"),
                "zinco": sample_dict.get("zinc") or current.get("zinco"),
                "soma_bases": sample_dict.get("base_sum") or current.get("soma_bases"),
                "ctc": sample_dict.get("ctc") or current.get("ctc"),
                "v_percent": sample_dict.get("v_percent") or current.get("v_percent"),
                "saturacao_aluminio": sample_dict.get("aluminum_saturation") or current.get("saturacao_aluminio"),
                "ctc_efetiva": sample_dict.get("effective_ctc") or current.get("ctc_efetiva"),
                "argila": sample_dict.get("clay") or current.get("argila"),
                "silte": sample_dict.get("silte") or current.get("silte"),
                "areia": sample_dict.get("sand") or current.get("areia"),
                "classificacao": sample_dict.get("classification") or current.get("classificacao"),
                "area_total": sample_dict.get("total_area") or current.get("area_total"),
                "latitude": sample_dict.get("latitude") or current.get("latitude"),
                "longitude": sample_dict.get("longitude") or current.get("longitude"),
                "profundidade": sample_dict.get("depth") or current.get("profundidade"),
            }

            print(f"🧪 Payload final da amostra: {data}", flush=True)
            print(f"🔄 Enviando PATCH para /api/amostras/{sample_id}/", flush=True)

            # Usa PATCH ao invés de PUT
            result = self._make_request("PATCH", f"/api/amostras/{sample_id}/", data=data)

            if result:
                print(f"✅ Amostra editada com sucesso! Resultado: {result}", flush=True)
                
                # Verifica persistência
                print(f"🔍 Verificando persistência...", flush=True)
                updated = self._make_request("GET", f"/api/amostras/{sample_id}/")
                print(f"📊 Dados após edição: {updated}", flush=True)
                
                return True
            else:
                print(f"❌ Falha ao editar amostra - resultado vazio", flush=True)
                return False

        except Exception as e:
            print(f"❌ ERRO em edit_sample: {e}", flush=True)
            import traceback
            traceback.print_exc()
            raise
    
    def delete_sample(self, id: int) -> bool:
        """MESMA ASSINATURA DO SQLITE ANTIGO - Deleta Amostra"""
        print(f"\n🔵 delete_sample CHAMADO - ID: {id}", flush=True)
        
        try:
            # Recuperar dados da amostra antes de deletar
            print(f"🔍 Buscando dados da amostra ID {id}...", flush=True)
            amostra = self._make_request("GET", f"/api/amostras/{id}/") or {}
            numero_amostra = amostra.get("numero_amostra")
            print(f"📊 Amostra encontrada: Número {numero_amostra}", flush=True)

            # DELETAR AMOSTRA
            print(f"🗑️ Deletando Amostra ID {id}...", flush=True)
            result = self._make_request("DELETE", f"/api/amostras/{id}/")
            
            if result is False or result is None:
                print(f"❌ API retornou FALSE/None para DELETE", flush=True)
                raise Exception("Falha ao excluir amostra - API retornou false")
            
            print(f"✅ Amostra deletada com sucesso!", flush=True)
            return True

        except Exception as e:
            print(f"❌ ERRO em delete_sample: {e}", flush=True)
            import traceback
            traceback.print_exc()
            raise

    def insert_report(self, report: Report, sample_id: int) -> Optional[int]:
        """Insere laudo (PDF)"""
        report_dict = to_dict(report)
        
        # Buscar informações da amostra para pegar numero_amostra e data_coleta
        amostra = self._make_request("GET", f"/api/amostras/{sample_id}/")
        if not amostra:
            return None
        
        data = {
            "numero_amostra": amostra.get('numero_amostra'),
            "data_coleta": amostra.get('data_coleta') or datetime.now().strftime("%Y-%m-%d"),
            "propriedade": amostra.get('propriedade'),
            "ativo": True
        }
        
        result = self._make_request("POST", "/api/laudos/", data=data)
        
        if result and 'id' in result:
            # Fazer upload do arquivo PDF se houver
            file_location = report_dict.get("file_location")
            if file_location:
                upload_success = self._upload_report_pdf(result['id'], file_location)
                if not upload_success:
                    print(f"[AVISO] Falha ao fazer upload do PDF para laudo {result['id']}: {file_location}")
            
            return result['id']
        
        return None
    
    # ========== MÉTODOS DE CONSULTA (RETORNAM SQLiteRow) ==========
    
    def get_persons(self, **kwargs) -> list:
        """RETORNA LISTA DE SQLiteRow COMPATÍVEL"""
        try:
            print(f"\n👤 Buscando pessoas...")
            
            params = {}

            # Busca por ID (detalhe)
            if kwargs.get('id'):
                print(f"   Filtro: ID = {kwargs['id']}")
                response = self._make_request("GET", f"/api/pessoas/{kwargs['id']}/")
                pessoas = [response] if response else []
            else:
                # Filtros de lista
                cpf_in = kwargs.get('cpf')
                name = kwargs.get('name')

                if cpf_in:
                    print(f"   Filtro: CPF = {cpf_in}")
                    cpf_digits = ''.join(ch for ch in str(cpf_in) if ch.isdigit())
                    params['cpf'] = cpf_digits
                elif name:
                    print(f"   Filtro: Nome = {name}")
                    params['search'] = name

                # Buscar pessoas do endpoint /api/pessoas/
                response = self._make_request("GET", "/api/pessoas/", params=params)
                
                # Se vier paginado (dict com 'results'), usa a lista interna
                if isinstance(response, dict):
                    if 'results' in response:
                        pessoas = response.get('results', [])
                    else:
                        pessoas = [response] if response else []
                else:
                    pessoas = response if isinstance(response, list) else []

            formatted = []

            for pessoa in pessoas:
                if not pessoa:
                    continue
                
                # Buscar endereço se houver referência
                endereco_data = {}
                endereco_ref = pessoa.get('endereco')
                if endereco_ref:
                    endereco_data = self._get_complete_address(endereco_ref) or {}
                
                row_data = {
                    'id': pessoa.get('id'),
                    'name': pessoa.get('name', ''),
                    'birth_date': pessoa.get('nascimento', ''),
                    'cpf': pessoa.get('cpf', ''),
                    'email': pessoa.get('email', ''),
                    'phone_number': pessoa.get('phone_number', ''),
                    'requester_id': pessoa.get('id'),
                    'cep': endereco_data.get('cep', ''),
                    'address_number': endereco_data.get('numero', ''),
                    'address_id': endereco_ref,
                    'street': endereco_data.get('rua', ''),
                    'city': endereco_data.get('cidade', ''),
                    'state': endereco_data.get('estado', ''),
                    'country': endereco_data.get('pais', 'Brasil'),
                }

                formatted.append(SQLiteRow(row_data))

            print(f"✅ {len(formatted)} pessoa(s) encontrada(s)")
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

                # Lista decrescente por ID (mais recentes primeiro)
                params['ordering'] = '-id'

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
            return []

    
    def get_properties(self, **kwargs) -> list:
        """RETORNA LISTA DE SQLiteRow COMPATÍVEL"""
        try:
            # Buscar propriedades
            if kwargs.get('id'):
                result = self._make_request("GET", f"/api/propriedades/{kwargs['id']}/")
                propriedades = [result] if result else []
            else:
                result = self._make_request("GET", "/api/propriedades/", params={'ordering': '-id'})
                propriedades = self._unwrap_results(result)

            # Se não pedir filtro de requester, retorna todas
            if not kwargs.get('requester_id'):
                formatted = []
                for prop in propriedades:
                    endereco = prop.get("endereco_detalhes") or {}
                    location_value = (
                        prop.get('localizacao')
                        or f"{endereco.get('rua', '')}, {endereco.get('numero', '')}"
                    ).strip(', ')
                    
                    row_data = {
                        'id': prop.get('id'),
                        'name': prop.get('name', ''),
                        'registration_number': prop.get('registration_number', ''),
                        'localizacao': location_value,
                        'location': location_value,
                        'city': endereco.get('cidade', ''),
                        'state': endereco.get('estado', ''),
                        'country': endereco.get('pais', 'Brasil'),
                    }
                    formatted.append(SQLiteRow(row_data))
                
                print(f"   📋 {len(formatted)} propriedade(s) encontrada(s)")
                return formatted

            # ESTRATÉGIA: Filtrar em Python comparando proprietários
            requester_id = kwargs['requester_id']
            print(f"🔍 Filtrando propriedades para requester_id {requester_id} (em Python)...")
            
            formatted = []
            for prop in propriedades:
                # Extrair IDs de proprietário (pode vir como dict ou int)
                prop_pessoa = prop.get('proprietario_pessoa')
                prop_empresa = prop.get('proprietario_empresa')
                
                # Converter para int se for dict
                pessoa_id = None
                if prop_pessoa:
                    pessoa_id = prop_pessoa.get('id') if isinstance(prop_pessoa, dict) else prop_pessoa
                
                empresa_id = None
                if prop_empresa:
                    empresa_id = prop_empresa.get('id') if isinstance(prop_empresa, dict) else prop_empresa
                
                # Verificar se essa propriedade pertence ao requester
                if pessoa_id == requester_id or empresa_id == requester_id:
                    print(f"   ✅ Propriedade ID {prop.get('id')}: proprietario_pessoa={pessoa_id}, proprietario_empresa={empresa_id}")
                    
                    endereco = prop.get("endereco_detalhes") or {}
                    location_value = (
                        prop.get('localizacao')
                        or f"{endereco.get('rua', '')}, {endereco.get('numero', '')}"
                    ).strip(', ')
                    
                    row_data = {
                        'id': prop.get('id'),
                        'name': prop.get('name', ''),
                        'registration_number': prop.get('registration_number', ''),
                        'localizacao': location_value,
                        'location': location_value,
                        'city': endereco.get('cidade', ''),
                        'state': endereco.get('estado', ''),
                        'country': endereco.get('pais', 'Brasil'),
                    }
                    formatted.append(SQLiteRow(row_data))
            
            print(f"   📋 {len(formatted)} propriedade(s) encontrada(s) para requester_id {requester_id}")
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
                        'aluminum_saturation': amostra.get('saturacao_aluminio'),
                        'effective_ctc': amostra.get('ctc_efetiva'),
                        'used_config': amostra.get('config_usada'),
                        'smp': amostra.get('smp'),
                        'fk_property_id': amostra.get('propriedade'),
                    }
                formatted.append(SQLiteRow(row_data))
            
            return formatted
            
        except Exception as e:
            return []
    
    def get_sample_info(self, sample_id: int) -> SQLiteRow:
        """RETORNA SQLiteRow COMPATÍVEL para geração de laudo"""
        try:
            print(f"\n🔍 [get_sample_info] Buscando amostra ID {sample_id}...")
            amostra = self._make_request("GET", f"/api/amostras/{sample_id}/")
            if not amostra:
                print(f"❌ [get_sample_info] Amostra não encontrada")
                return SQLiteRow({})
            
            print(f"✅ [get_sample_info] Amostra encontrada: {amostra.get('numero_amostra')}")

            # Propriedade e endereço
            propriedade_id = amostra.get("propriedade")
            print(f"   Propriedade ID: {propriedade_id}")
            propriedade = None
            endereco = {}
            proprietario_id = None
            
            if propriedade_id:
                try:
                    propriedade = self._make_request("GET", f"/api/propriedades/{propriedade_id}/") or {}
                    print(f"   ✅ Propriedade: {propriedade.get('name')}")
                    
                    # Buscar endereço
                    endereco_ref = propriedade.get("endereco")
                    if endereco_ref:
                        endereco = self._get_complete_address(endereco_ref) or {}
                        print(f"   ✅ Endereço: {endereco.get('cidade')}/{endereco.get('estado')}")
                    
                    # Identificar proprietário ID
                    proprietario_id = propriedade.get("proprietario_pessoa") or propriedade.get("proprietario_empresa")
                    print(f"   Proprietário ID: {proprietario_id}")
                    
                except Exception as e:
                    print(f"❌ Erro ao buscar propriedade: {e}")
                    propriedade = {}

            # Proprietário (pessoa ou empresa)
            requester_name = ""
            document_number = ""
            document_type = ""
            
            if proprietario_id:
                # Tentar buscar como pessoa primeiro
                try:
                    pessoa = self._make_request("GET", f"/api/pessoas/{proprietario_id}/")
                    if pessoa:
                        requester_name = pessoa.get("name", "")
                        document_number = pessoa.get("cpf", "")
                        document_type = "cpf"
                        print(f"   ✅ Proprietário (Pessoa): {requester_name} - CPF {document_number}")
                except Exception:
                    # Se não for pessoa, tentar como empresa
                    try:
                        empresa = self._make_request("GET", f"/api/empresas/{proprietario_id}/")
                        if empresa:
                            requester_name = empresa.get("name", "")
                            document_number = empresa.get("cnpj", "")
                            document_type = "cnpj"
                            print(f"   ✅ Proprietário (Empresa): {requester_name} - CNPJ {document_number}")
                    except Exception as e:
                        print(f"❌ Erro ao buscar proprietário: {e}")

            row_data = {
                'sample_description': amostra.get('descricao', ''),
                'sample_number': amostra.get('numero_amostra'),
                'collection_date': amostra.get('data_coleta'),
                'depth': amostra.get('profundidade'),
                'total_area': amostra.get('area_total'),
                'property_name': propriedade.get('name', '') if propriedade else '',
                'registration_number': propriedade.get('registration_number', '') if propriedade else '',
                'city': endereco.get('cidade', '') if endereco else '',
                'state': endereco.get('estado', '') if endereco else '',
                'country': endereco.get('pais', 'Brasil') if endereco else 'Brasil',
                'requester_name': requester_name,
                'document_number': document_number,
                'document_type': document_type,
            }
            
            print(f"\n📋 [get_sample_info] Dados compilados:")
            print(f"   Solicitante: {requester_name} ({document_type.upper()}: {document_number})")
            print(f"   Propriedade: {row_data['property_name']} - {row_data['city']}/{row_data['state']}")
            print(f"   Amostra: {row_data['sample_number']} - Prof: {row_data['depth']}cm - Área: {row_data['total_area']}m²")
            print(f"✅ [get_sample_info] Row data retornado com sucesso\n")

            return SQLiteRow(row_data)

        except Exception as e:
            print(f"❌ [get_sample_info] Erro geral: {e}")
            import traceback
            traceback.print_exc()
            return SQLiteRow({})
    
    def get_report_info(self) -> list:
        """RETORNA LISTA DE SQLiteRow COMPATÍVEL"""
        try:
            result_list = self._make_request("GET", "/api/laudos/") or []
            # Debug para entender ausência de laudos
            try:
                size = len(result_list) if hasattr(result_list, '__len__') else 1
                print(f"[DEBUG] get_report_info: laudos recebidos = {size}")
            except Exception:
                pass

            # Se vier paginado (dict com 'results'), usa a lista interna
            if isinstance(result_list, dict) and 'results' in result_list:
                result_list = result_list['results'] or []

            formatted = []
            for laudo in result_list if isinstance(result_list, list) else [result_list]:
                if laudo:
                    # Agora o serializer já retorna solicitante_nome e propriedade_nome
                    row_data = {
                        'id': laudo.get('id') if hasattr(laudo, 'get') else None,
                        'requester_name': laudo.get('solicitante_nome', 'Não informado'),
                        'date': laudo.get('data_coleta') if hasattr(laudo, 'get') else None,
                        'property': laudo.get('propriedade_nome', 'Não informado'),
                    }
                    formatted.append(SQLiteRow(row_data))
            
            return formatted
            
        except Exception as e:
            print(f"[DEBUG] get_report_info erro: {e}")
            return []
    
    def publish_report(self, laudo_id: int) -> bool:
        """
        Publica um laudo (marca como revisado e disponível para produtor)
        Retorna True se sucesso, False caso contrário
        """
        try:
            print(f"\n📋 Publicando laudo ID={laudo_id}...")
            result = self._make_request("POST", f"/api/laudos/{laudo_id}/publicar/")
            
            if result and result.get('success'):
                print(f"✅ Laudo {laudo_id} publicado com sucesso!")
                print(f"   Data de publicação: {result.get('data_publicacao')}")
                return True
            else:
                print(f"⚠️ Laudo {laudo_id}: {result.get('message', 'Erro desconhecido')}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao publicar laudo {laudo_id}: {str(e)}")
            return False
    
    def upload_signed_report(self, laudo_id: int, file_path: str) -> bool:
        """
        Faz upload do PDF assinado para substituir o laudo original
        Retorna True se sucesso, False caso contrário
        """
        try:
            print(f"\n📄 Fazendo upload do PDF assinado para laudo ID={laudo_id}...")
            print(f"📁 Arquivo: {file_path}")
            
            success = self._upload_report_pdf(laudo_id, file_path)
            
            if success:
                print(f"✅ PDF assinado enviado com sucesso!")
                return True
            else:
                print(f"❌ Falha ao enviar PDF assinado")
                return False
        except Exception as e:
            print(f"❌ Erro ao fazer upload do PDF assinado: {str(e)}")
            return False
    
    def delete_report(self, laudo_id: int) -> bool:
        """
        Remove um laudo do sistema
        Retorna True se sucesso, False caso contrário
        """
        try:
            print(f"\n🗑️ Removendo laudo ID={laudo_id}...")
            
            response = self.session.delete(
                f"{self.base_url}/api/laudos/{laudo_id}/",
                headers=self.headers
            )
            
            if response.status_code == 204:  # No Content - sucesso na deleção
                print(f"✅ Laudo {laudo_id} removido com sucesso!")
                return True
            elif response.status_code == 404:
                print(f"⚠️ Laudo {laudo_id} não encontrado")
                return False
            else:
                print(f"❌ Erro ao remover laudo {laudo_id}: Status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao remover laudo {laudo_id}: {str(e)}")
            return False
    
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
                    return True
                else:
                    return False
        except Exception as e:
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