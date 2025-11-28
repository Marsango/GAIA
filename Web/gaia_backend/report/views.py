from rest_framework import viewsets, filters
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Propriedade, Laudo
from .serializers import PropriedadeSerializer, LaudoSerializer
from authentication.models import Usuario 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class PropriedadeViewSet(viewsets.ModelViewSet):
    """API para propriedades - CRUD completo"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    serializer_class = PropriedadeSerializer
    queryset = Propriedade.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Mostra apenas propriedades do usuário logado
            return Propriedade.objects.filter(proprietario=user)
        return Propriedade.objects.none()

class LaudoViewSet(viewsets.ModelViewSet):
    serializer_class = LaudoSerializer
    queryset = Laudo.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['data_coleta']
    search_fields = ['numero_amostra']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Laudo.objects.filter(propriedade__proprietario=user, ativo=True)
        return Laudo.objects.none()
    
    @action(detail=False, methods=['get'])
    def por_propriedade(self, request):
        propriedade_id = request.query_params.get('propriedade_id')
        if propriedade_id:
            laudos = self.get_queryset().filter(propriedade_id=propriedade_id)
            serializer = self.get_serializer(laudos, many=True)
            return Response(serializer.data)
        return Response([])

@api_view(['POST'])
def sync_propriedade(request):
    """API simples para o software cadastrar propriedades"""
    try:
        data = request.data
        
        # Encontra o proprietário pelo CPF
        proprietario_cpf = data.get('proprietario_cpf')
        try:
            proprietario = Usuario.objects.get(cpf=proprietario_cpf)
        except Usuario.DoesNotExist:
            return Response({
                'error': f'Proprietário com CPF {proprietario_cpf} não encontrado'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Cria a propriedade
        propriedade = Propriedade.objects.create(
            nome=data.get('nome'),
            localizacao=data.get('localizacao', ''),
            proprietario=proprietario
        )
        
        return Response({
            'id': propriedade.id,
            'status': 'created',
            'message': 'Propriedade criada com sucesso'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def sync_laudo(request):
    """API simples para o software cadastrar laudos"""
    try:
        data = request.data
        
        # Encontra a propriedade
        propriedade_nome = data.get('propriedade_nome')
        proprietario_cpf = data.get('proprietario_cpf')
        
        try:
            propriedade = Propriedade.objects.get(
                nome=propriedade_nome,
                proprietario__cpf=proprietario_cpf
            )
        except Propriedade.DoesNotExist:
            return Response({
                'error': f'Propriedade {propriedade_nome} não encontrada'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Cria o laudo
        laudo = Laudo.objects.create(
            numero_amostra=data.get('numero_amostra'),
            data_coleta=data.get('data_coleta'),
            arquivo_pdf=data.get('arquivo_pdf'),
            propriedade=propriedade
        )
        
        return Response({
            'id': laudo.id,
            'status': 'created', 
            'message': 'Laudo criado com sucesso'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)