#!/usr/bin/env python
"""
Script para popular o banco de dados com dados de teste
para testar responsividade do site
Cria 1-2 usuários com várias propriedades, amostras e laudos
"""
import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from report.models import Endereco, Person, Empresa, Propriedade, Amostra, Laudo
from authentication.models import Usuario
from django.contrib.auth.hashers import make_password

# ==================== DADOS PARA TESTE ====================

CIDADES = [
    ("Curitiba", "PR"),
    ("Londrina", "PR"),
    ("Maringá", "PR"),
    ("São Paulo", "SP"),
    ("Campinas", "SP"),
    ("Ribeirão Preto", "SP"),
    ("Goiânia", "GO"),
    ("Brasília", "DF"),
]

NOMES_PROPRIEDADES = [
    "Fazenda Santa Clara",
    "Sítio Verde",
    "Propriedade Bom Resultado",
    "Granja Montanha Alta",
    "Chácara do Vale",
    "Fazenda Rio Grande",
    "Propriedade São João",
    "Sítio do Recanto",
    "Granja Esperança",
    "Fazenda Boa Vista",
    "Fazenda Nova Esperança",
    "Sítio das Pedras",
    "Propriedade Central",
    "Granja do Vale",
    "Fazenda Maravilha",
]

# ==================== FUNÇÕES ====================

def criar_enderecos(quantidade=10):
    """Cria endereços teste"""
    print(f"\n📍 Criando {quantidade} endereços...")
    enderecos = []
    
    for i in range(quantidade):
        cidade, estado = random.choice(CIDADES)
        endereco = Endereco.objects.create(
            cep=f"8000{i:03d}",
            rua=f"Rua {random.choice(['do Comércio', 'Principal', 'Santo Antônio', 'das Flores', 'Central'])}",
            numero=str(random.randint(100, 9999)),
            cidade=cidade,
            estado=estado,
            pais="Brasil"
        )
        enderecos.append(endereco)
        print(f"   ✅ Endereço {i+1}: {endereco.rua}, {endereco.numero} - {cidade}/{estado}")
    
    return enderecos

def criar_usuario_pessoa_fisica(enderecos):
    """Cria um usuário pessoa física com CPF"""
    print(f"\n👤 Criando usuário PESSOA FÍSICA...")
    
    cpf = "12345678901"
    usuario = Usuario.objects.create(
        username="pessoa_teste",
        first_name="João",
        last_name="Silva",
        email="pessoa@labsolos.test",
        cpf=cpf,
        cnpj=None,
        telefone="(46) 98901-2345",
        is_staff=False,
        is_active=True,
        primeiro_acesso=False
    )
    usuario.set_password("senha123")
    usuario.save()
    
    print(f"   ✅ Usuário: {usuario.first_name} {usuario.last_name}")
    print(f"   📧 Email: {usuario.email}")
    print(f"   🆔 CPF: {cpf}")
    print(f"   🔐 Senha: senha123")
    
    return usuario

def criar_usuario_empresa(enderecos):
    """Cria um usuário empresa com CNPJ"""
    print(f"\n🏢 Criando usuário EMPRESA...")
    
    cnpj = "12345678000190"
    usuario = Usuario.objects.create(
        username="empresa_teste",
        first_name="Agrícola",
        last_name="Teste Ltda",
        email="empresa@labsolos.test",
        cpf=None,
        cnpj=cnpj,
        telefone="(46) 3333-4444",
        is_staff=False,
        is_active=True,
        primeiro_acesso=False
    )
    usuario.set_password("senha123")
    usuario.save()
    
    print(f"   ✅ Usuário: {usuario.first_name} {usuario.last_name}")
    print(f"   📧 Email: {usuario.email}")
    print(f"   🆔 CNPJ: {cnpj}")
    print(f"   🔐 Senha: senha123")
    
    return usuario

def criar_propriedades(usuarios, enderecos, quantidade_por_usuario=8):
    """Cria propriedades vinculadas aos usuários"""
    print(f"\n🏠 Criando propriedades ({quantidade_por_usuario} por usuário)...")
    propriedades = []
    
    contador = 1
    for usuario in usuarios:
        tipo_user = "PESSOA FÍSICA" if usuario.cpf else "EMPRESA"
        print(f"\n   👤 Propriedades do usuário: {usuario.first_name} ({tipo_user})")
        
        # Criar Person ou Empresa correspondente ao usuário
        if usuario.cpf:
            # Criar Person para PF
            proprietario_pessoa = Person.objects.create(
                name=f"{usuario.first_name} {usuario.last_name}",
                cpf=usuario.cpf,
                email=usuario.email,
                phone_number=usuario.telefone,
                endereco=random.choice(enderecos)
            )
            proprietario_empresa = None
        else:
            # Criar Empresa para PJ
            proprietario_pessoa = None
            proprietario_empresa = Empresa.objects.create(
                name=f"{usuario.first_name} {usuario.last_name}",
                cnpj=usuario.cnpj,
                email=usuario.email,
                telefone=usuario.telefone,
                endereco=random.choice(enderecos)
            )
        
        # Criar propriedades vinculadas
        for i in range(quantidade_por_usuario):
            propriedade = Propriedade.objects.create(
                name=f"{random.choice(NOMES_PROPRIEDADES)} {contador}",
                registration_number=random.randint(1000000, 9999999),
                localizacao=f"Fazenda {contador}, Km {random.randint(10, 100)} - BR",
                endereco=random.choice(enderecos),
                proprietario_pessoa=proprietario_pessoa,
                proprietario_empresa=proprietario_empresa,
                usuario=usuario,  # ← Adiciona referência ao usuário também
            )
            propriedades.append(propriedade)
            print(f"      ✅ Propriedade {i+1}: {propriedade.name}")
            contador += 1
    
    return propriedades

