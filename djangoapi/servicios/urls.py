from django.urls import path, include
from rest_framework import routers
from . import views

# El enrutador
router = routers.DefaultRouter()
router.register(r'zonas_servicio', views.ZonaServicioViewSet)
router.register(r'tuberias', views.TuberiaViewSet)
router.register(r'arquetas_pozos', views.ArquetaPozoViewSet)

# OJO AQUÍ: Debe llamarse exactamente 'urlpatterns'
urlpatterns = [
    path('', include(router.urls)),
]