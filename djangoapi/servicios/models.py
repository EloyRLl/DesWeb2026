from django.db import models
# IMPORTANTE: Para usar campos geoespaciales (PostGIS) importamos los modelos de GIS
from django.contrib.gis.db import models as gis_models
# Importamos el SRID (sistema de coordenadas) configurado globalmente en el proyecto
from djangoapi.settings import EPSG_FOR_GEOMETRIES

class ZonaServicio(models.Model):
    """
    Modelo 1: Representa áreas o regiones.
    Cumple el requisito de tipo de geometría: POLÍGONO (PolygonField).
    Tiene 5 campos normales + 1 geométrico.
    """
    nombre = models.CharField(max_length=100)
    poblacion_afectada = models.IntegerField()
    fecha_creacion = models.DateField()
    responsable = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)
    
    # Campo geométrico (Polígono) con el SRID dinámico de la plantilla
    geom = gis_models.PolygonField(srid=int(EPSG_FOR_GEOMETRIES))

    class Meta:
        db_table = 'zonas_servicio'  # Nombre con el que se creará la tabla en PostGIS

    def __str__(self):
        return self.nombre


class Tuberia(models.Model):
    """
    Modelo 2: Representa redes de distribución lineales.
    Cumple el requisito de tipo de geometría: LÍNEA (LineStringField).
    Tiene 5 campos normales + 1 geométrico.
    """
    tamano_tubo = models.IntegerField()
    material = models.CharField(max_length=50)
    presion_maxima = models.FloatField()
    fecha_instalacion = models.DateField()
    estado = models.CharField(max_length=50)
    
    # Campo geométrico (Línea)
    geom = gis_models.LineStringField(srid=int(EPSG_FOR_GEOMETRIES))

    class Meta:
        db_table = 'tuberias'

    def __str__(self):
        return f"Tubería de {self.material} ({self.tamano_tubo}mm)"


class ArquetaPozo(models.Model):
    """
    Modelo 3: Representa infraestructura puntual.
    Cumple el requisito de tipo de geometría: PUNTO (PointField).
    Tiene 5 campos normales + 1 geométrico.
    """
    tipo_elemento = models.CharField(max_length=50)
    profundidad = models.FloatField()
    fecha_mantenimiento = models.DateField()
    accesible = models.BooleanField(default=True)
    estado_conservacion = models.CharField(max_length=50)
    
    # Campo geométrico (Punto)
    geom = gis_models.PointField(srid=int(EPSG_FOR_GEOMETRIES))

    class Meta:
        db_table = 'arquetas_pozos'

    def __str__(self):
        return f"{self.tipo_elemento} (Profundidad: {self.profundidad}m)"