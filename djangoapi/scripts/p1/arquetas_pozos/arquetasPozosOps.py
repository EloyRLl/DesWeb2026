# djangoapi/scripts/p1/arquetas_pozos/arquetasPozosOps.py
from myLib.db import Db
from myLib import p1Settings as settings

class ArquetasPozosOps:
    
    def insert(self, d):
        db = Db(getRowsAsDicts=True)
        geom = d['geom']
        
        # 1. Validar la geometría
        q_val = "SELECT ST_IsValid(ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)) as is_valid"
        db.query(q_val, [geom, settings.EPSG_CODE, settings.SNAP_DISTANCE])
        if not db.result[0]['is_valid']:
            return {'ok': False, 'message': 'La geometría del punto no es válida.', 'data': []}
            
        # 2. REGLA TOPOLÓGICA: El punto debe caer DENTRO de una Zona de Servicio
        q_dentro = """
        SELECT id, nombre FROM d.zonas_servicio 
        WHERE ST_Intersects(geom, ST_SnapToGrid(ST_GeomFromText(%s, %s), %s))
        """
        db.query(q_dentro, [geom, settings.EPSG_CODE, settings.SNAP_DISTANCE])
        
        if len(db.result) == 0:
            return {'ok': False, 'message': 'Regla Topológica fallida: La arqueta/pozo NO está dentro de ninguna Zona de Servicio registrada.', 'data': []}
            
        # 3. Si todo es correcto, insertamos
        q_ins = """
        INSERT INTO d.arquetas_pozos (tipo_elemento, profundidad, fecha_mantenimiento, accesible, estado_conservacion, geom)
        VALUES (%s, %s, %s, %s, %s, ST_SnapToGrid(ST_GeomFromText(%s, %s), %s))
        RETURNING id
        """
        success, msg = db.query(q_ins, [
            d['tipo_elemento'], d['profundidad'], d['fecha_mantenimiento'], 
            d['accesible'], d['estado_conservacion'], 
            geom, settings.EPSG_CODE, settings.SNAP_DISTANCE
        ])
        
        if success and db.result:
            return {'ok': True, 'message': f"Punto insertado. (Pertenece a la zona: {db.result[0].get('nombre', 'Desconocida')})", 'data': [{'id': db.result[0]['id']}]}
        return {'ok': False, 'message': f'Error: {msg}', 'data': []}

    def update(self, d):
        db = Db(getRowsAsDicts=True)
        id_val = d['id']
        geom = d['geom']
        
        # Validar geometría
        q_val = "SELECT ST_IsValid(ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)) as is_valid"
        db.query(q_val, [geom, settings.EPSG_CODE, settings.SNAP_DISTANCE])
        if not db.result[0]['is_valid']:
            return {'ok': False, 'message': 'La nueva geometría no es válida.', 'data': []}
            
        # Validar que sigue cayendo dentro de un polígono tras moverlo
        q_dentro = """
        SELECT id FROM d.zonas_servicio 
        WHERE ST_Intersects(geom, ST_SnapToGrid(ST_GeomFromText(%s, %s), %s))
        """
        db.query(q_dentro, [geom, settings.EPSG_CODE, settings.SNAP_DISTANCE])
        if len(db.result) == 0:
            return {'ok': False, 'message': 'Regla Topológica fallida: Al mover el punto, este ha quedado fuera de las Zonas de Servicio.', 'data': []}
            
        # Actualizar
        q_upd = """
        UPDATE d.arquetas_pozos
        SET tipo_elemento=%s, profundidad=%s, fecha_mantenimiento=%s, accesible=%s, estado_conservacion=%s, 
            geom=ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)
        WHERE id=%s
        """
        success, msg = db.query(q_upd, [
            d['tipo_elemento'], d['profundidad'], d['fecha_mantenimiento'], 
            d['accesible'], d['estado_conservacion'], 
            geom, settings.EPSG_CODE, settings.SNAP_DISTANCE, id_val
        ])
        if success:
            return {'ok': True, 'message': 'Arqueta/Pozo actualizado.', 'data': [{'rows_updated': db.result}]}
        return {'ok': False, 'message': f'Error: {msg}', 'data': []}

    def delete(self, d):
        db = Db()
        success, msg = db.query("DELETE FROM d.arquetas_pozos WHERE id=%s", [d['id']])
        if success:
            return {'ok': True, 'message': 'Elemento borrado.', 'data': [{'rows_deleted': db.result}]}
        return {'ok': False, 'message': f'Error al borrar: {msg}', 'data': []}

    def selectAsDicts(self, d):
        db = Db(getRowsAsDicts=True)
        q_sel = "SELECT id, tipo_elemento, profundidad, fecha_mantenimiento, accesible, estado_conservacion, ST_AsText(geom) as geom FROM d.arquetas_pozos WHERE id=%s"
        success, msg = db.query(q_sel, [d['id']])
        if success and db.result:
            for row in db.result:
                if 'fecha_mantenimiento' in row and row['fecha_mantenimiento']:
                    row['fecha_mantenimiento'] = str(row['fecha_mantenimiento'])
            return {'ok': True, 'message': 'OK', 'data': db.result}
        return {'ok': False, 'message': 'No encontrado.', 'data': []}

    def selectAsTuples(self, d):
        db = Db(getRowsAsDicts=False)
        q_sel = "SELECT id, tipo_elemento, profundidad, fecha_mantenimiento, accesible, estado_conservacion, ST_AsText(geom) FROM d.arquetas_pozos WHERE id=%s"
        success, msg = db.query(q_sel, [d['id']])
        if success and db.result:
            return {'ok': True, 'message': 'OK', 'data': db.result}
        return {'ok': False, 'message': 'No encontrado.', 'data': []}