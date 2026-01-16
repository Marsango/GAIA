# report/views.py - VERSÃO CORRIGIDA
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import Propriedade, Laudo, Amostra, Empresa, Person, Endereco
from .serializers import PropriedadeSerializer, LaudoSerializer, AmostraSerializer, EmpresaSerializer, PersonSerializer, EnderecoSerializer
from django.utils import timezone

class PersonViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Person
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cpf', 'email']
    search_fields = ['name', 'cpf', 'email', 'phone_number']
    ordering_fields = ['name', 'nascimento']

class EnderecoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Endereco
    """
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cep', 'cidade', 'estado']
    search_fields = ['rua', 'cidade', 'estado', 'cep']
    ordering_fields = ['cidade', 'estado']

class PropriedadeViewSet(viewsets.ModelViewSet):
    queryset = Propriedade.objects.all()
    serializer_class = PropriedadeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Propriedade.objects.all()

class LaudoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para laudos - Compatível com software desktop
    """
    queryset = Laudo.objects.all()
    serializer_class = LaudoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['propriedade', 'ativo']
    search_fields = ['numero_amostra']
    
    def get_queryset(self):
        """Filtra laudos pelas propriedades do usuário"""
        queryset = super().get_queryset()
        
        # Filtra laudos das propriedades deste usuário
        queryset = queryset.filter(
            Q(propriedade__proprietario_pessoa=self.request.user) |
            Q(propriedade__proprietario_empresa__user=self.request.user)
        )
        # Filtro por propriedade específica
        propriedade_id = self.request.query_params.get('propriedade_id')
        if propriedade_id:
            queryset = queryset.filter(propriedade_id=propriedade_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def por_propriedade(self, request):
        """
        Endpoint específico para software desktop
        URL: /api/laudos/por_propriedade/?propriedade_id=1
        """
        propriedade_id = request.query_params.get('propriedade_id')
        
        if not propriedade_id:
            return Response(
                {'error': 'propriedade_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Verifica se propriedade pertence ao usuário
            propriedade = Propriedade.objects.get(
                id=propriedade_id,
                proprietario=self.request.user
            )
        except Propriedade.DoesNotExist:
            return Response(
                {'error': 'Propriedade não encontrada ou acesso negado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        laudos = self.get_queryset().filter(propriedade_id=propriedade_id, ativo=True)
        serializer = self.get_serializer(laudos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_pdf(self, request, pk=None):
        """Upload de arquivo PDF para laudo"""
        laudo = self.get_object()
        
        if 'arquivo_pdf' not in request.FILES:
            return Response(
                {'error': 'Nenhum arquivo enviado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        laudo.arquivo_pdf = request.FILES['arquivo_pdf']
        laudo.save()
        
        return Response({
            'success': True,
            'message': 'Arquivo enviado com sucesso',
            'url': laudo.arquivo_pdf.url
        })
    
    # Método create adaptado para software desktop
    def create(self, request, *args, **kwargs):
        """
        Criação de laudo compatível com software desktop
        Aceita os mesmos campos que o sistema antigo
        """
        data = request.data.copy()
        
        # Se propriedade_id for passado, converte para propriedade
        if 'propriedade_id' in data:
            data['propriedade'] = data.pop('propriedade_id')
        
        # Adiciona automaticamente o usuário da propriedade
        if 'propriedade' in data:
            try:
                propriedade = Propriedade.objects.get(
                    id=data['propriedade'],
                    proprietario=request.user
                )
            except Propriedade.DoesNotExist:
                return Response(
                    {'error': 'Propriedade não encontrada ou acesso negado'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AmostraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para amostras - IMPORTANTE: Amostra representa os "laudos" técnicos do sistema antigo
    """
    queryset = Amostra.objects.all()
    serializer_class = AmostraSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['propriedade', 'ativo', 'classificacao']
    search_fields = ['numero_amostra', 'descricao']
    
    def get_queryset(self):
        """Filtra amostras pelas propriedades do usuário"""
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(propriedade__proprietario_pessoa=self.request.user) |
            Q(propriedade__proprietario_empresa__user=self.request.user)
        )
        return queryset
    
    @action(detail=False, methods=['get'])
    def por_propriedade(self, request):
        """
        Endpoint para software desktop - Amostras por propriedade
        URL: /api/amostras/por_propriedade/?propriedade_id=1
        """
        propriedade_id = request.query_params.get('propriedade_id')
        
        if not propriedade_id:
            return Response(
                {'error': 'propriedade_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Verifica se propriedade pertence ao usuário
            propriedade = Propriedade.objects.get(
                id=propriedade_id
            )
            # Valida se propriedade pertence ao usuário
            if not (
                propriedade.proprietario_pessoa == self.request.user or
                (hasattr(propriedade.proprietario_empresa, 'user') and 
                 propriedade.proprietario_empresa.user == self.request.user)
            ):
                raise Propriedade.DoesNotExist()
        except Propriedade.DoesNotExist:
            return Response(
                {'error': 'Propriedade não encontrada ou acesso negado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        amostras = self.get_queryset().filter(propriedade_id=propriedade_id, ativo=True)
        serializer = self.get_serializer(amostras, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def criar_simples(self, request):
        """
        Criação simplificada para software desktop
        Mapeia campos antigos para novos
        """
        from datetime import date
        
        data = request.data.copy()
        
        # Mapeamento de campos para compatibilidade
        field_mapping = {
            'propriedade_id': 'propriedade',
            'numero_amostra': 'numero_amostra',
            'data_coleta': 'data_coleta',
            'ph': 'ph',
            'fosforo': 'fosforo',
            'potassio': 'potassio',
            'materia_organica': 'materia_organica',
            'descricao': 'descricao',
            'argila': 'argila',
            'silte': 'silte',
            'areia': 'areia',
            'classificacao': 'classificacao',
        }
        
        mapped_data = {}
        for old_field, new_field in field_mapping.items():
            if old_field in data:
                mapped_data[new_field] = data[old_field]
        
        # Validar que propriedade foi informada
        if 'propriedade' not in mapped_data:
            return Response(
                {'error': 'propriedade_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Gerar número de amostra automático se não informado
        if 'numero_amostra' not in mapped_data:
            try:
                ultima_amostra = Amostra.objects.filter(
                    propriedade=mapped_data['propriedade']
                ).order_by('-numero_amostra').first()
                if ultima_amostra:
                    mapped_data['numero_amostra'] = int(ultima_amostra.numero_amostra) + 1
                else:
                    mapped_data['numero_amostra'] = 1
            except (ValueError, TypeError):
                mapped_data['numero_amostra'] = 1
        
        # Definir data_coleta como hoje se não informada
        if 'data_coleta' not in mapped_data:
            mapped_data['data_coleta'] = str(date.today())
        
        serializer = self.get_serializer(data=mapped_data)
        serializer.is_valid(raise_exception=True)
        
        # Salva a amostra
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ========== ENDPOINT DE INFO PARA SOFTWARE DESKTOP ==========
@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """Informações da API para software desktop"""
    return Response({
        'name': 'Lab Solos API',
        'version': '1.0',
        'compatible_with': 'Software Desktop v2.0+',
        'description': 'API para integração do software desktop com sistema web',
        'models_supported': ['Propriedade', 'Laudo', 'Amostra'],
        'endpoints': {
            'auth': {
                'login': 'POST /api/token/',
                'refresh': 'POST /api/token/refresh/',
            },
            'propriedades': {
                'list': 'GET /api/propriedades/',
                'create': 'POST /api/propriedades/',
                'detail': 'GET /api/propriedades/{id}/',
                'buscar': 'GET /api/propriedades/buscar/?q=termo&cpf=...',
                'por_cpf': 'GET /api/propriedades/por_cpf/?cpf=...',
                'amostras': 'GET /api/propriedades/{id}/amostras/',
                'laudos': 'GET /api/propriedades/{id}/laudos/',
            },
            'laudos': {
                'list': 'GET /api/laudos/',
                'create': 'POST /api/laudos/',
                'detail': 'GET /api/laudos/{id}/',
                'por_propriedade': 'GET /api/laudos/por_propriedade/?propriedade_id=1',
                'upload_pdf': 'POST /api/laudos/{id}/upload_pdf/',
            },
            'amostras': {
                'list': 'GET /api/amostras/',
                'create': 'POST /api/amostras/',
                'detail': 'GET /api/amostras/{id}/',
                'por_propriedade': 'GET /api/amostras/por_propriedade/?propriedade_id=1',
                'criar_simples': 'POST /api/amostras/criar_simples/',
            }
        },
        'authentication': 'Bearer token JWT',
        'cors': 'Habilitado para todas as origens'
    })

# ========== ENDPOINT DE SAÚDE ==========
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Endpoint de verificação de saúde da API"""
    return Response({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0'
    })

# Endpoint para buscar usuário atual
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Retorna informações do usuário atual"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# Endpoint para empresas (se necessário)
class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]