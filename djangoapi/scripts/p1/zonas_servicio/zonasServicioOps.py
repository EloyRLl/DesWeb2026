# djangoapi/scripts/p1/zonas_servicio/zonasServicioOps.py
from myLib.db import Db
from myLib import p1Settings as settings

class ZonasServicioOps:
    
    def insert(self, d):
        db = Db(getRowsAsDicts=True)
        geom = d['geom']
        
        # 1. Validar la geometría después de redondearla a la distancia Snap
        q_val = "SELECT ST_IsValid(ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)) as is_valid"
        success, msg = db.query(q_val, [geom, settings.EPSG_CODE, settings.SNAP_DISTANCE])
        if not success or not db.result[0]['is_valid']:
            return {'ok': False, 'message': 'La geometría del polígono no es válida.', 'data': []}
            
        # 2. Comprobar que no interseca con otras zonas de servicio
        q_int = """
        SELECT id FROM d.zonas_servicio 
        WHERE ST_Intersects(geom, ST_SnapToGrid(ST_GeomFromText(%s, %s), %s))
        """
        db.query(q_int, [geom, settings.EPSG_CODE, settings.SNAP_DISTANCE])
        if len(db.result) > 0:
            # Extraemos los IDs que chocan para informar
            ids_conflictivos = [row['id'] for row in db.result]
            return {'ok': False, 'message': f'El polígono interseca con las zonas: {ids_conflictivos}. Inserción rechazada.', 'data': []}
            
        # 3. Si todo es correcto, insertamos
        q_ins = """
        INSERT INTO d.zonas_servicio (nombre, poblacion_afectada, fecha_creacion, responsable, activa, geom)
        VALUES (%s, %s, %s, %s, %s, ST_SnapToGrid(ST_GeomFromText(%s, %s), %s))
        RETURNING id
        """
        success, msg = db.query(q_ins, [
            d['nombre'], d['poblacion_afectada'], d['fecha_creacion'], 
            d['responsable'], d['activa'], 
            geom, settings.EPSG_CODE, settings.SNAP_DISTANCE
        ])
        
        if success and db.result:
            inserted_id = db.result[0]['id']
            return {'ok': True, 'message': 'Zona de servicio insertada correctamente.', 'data': [{'id': inserted_id}]}
        else:
            return {'ok': False, 'message': f'Error en base de datos: {msg}', 'data': []}

    def update(self, d):
        db = Db(getRowsAsDicts=True)
        id_val = d['id']
        geom = d['geom']
        
        # 1. Validar la nueva geometría
        q_val = "SELECT ST_IsValid(ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)) as is_valid"
        db.query(q_val, [geom, settings.EPSG_CODE, settings.SNAP_DISTANCE])
        if not db.result[0]['is_valid']:
            return {'ok': False, 'message': 'La nueva geometría del polígono no es válida.', 'data': []}
            
        # 2. Comprobar que no interseca con OTROS polígonos (excluimos el propio ID que estamos actualizando)
        q_int = """
        SELECT id FROM d.zonas_servicio 
        WHERE ST_Intersects(geom, ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)) 
        AND id != %s
        """
        db.query(q_int, [geom, settings.EPSG_CODE, settings.SNAP_DISTANCE, id_val])
        if len(db.result) > 0:
            ids_conflictivos = [row['id'] for row in db.result]
            return {'ok': False, 'message': f'El polígono modificado interseca con las zonas: {ids_conflictivos}.', 'data': []}
            
        # 3. Actualizar
        q_upd = """
        UPDATE d.zonas_servicio
        SET nombre=%s, poblacion_afectada=%s, fecha_creacion=%s, responsable=%s, activa=%s, 
            geom=ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)
        WHERE id=%s
        """
        success, msg = db.query(q_upd, [
            d['nombre'], d['poblacion_afectada'], d['fecha_creacion'], 
            d['responsable'], d['activa'], 
            geom, settings.EPSG_CODE, settings.SNAP_DISTANCE, id_val
        ])
        
        if success:
            return {'ok': True, 'message': 'Zona de servicio actualizada.', 'data': [{'rows_updated': db.result}]}
        else:
            return {'ok': False, 'message': f'Error: {msg}', 'data': []}

    def delete(self, d):
        db = Db()
        q_del = "DELETE FROM d.zonas_servicio WHERE id=%s"
        success, msg = db.query(q_del, [d['id']])
        if success:
            return {'ok': True, 'message': 'Zona de servicio borrada.', 'data': [{'rows_deleted': db.result}]}
        return {'ok': False, 'message': f'Error al borrar: {msg}', 'data': []}

    def selectAsDicts(self, d):
        db = Db(getRowsAsDicts=True)
        q_sel = """
        SELECT id, nombre, poblacion_afectada, fecha_creacion, responsable, activa, ST_AsText(geom) as geom 
        FROM d.zonas_servicio WHERE id=%s
        """
        success, msg = db.query(q_sel, [d['id']])
        if success and len(db.result) > 0:
            # Hay que asegurar que los campos tipo Date se pasen a string para evitar fallos si se exportan a JSON luego
            for row in db.result:
                if 'fecha_creacion' in row and row['fecha_creacion']:
                    row['fecha_creacion'] = str(row['fecha_creacion'])
            return {'ok': True, 'message': 'Datos recuperados con éxito.', 'data': db.result}
        return {'ok': False, 'message': 'Zona de servicio no encontrada.', 'data': []}

    def selectAsTuples(self, d):
        db = Db(getRowsAsDicts=False) # Para que devuelva una tupla en lugar de diccionario
        q_sel = """
        SELECT id, nombre, poblacion_afectada, fecha_creacion, responsable, activa, ST_AsText(geom) 
        FROM d.zonas_servicio WHERE id=%s
        """
        success, msg = db.query(q_sel, [d['id']])
        if success and len(db.result) > 0:
            return {'ok': True, 'message': 'Datos recuperados con éxito.', 'data': db.result}
        return {'ok': False, 'message': 'Zona de servicio no encontrada.', 'data': []}