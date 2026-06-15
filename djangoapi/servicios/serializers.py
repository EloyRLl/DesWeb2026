from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry

# Modelos
from .models import ZonaServicio, Tuberia, ArquetaPozo

# Clases base del profesor
from core.myLib.geoModelSerializer import GeoModelSerializer, GeomodelPolygonSerializer, GeomodelLinestringSerializer


class ZonaServicioSerializer(GeomodelPolygonSerializer):
    # 👇 FORZAMOS A DJANGO A MOSTRAR LA CAJA DE TEXTO EN LA WEB 👇
    geom = serializers.CharField(style={'base_template': 'textarea.html'}, help_text="Introduce WKT (ej. POLYGON((...)))")

    # Cumple: "Reject polygons that intersects with other polygons"
    check_geometry_is_valid = True 
    check_st_relation = True 
    matrix9IM = 'T********'  # Matriz para intersección de interiores

    class Meta:
        model = ZonaServicio
        fields = [
            'id', 
            'geom', 
            'nombre', 
            'poblacion_afectada', 
            'fecha_creacion', 
            'responsable', 
            'activa'
        ]

    def create(self, validated_data):
        validated_data.pop('area', None)
        validated_data.pop('perimeter', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('area', None)
        validated_data.pop('perimeter', None)
        return super().update(instance, validated_data)


class TuberiaSerializer(GeomodelLinestringSerializer):
    # 👇 FORZAMOS A DJANGO A MOSTRAR LA CAJA DE TEXTO EN LA WEB 👇
    geom = serializers.CharField(style={'base_template': 'textarea.html'}, help_text="Introduce WKT (ej. LINESTRING(0 0, 10 10))")

    # Cumple: "Reject linestrings than intersects with other linestrings"
    check_geometry_is_valid = True
    check_st_relation = True 
    matrix9IM = 'T********'  
    
    class Meta:
        model = Tuberia
        fields = [
            'id', 'geom', 'tamano_tubo', 'material', 'presion_maxima', 
            'fecha_instalacion', 'estado'
        ]

    def create(self, validated_data):
        validated_data.pop('length', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('length', None)
        return super().update(instance, validated_data)


class ArquetaPozoSerializer(GeoModelSerializer):
    # 👇 FORZAMOS A DJANGO A MOSTRAR LA CAJA DE TEXTO EN LA WEB 👇
    geom = serializers.CharField(style={'base_template': 'textarea.html'}, help_text="Introduce WKT (ej. POINT(X Y))")

    # Los puntos son siempre válidos y no se auto-cruzan
    check_geometry_is_valid = True 
    check_st_relation = False 
    
    class Meta:
        model = ArquetaPozo
        fields = [
            'id', 'geom', 'tipo_elemento', 'profundidad', 
            'fecha_mantenimiento', 'accesible', 'estado_conservacion'
        ]

    def validate_geom(self, value):
        wkb_geom = super().validate_geom(value)
        
        punto_geos = GEOSGeometry(wkb_geom)
        
        esta_dentro = ZonaServicio.objects.filter(geom__contains=punto_geos).exists()
        
        if not esta_dentro:
            raise serializers.ValidationError(
                "Operación rechazada: El punto de la Arqueta/Pozo debe estar estrictamente dentro de un polígono de ZonaServicio (ST_Within)."
            )
            
        return wkb_geom