from rest_framework import viewsets, permissions
from .models import ZonaServicio, Tuberia, ArquetaPozo
from .serializers import ZonaServicioSerializer, TuberiaSerializer, ArquetaPozoSerializer

class ZonaServicioViewSet(viewsets.ModelViewSet):
    queryset = ZonaServicio.objects.all()
    serializer_class = ZonaServicioSerializer
    permission_classes = [permissions.AllowAny]

class TuberiaViewSet(viewsets.ModelViewSet):
    queryset = Tuberia.objects.all()
    serializer_class = TuberiaSerializer
    permission_classes = [permissions.AllowAny]

class ArquetaPozoViewSet(viewsets.ModelViewSet):
    queryset = ArquetaPozo.objects.all()
    serializer_class = ArquetaPozoSerializer
    permission_classes = [permissions.AllowAny]