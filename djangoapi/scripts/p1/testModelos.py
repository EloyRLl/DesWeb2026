# djangoapi/scripts/p1/testModelos.py

from servicios.models import ZonaServicio, Tuberia, ArquetaPozo
from django.contrib.gis.geos import GEOSGeometry

def run():
    print("--- INICIANDO TEST CON MODELOS DE DJANGO ---")

    # ---------------------------------------------------------
    # 1. PRUEBA: ZONAS DE SERVICIO (Polígonos)
    # ---------------------------------------------------------
    print("\n1. Insertando Zona de Servicio (Polígono)...")
    # GEOSGeometry convierte el texto WKT en un objeto geométrico de Django
    geom_zona = GEOSGeometry('POLYGON((0 0, 0 100, 100 100, 100 0, 0 0))', srid=25830)
    
    # Validamos la geometría y comprobamos que no intersecte con zonas ya existentes
    if not geom_zona.valid:
        print({'ok': False, 'message': 'Geometría no válida', 'data': []})
    elif ZonaServicio.objects.filter(geom__intersects=geom_zona).exists():
        print({'ok': False, 'message': 'El polígono interseca con zonas existentes', 'data': []})
    else:
        # Insertamos usando el método .create() de Django
        zona = ZonaServicio.objects.create(
            nombre='Sector Norte Django',
            poblacion_afectada=3000,
            fecha_creacion='2023-05-12',
            responsable='Aguas SA',
            activa=True,
            geom=geom_zona
        )
        print({'ok': True, 'message': 'Zona de servicio insertada', 'data': [{'id': zona.id}]})

    # ---------------------------------------------------------
    # 2. PRUEBA: TUBERÍAS (Líneas)
    # ---------------------------------------------------------
    print("\n2. Insertando Tubería (Línea)...")
    geom_tuberia = GEOSGeometry('LINESTRING(10 10, 50 50, 90 10)', srid=25830)
    tuberia = Tuberia.objects.create(
        tamano_tubo=400,
        material='PVC',
        presion_maxima=16.5,
        fecha_instalacion='2023-06-01',
        estado='Óptimo',
        geom=geom_tuberia
    )
    print({'ok': True, 'message': 'Tubería insertada', 'data': [{'id': tuberia.id}]})

    # ---------------------------------------------------------
    # 3. PRUEBA: ARQUETAS Y POZOS (Puntos) - DENTRO DEL POLÍGONO
    # ---------------------------------------------------------
    print("\n3. Insertando Arqueta DENTRO de la Zona de Servicio...")
    geom_arqueta_in = GEOSGeometry('POINT(50 50)', srid=25830)
    
    # REGLA TOPOLÓGICA CON DJANGO: Chequeamos si la arqueta cae dentro de alguna zona
    if not ZonaServicio.objects.filter(geom__intersects=geom_arqueta_in).exists():
        print({'ok': False, 'message': 'Regla Topológica fallida: La arqueta NO está dentro de ninguna Zona', 'data': []})
    else:
        arqueta1 = ArquetaPozo.objects.create(
            tipo_elemento='Pozo de Registro',
            profundidad=2.5,
            fecha_mantenimiento='2024-01-15',
            accesible=True,
            estado_conservacion='Limpio',
            geom=geom_arqueta_in
        )
        print({'ok': True, 'message': 'Punto insertado con éxito', 'data': [{'id': arqueta1.id}]})

    # ---------------------------------------------------------
    # 4. PRUEBA: ARQUETAS Y POZOS (Puntos) - FUERA DEL POLÍGONO
    # ---------------------------------------------------------
    print("\n4. Insertando Arqueta FUERA de la Zona de Servicio (Debería dar error)...")
    geom_arqueta_out = GEOSGeometry('POINT(200 200)', srid=25830)
    
    if not ZonaServicio.objects.filter(geom__intersects=geom_arqueta_out).exists():
        print({'ok': False, 'message': 'Regla Topológica fallida: La arqueta NO está dentro de ninguna Zona', 'data': []})
    else:
        arqueta2 = ArquetaPozo.objects.create(
            tipo_elemento='Arqueta', profundidad=1.2, fecha_mantenimiento='2024-02-10',
            accesible=False, estado_conservacion='Rota', geom=geom_arqueta_out
        )
        print({'ok': True, 'message': 'Punto insertado', 'data': [{'id': arqueta2.id}]})
        
    print("\n--- FIN DE LOS TESTS CON DJANGO ---")