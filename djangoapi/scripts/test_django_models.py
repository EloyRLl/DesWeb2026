# djangoapi/scripts/test_django_models.py

from servicios.models import ZonaServicio, Tuberia, ArquetaPozo
from django.contrib.gis.geos import GEOSGeometry

class ZonasDjangoOps:
    def insert(self, d):
        # 1. Creamos y validamos la geometría con GeoDjango
        geom = GEOSGeometry(d['geom'], srid=25830)
        if not geom.valid:
            return {'ok': False, 'message': 'Geometría no válida.', 'data': []}
        
        # 2. Comprobamos si interseca con otras zonas existentes
        if ZonaServicio.objects.filter(geom__intersects=geom).exists():
            return {'ok': False, 'message': 'El polígono interseca con zonas existentes.', 'data': []}
            
        # 3. Guardamos en base de datos
        zona = ZonaServicio.objects.create(
            nombre=d['nombre'], poblacion_afectada=d['poblacion_afectada'],
            fecha_creacion=d['fecha_creacion'], responsable=d['responsable'],
            activa=d['activa'], geom=geom
        )
        return {'ok': True, 'message': 'Zona de servicio insertada (Django ORM).', 'data': [{'id': zona.id}]}


class TuberiasDjangoOps:
    def insert(self, d):
        geom = GEOSGeometry(d['geom'], srid=25830)
        if not geom.valid:
            return {'ok': False, 'message': 'Geometría no válida.', 'data': []}
            
        tuberia = Tuberia.objects.create(
            tamano_tubo=d['tamano_tubo'], material=d['material'],
            presion_maxima=d['presion_maxima'], fecha_instalacion=d['fecha_instalacion'],
            estado=d['estado'], geom=geom
        )
        return {'ok': True, 'message': 'Tubería insertada (Django ORM).', 'data': [{'id': tuberia.id}]}


class ArquetasDjangoOps:
    def insert(self, d):
        geom = GEOSGeometry(d['geom'], srid=25830)
        if not geom.valid:
            return {'ok': False, 'message': 'Geometría no válida.', 'data': []}
            
        # --- REGLA TOPOLÓGICA OBLIGATORIA ---
        # El punto debe estar dentro (intersectar) con alguna Zona de Servicio
        if not ZonaServicio.objects.filter(geom__intersects=geom).exists():
            return {'ok': False, 'message': 'Regla Topológica: La arqueta NO está dentro de ninguna Zona de Servicio.', 'data': []}
            
        arqueta = ArquetaPozo.objects.create(
            tipo_elemento=d['tipo_elemento'], profundidad=d['profundidad'],
            fecha_mantenimiento=d['fecha_mantenimiento'], accesible=d['accesible'],
            estado_conservacion=d['estado_conservacion'], geom=geom
        )
        return {'ok': True, 'message': 'Arqueta insertada (Django ORM).', 'data': [{'id': arqueta.id}]}


# La función run() es obligatoria para poder usar 'python manage.py runscript'
def run():
    print("\n--- INICIANDO TEST CON MODELOS DE DJANGO ---")
    
    # Limpiamos los datos previos de Django para que el test se pueda repetir sin chocar
    ZonaServicio.objects.all().delete()
    Tuberia.objects.all().delete()
    ArquetaPozo.objects.all().delete()

    zonas_ops = ZonasDjangoOps()
    tuberias_ops = TuberiasDjangoOps()
    arquetas_ops = ArquetasDjangoOps()

    print("\n1. Insertando Zona de Servicio...")
    res_zona = zonas_ops.insert({
        'nombre': 'Sector Norte Django', 'poblacion_afectada': 3000,
        'fecha_creacion': '2023-05-12', 'responsable': 'Aguas SA',
        'activa': True, 'geom': 'POLYGON((0 0, 0 100, 100 100, 100 0, 0 0))'
    })
    print(res_zona)

    print("\n2. Insertando Tubería...")
    res_tuberia = tuberias_ops.insert({
        'tamano_tubo': 400, 'material': 'PVC', 'presion_maxima': 16.5,
        'fecha_instalacion': '2023-06-01', 'estado': 'Óptimo',
        'geom': 'LINESTRING(10 10, 50 50, 90 10)'
    })
    print(res_tuberia)

    print("\n3. Insertando Arqueta DENTRO (Debería funcionar)...")
    res_arqueta_ok = arquetas_ops.insert({
        'tipo_elemento': 'Pozo', 'profundidad': 2.5,
        'fecha_mantenimiento': '2024-01-15', 'accesible': True,
        'estado_conservacion': 'Limpio', 'geom': 'POINT(50 50)'
    })
    print(res_arqueta_ok)

    print("\n4. Insertando Arqueta FUERA (Debería fallar por la regla topológica)...")
    res_arqueta_fail = arquetas_ops.insert({
        'tipo_elemento': 'Arqueta', 'profundidad': 1.2,
        'fecha_mantenimiento': '2024-02-10', 'accesible': False,
        'estado_conservacion': 'Rota', 'geom': 'POINT(200 200)'
    })
    print(res_arqueta_fail)
    print("\n--- FIN DE LOS TESTS CON DJANGO ---\n")