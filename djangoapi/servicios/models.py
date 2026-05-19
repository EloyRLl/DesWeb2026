from django.contrib.gis.db import models

class ZonaServicio(models.Model):
    nombre = models.CharField(max_length=100)
    poblacion_afectada = models.IntegerField()
    fecha_creacion = models.DateField()
    responsable = models.CharField(max_length=100)
    activa = models.BooleanField()
    geom = models.PolygonField(srid=25830)

    class Meta:
        managed = False
        db_table = 'd"."zonas_servicio'


    def __str__(self):
        return self.nombre

class Tuberia(models.Model):
    tamano_tubo = models.IntegerField()
    material = models.CharField(max_length=50)
    presion_maxima = models.FloatField()
    fecha_instalacion = models.DateField()
    estado = models.CharField(max_length=50)
    geom = models.LineStringField(srid=25830)

    class Meta:
        managed = False
        db_table = 'd"."tuberias'

    def __str__(self):
        return f"Tubería {self.material} ({self.tamano_tubo}mm)"

class ArquetaPozo(models.Model):
    tipo_elemento = models.CharField(max_length=50)
    profundidad = models.FloatField()
    fecha_mantenimiento = models.DateField()
    accesible = models.BooleanField()
    estado_conservacion = models.CharField(max_length=50)
    geom = models.PointField(srid=25830)

    class Meta:
        managed = False
        db_table = 'd"."arquetas_pozos'

    def __str__(self):
        return self.tipo_elemento