def criar_amostras(propriedades, quantidade_por_propriedade=3):
    """Cria amostras de solo"""
    print(f"\n🧪 Criando amostras ({quantidade_por_propriedade} por propriedade)...")
    amostras = []
    
    contador = 1
    total_amostras = len(propriedades) * quantidade_por_propriedade
    
    for propriedade in propriedades:
        for j in range(quantidade_por_propriedade):
            data_coleta = datetime.now() - timedelta(days=random.randint(1, 90))
            
            amostra = Amostra.objects.create(
                numero_amostra=contador,
                data_coleta=data_coleta.date(),
                descricao=f"Amostra coletada em {['gleba 1', 'gleba 2', 'linha central', 'fundo da propriedade'][j % 4]}",
                propriedade=propriedade,
                area_total=random.uniform(10, 200),
                latitude=random.uniform(-27, -22),
                longitude=random.uniform(-52, -48),
                profundidade=random.choice([10, 15, 20, 25]),
                
                # Parâmetros químicos
                ph=round(random.uniform(4.5, 7.5), 2),
                smp=round(random.uniform(3.0, 7.0), 2),
                fosforo=round(random.uniform(5, 50), 2),
                potassio=round(random.uniform(30, 300), 2),
                materia_organica=round(random.uniform(1.5, 8.0), 2),
                aluminio=round(random.uniform(0, 3), 2),
                h_al=round(random.uniform(0.5, 10), 2),
                calcio=round(random.uniform(0.5, 8), 2),
                magnesio=round(random.uniform(0.2, 4), 2),
                cobre=round(random.uniform(0.5, 5), 2),
                ferro=round(random.uniform(10, 100), 2),
                manganes=round(random.uniform(1, 10), 2),
                zinco=round(random.uniform(0.5, 15), 2),
                soma_bases=round(random.uniform(1, 15), 2),
                ctc=round(random.uniform(5, 30), 2),
                v_percent=round(random.uniform(10, 90), 2),
                saturacao_aluminio=round(random.uniform(0, 50), 2),
                ctc_efetiva=round(random.uniform(5, 30), 2),
                
                # Parâmetros físicos
                argila=round(random.uniform(10, 60), 2),
                silte=round(random.uniform(10, 50), 2),
                areia=round(random.uniform(10, 70), 2),
                classificacao=random.choice(["AD0", "AD1", "AD2", "AD3", "AD4", "AD5", "AD6"]),
            )
            amostras.append(amostra)
            contador += 1
            
            if contador % 20 == 0:
                print(f"   ✅ {contador}/{total_amostras} amostras criadas...")
    
    print(f"   ✅ Total: {len(amostras)} amostras criadas!")
    return amostras

def criar_laudos(amostras):
    """Cria laudos (metade com PDF, metade sem)"""
    print(f"\n📄 Criando laudos para amostras...")
    
    laudos = []
    contador = 0
    
    for i, amostra in enumerate(amostras):
        laudo = Laudo.objects.create(
            numero_amostra=amostra.numero_amostra,
            data_coleta=amostra.data_coleta,
            propriedade=amostra.propriedade,
            ativo=True,
            publicado=random.choice([True, False, True]),  # 2/3 publicados
        )
        laudos.append(laudo)
        contador += 1
        
        if contador % 20 == 0:
            print(f"   ✅ {contador} laudos criados...")
    
    print(f"   ✅ Total: {len(laudos)} laudos criados!")
    print(f"   📊 Laudos publicados: ~{len([l for l in laudos if l.publicado])}/{len(laudos)}")
    
    return laudos

# ==================== MAIN ====================

