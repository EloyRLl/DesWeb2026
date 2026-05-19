# djangoapi/scripts/p1/djangoOps.py

from servicios.models import ZonaServicio, Tuberia, ArquetaPozo
from django.contrib.gis.geos import GEOSGeometry

import ast

# ... (Aquí van tus clases ZonasDjangoOps, TuberiasDjangoOps, ArquetasDjangoOps) ...


class ZonasDjangoOps:
    def insert(self, d):
        try:
            geom = GEOSGeometry(d['geom'], srid=25830)
            if not geom.valid:
                return {'ok': False, 'message': 'Geometría no válida.', 'data': []}
            
            if ZonaServicio.objects.filter(geom__intersects=geom).exists():
                return {'ok': False, 'message': 'El polígono interseca con zonas existentes.', 'data': []}
                
            zona = ZonaServicio.objects.create(
                nombre=d['nombre'], poblacion_afectada=d['poblacion_afectada'],
                fecha_creacion=d['fecha_creacion'], responsable=d['responsable'],
                activa=d['activa'], geom=geom
            )
            return {'ok': True, 'message': 'Zona de servicio insertada.', 'data': [{'id': zona.id}]}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def update(self, d):
        try:
            geom = GEOSGeometry(d['geom'], srid=25830)
            if not geom.valid:
                return {'ok': False, 'message': 'Geometría no válida.', 'data': []}
            
            # Comprobamos que no choque con OTROS polígonos (excluimos el nuestro)
            if ZonaServicio.objects.exclude(id=d['id']).filter(geom__intersects=geom).exists():
                return {'ok': False, 'message': 'El polígono interseca con otras zonas.', 'data': []}
                
            ZonaServicio.objects.filter(id=d['id']).update(
                nombre=d['nombre'], poblacion_afectada=d['poblacion_afectada'],
                fecha_creacion=d['fecha_creacion'], responsable=d['responsable'],
                activa=d['activa'], geom=geom
            )
            return {'ok': True, 'message': 'Zona de servicio actualizada.', 'data': [{'id': d['id']}]}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def delete(self, d):
        try:
            eliminados, _ = ZonaServicio.objects.filter(id=d['id']).delete()
            if eliminados > 0:
                return {'ok': True, 'message': 'Zona borrada correctamente.', 'data': []}
            return {'ok': False, 'message': 'Zona no encontrada.', 'data': []}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def selectAsDicts(self, d):
        try:
            # .values() devuelve un diccionario directamente en Django
            zona = ZonaServicio.objects.filter(id=d['id']).values().first()
            if zona:
                zona['geom'] = zona['geom'].wkt # Pasamos la geometría a texto legible
                return {'ok': True, 'message': 'OK', 'data': [zona]}
            return {'ok': False, 'message': 'Zona no encontrada.', 'data': []}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}


class ArquetasDjangoOps:
    def insert(self, d):
        try:
            geom = GEOSGeometry(d['geom'], srid=25830)
            if not geom.valid:
                return {'ok': False, 'message': 'Geometría no válida.', 'data': []}
                
            # REGLA TOPOLÓGICA
            if not ZonaServicio.objects.filter(geom__intersects=geom).exists():
                return {'ok': False, 'message': 'Regla Topológica: La arqueta NO está dentro de ninguna Zona.', 'data': []}
                
            arqueta = ArquetaPozo.objects.create(
                tipo_elemento=d['tipo_elemento'], profundidad=d['profundidad'],
                fecha_mantenimiento=d['fecha_mantenimiento'], accesible=d['accesible'],
                estado_conservacion=d['estado_conservacion'], geom=geom
            )
            return {'ok': True, 'message': 'Arqueta insertada.', 'data': [{'id': arqueta.id}]}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def update(self, d):
        try:
            geom = GEOSGeometry(d['geom'], srid=25830)
            if not geom.valid:
                return {'ok': False, 'message': 'Geometría no válida.', 'data': []}
                
            # REGLA TOPOLÓGICA AL ACTUALIZAR (por si han movido el punto de sitio)
            if not ZonaServicio.objects.filter(geom__intersects=geom).exists():
                return {'ok': False, 'message': 'Regla Topológica: Al moverla, la arqueta ha quedado fuera de las Zonas.', 'data': []}
                
            ArquetaPozo.objects.filter(id=d['id']).update(
                tipo_elemento=d['tipo_elemento'], profundidad=d['profundidad'],
                fecha_mantenimiento=d['fecha_mantenimiento'], accesible=d['accesible'],
                estado_conservacion=d['estado_conservacion'], geom=geom
            )
            return {'ok': True, 'message': 'Arqueta actualizada.', 'data': [{'id': d['id']}]}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def delete(self, d):
        try:
            eliminados, _ = ArquetaPozo.objects.filter(id=d['id']).delete()
            if eliminados > 0:
                return {'ok': True, 'message': 'Arqueta borrada.', 'data': []}
            return {'ok': False, 'message': 'Arqueta no encontrada.', 'data': []}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def selectAsDicts(self, d):
        try:
            arqueta = ArquetaPozo.objects.filter(id=d['id']).values().first()
            if arqueta:
                arqueta['geom'] = arqueta['geom'].wkt
                return {'ok': True, 'message': 'OK', 'data': [arqueta]}
            return {'ok': False, 'message': 'No encontrada.', 'data': []}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}



