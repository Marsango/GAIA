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