def popular_banco():
    """Função principal para popular o banco"""
    
    print("\n" + "="*70)
    print(" POPULANDO BANCO DE DADOS COM DADOS DE TESTE")
    print("="*70)
    
    try:
        # Limpar dados antigos (opcional)
        print("\n Limpando dados antigos...")
        Laudo.objects.all().delete()
        Amostra.objects.all().delete()
        Propriedade.objects.all().delete()
        Usuario.objects.filter(username__contains="teste").delete()
        Endereco.objects.all().delete()
        print("   ✅ Dados antigos removidos")
        
        # Criar dados
        enderecos = criar_enderecos(quantidade=15)
        
        # Criar usuários
        usuario_pf = criar_usuario_pessoa_fisica(enderecos)
        usuario_pj = criar_usuario_empresa(enderecos)
        usuarios = [usuario_pf, usuario_pj]
        
        # Criar propriedades (8 por usuário)
        propriedades = criar_propriedades(usuarios, enderecos, quantidade_por_usuario=8)
        
        # Criar amostras (3 por propriedade)
        amostras = criar_amostras(propriedades, quantidade_por_propriedade=3)

        # Criar mais de 50 amostras na MESMA DATA para outra propriedade
        propriedade_muitas_amostras = propriedades[1]
        data_unica = datetime.now().date()
        print(
            f"\n🧪 Criando 55 amostras na mesma data para: {propriedade_muitas_amostras.name}..."
        )
        ultimo_numero_amostra = Amostra.objects.all().order_by('numero_amostra').last()
        proximo_numero_amostra = (
            ultimo_numero_amostra.numero_amostra + 1 if ultimo_numero_amostra else 1
        )
        amostras_extras = []
        for i in range(55):
            amostra_extra = Amostra.objects.create(
                numero_amostra=proximo_numero_amostra + i,
                data_coleta=data_unica,
                descricao="Amostra extra coletada no mesmo dia",
                propriedade=propriedade_muitas_amostras,
                area_total=random.uniform(10, 200),
                latitude=random.uniform(-27, -22),
                longitude=random.uniform(-52, -48),
                profundidade=random.choice([10, 15, 20, 25]),
                ph=round(random.uniform(4.5, 7.5), 2),
                smp=round(random.uniform(3.0, 7.0), 2),
                fosforo=round(random.uniform(5, 50), 2),
                potassio=round(random.uniform(30, 300), 2),
                materia_organica=round(random.uniform(1.5, 8.0), 2),
                aluminio=round(random.uniform(0, 3), 2),
                h_al=round(random.uniform(0.5, 10), 2),
                calcio=round(random.uniform(0.5, 8), 2),
                magnesio=round(random.uniform(0.2, 4), 2),
                cobre=round(random.uniform(0.5, 5), 2),
                ferro=round(random.uniform(10, 100), 2),
                manganes=round(random.uniform(1, 10), 2),
                zinco=round(random.uniform(0.5, 15), 2),
                soma_bases=round(random.uniform(1, 15), 2),
                ctc=round(random.uniform(5, 30), 2),
                v_percent=round(random.uniform(10, 90), 2),
                saturacao_aluminio=round(random.uniform(0, 50), 2),
                ctc_efetiva=round(random.uniform(5, 30), 2),
                argila=round(random.uniform(10, 60), 2),
                silte=round(random.uniform(10, 50), 2),
                areia=round(random.uniform(10, 70), 2),
                classificacao=random.choice(["AD0", "AD1", "AD2", "AD3", "AD4", "AD5", "AD6"]),
            )
            amostras_extras.append(amostra_extra)
        amostras.extend(amostras_extras)
        print(f"   ✅ 55 amostras extras criadas para {propriedade_muitas_amostras.name}!")

        # Criar laudos
        laudos = criar_laudos(amostras)

        # Criar mais de 50 laudos adicionais para a primeira propriedade de João
        primeira_propriedade = propriedades[0]
        print(f"\n📄 Criando 60 laudos adicionais para: {primeira_propriedade.name}...")
        # Descobrir o próximo numero_amostra
        ultimo_numero = Laudo.objects.all().order_by('numero_amostra').last()
        proximo_numero = (ultimo_numero.numero_amostra + 1) if ultimo_numero else 1

        for i in range(60):
            Laudo.objects.create(
                numero_amostra=proximo_numero + i,
                data_coleta=datetime.now().date(),
                propriedade=primeira_propriedade,
                ativo=True,
                publicado=random.choice([True, False, True]),
            )
        print(f"   ✅ 60 laudos adicionais criados para {primeira_propriedade.name}!")
        
        # Resumo
        print("\n" + "="*70)
        print("✅ DADOS POPULADOS COM SUCESSO!")
        print("="*70)
        print(f"📍 Endereços criados: {Endereco.objects.count()}")
        print(f"👤 Usuários criados: {len(usuarios)}")
        print(f"   - Pessoa Física: {usuario_pf.first_name} (CPF: {usuario_pf.cpf})")
        print(f"   - Empresa: {usuario_pj.first_name} (CNPJ: {usuario_pj.cnpj})")
        print(f"🏠 Propriedades: {Propriedade.objects.count()} (8 por usuário)")
        print(f"🧪 Amostras: {Amostra.objects.count()} (3 por propriedade)")
        print(f"📄 Laudos: {Laudo.objects.count()}")
        
        print("\n" + "="*70)
        print("🔐 CREDENCIAIS DE TESTE")
        print("="*70)
        print(f"\n👤 PESSOA FÍSICA:")
        print(f"   Email: pessoa@labsolos.test")
        print(f"   Senha: senha123")
        print(f"\n🏢 EMPRESA:")
        print(f"   Email: empresa@labsolos.test")
        print(f"   Senha: senha123")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO ao popular banco: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    popular_banco()