class TuberiasDjangoOps:
    def insert(self, d):
        try:
            geom = GEOSGeometry(d['geom'], srid=25830)
            if not geom.valid:
                return {'ok': False, 'message': 'Geometría no válida.', 'data': []}
                
            tuberia = Tuberia.objects.create(
                tamano_tubo=d['tamano_tubo'], 
                material=d['material'],
                presion_maxima=d['presion_maxima'], 
                fecha_instalacion=d['fecha_instalacion'],
                estado=d['estado'], 
                geom=geom
            )
            return {'ok': True, 'message': 'Tubería insertada correctamente.', 'data': [{'id': tuberia.id}]}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def update(self, d):
        try:
            geom = GEOSGeometry(d['geom'], srid=25830)
            if not geom.valid:
                return {'ok': False, 'message': 'Geometría no válida.', 'data': []}
                
            # Guardamos el resultado del update en una variable
            filas_afectadas = Tuberia.objects.filter(id=d['id']).update(
                tamano_tubo=d['tamano_tubo'], 
                material=d['material'],
                presion_maxima=d['presion_maxima'], 
                fecha_instalacion=d['fecha_instalacion'],
                estado=d['estado'], 
                geom=geom
            )
            
            # Comprobamos si realmente se ha actualizado algo
            if filas_afectadas == 0:
                return {'ok': False, 'message': f"No se encontró ninguna tubería con el ID {d['id']}.", 'data': []}
                
            return {'ok': True, 'message': 'Tubería actualizada correctamente.', 'data': [{'id': d['id']}]}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def delete(self, d):
        try:
            eliminados, _ = Tuberia.objects.filter(id=d['id']).delete()
            if eliminados > 0:
                return {'ok': True, 'message': 'Tubería borrada correctamente.', 'data': []}
            return {'ok': False, 'message': 'Tubería no encontrada.', 'data': []}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}

    def selectAsDicts(self, d):
        try:
            tuberia = Tuberia.objects.filter(id=d['id']).values().first()
            if tuberia:
                tuberia['geom'] = tuberia['geom'].wkt
                return {'ok': True, 'message': 'OK', 'data': [tuberia]}
            return {'ok': False, 'message': 'Tubería no encontrada.', 'data': []}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': []}
        
# Reemplaza la función run() del final por esta:
def run(*args):
    # args es una tupla con todos los parámetros pasados tras --script-args
    if len(args) == 3:
        table_name = args[0]
        operation = args[1]
        
        # Convertimos el string del diccionario a un diccionario real de Python
        try:
            data_dict = ast.literal_eval(args[2])
        except Exception as e:
            print("Error: El formato del diccionario no es válido.")
            print("Detalle:", e)
            return

        # 1. Enrutamiento de la Tabla
        if table_name == "zonas_servicio":
            ops = ZonasDjangoOps()
        elif table_name == "tuberias":
            ops = TuberiasDjangoOps()
        elif table_name == "arquetas_pozos":
            ops = ArquetasDjangoOps()
        else:
            print("Error: Tabla no reconocida. Usa: zonas_servicio, tuberias o arquetas_pozos")
            return

        # 2. Enrutamiento de la Operación
        if operation == "insert":
            print(ops.insert(data_dict))
        elif operation == "update":
            print(ops.update(data_dict))
        elif operation == "delete":
            print(ops.delete(data_dict))
        elif operation == "select":
            print(ops.selectAsDicts(data_dict))
        else:
            print("Error: Operación no reconocida. Usa: insert, update, delete o select")
            