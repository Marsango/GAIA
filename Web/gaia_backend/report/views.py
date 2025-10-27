from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Propriedade, Laudo
from .serializers import PropriedadeSerializer, LaudoSerializer

class PropriedadeViewSet(viewsets.ModelViewSet):
    """API para propriedades - CRUD completo"""
    serializer_class = PropriedadeSerializer
    queryset = Propriedade.objects.all()
    
    def get_queryset(self):
        # Retorna apenas propriedades do usuário logado
        # return Propriedade.objects.filter(
        #     proprietario=self.request.user, 
        #     ativo=True
        # )
        return Propriedade.objects.all()

# class LaudoViewSet(viewsets.ModelViewSet):
#     """API para laudos - CRUD completo"""
#     serializer_class = LaudoSerializer
#     queryset = Laudo.objects.all()  # ← ADICIONE ESTA LINHA
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     filterset_fields = ['data_coleta']
#     search_fields = ['numero_amostra']
    
#     def get_queryset(self):
#         # Retorna apenas laudos das propriedades do usuário logado
#         return Laudo.objects.filter(
#             propriedade__proprietario=self.request.user,
#             ativo=True
#         ).select_related('propriedade')
    
#     @action(detail=False, methods=['get'])
#     def por_propriedade(self, request):
#         """Laudos de uma propriedade específica: /api/laudos/por_propriedade/?propriedade_id=1"""
#         propriedade_id = request.query_params.get('propriedade_id')
#         if propriedade_id:
#             laudos = self.get_queryset().filter(propriedade_id=propriedade_id)
#             serializer = self.get_serializer(laudos, many=True)
#             return Response(serializer.data)
#         return Response([])

class LaudoViewSet(viewsets.ModelViewSet):
    serializer_class = LaudoSerializer
    queryset = Laudo.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['data_coleta']
    search_fields = ['numero_amostra']
    
    def get_queryset(self):
        # COMENTE o filtro por usuário temporariamente:
        # return Laudo.objects.filter(
        #     propriedade__proprietario=self.request.user,
        #     ativo=True
        # ).select_related('propriedade')
        
        return Laudo.objects.filter(ativo=True).select_related('propriedade')
    
    @action(detail=False, methods=['get'])
    def por_propriedade(self, request):
        propriedade_id = request.query_params.get('propriedade_id')
        if propriedade_id:
            laudos = self.get_queryset().filter(propriedade_id=propriedade_id)
            serializer = self.get_serializer(laudos, many=True)
            return Response(serializer.data)
        return Response([])