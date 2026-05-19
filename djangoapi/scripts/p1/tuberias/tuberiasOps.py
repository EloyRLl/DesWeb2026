# djangoapi/scripts/p1/tuberias/tuberiasOps.py
from myLib.db import Db
from myLib import p1Settings as settings

class TuberiasOps:
    
    def insert(self, d):
        db = Db(getRowsAsDicts=True)
        geom = d['geom']
        
        # 1. Validar la geometría tras el redondeo
        q_val = "SELECT ST_IsValid(ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)) as is_valid"
        db.query(q_val, [geom, settings.EPSG_CODE, settings.SNAP_DISTANCE])
        if not db.result[0]['is_valid']:
            return {'ok': False, 'message': 'La geometría de la tubería no es válida.', 'data': []}
            
        # 2. Insertar
        q_ins = """
        INSERT INTO d.tuberias (tamano_tubo, material, presion_maxima, fecha_instalacion, estado, geom)
        VALUES (%s, %s, %s, %s, %s, ST_SnapToGrid(ST_GeomFromText(%s, %s), %s))
        RETURNING id
        """
        success, msg = db.query(q_ins, [
            d['tamano_tubo'], d['material'], d['presion_maxima'], 
            d['fecha_instalacion'], d['estado'], 
            geom, settings.EPSG_CODE, settings.SNAP_DISTANCE
        ])
        
        if success and db.result:
            return {'ok': True, 'message': 'Tubería insertada.', 'data': [{'id': db.result[0]['id']}]}
        return {'ok': False, 'message': f'Error: {msg}', 'data': []}

    def update(self, d):
        db = Db(getRowsAsDicts=True)
        id_val = d['id']
        geom = d['geom']
        
        q_val = "SELECT ST_IsValid(ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)) as is_valid"
        db.query(q_val, [geom, settings.EPSG_CODE, settings.SNAP_DISTANCE])
        if not db.result[0]['is_valid']:
            return {'ok': False, 'message': 'La nueva geometría no es válida.', 'data': []}
            
        q_upd = """
        UPDATE d.tuberias
        SET tamano_tubo=%s, material=%s, presion_maxima=%s, fecha_instalacion=%s, estado=%s, 
            geom=ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)
        WHERE id=%s
        """
        success, msg = db.query(q_upd, [
            d['tamano_tubo'], d['material'], d['presion_maxima'], 
            d['fecha_instalacion'], d['estado'], 
            geom, settings.EPSG_CODE, settings.SNAP_DISTANCE, id_val
        ])
        if success:
            return {'ok': True, 'message': 'Tubería actualizada.', 'data': [{'rows_updated': db.result}]}
        return {'ok': False, 'message': f'Error: {msg}', 'data': []}

    def delete(self, d):
        db = Db()
        success, msg = db.query("DELETE FROM d.tuberias WHERE id=%s", [d['id']])
        if success:
            return {'ok': True, 'message': 'Tubería borrada.', 'data': [{'rows_deleted': db.result}]}
        return {'ok': False, 'message': f'Error al borrar: {msg}', 'data': []}

    def selectAsDicts(self, d):
        db = Db(getRowsAsDicts=True)
        q_sel = "SELECT id, tamano_tubo, material, presion_maxima, fecha_instalacion, estado, ST_AsText(geom) as geom FROM d.tuberias WHERE id=%s"
        success, msg = db.query(q_sel, [d['id']])
        if success and db.result:
            for row in db.result:
                if 'fecha_instalacion' in row and row['fecha_instalacion']:
                    row['fecha_instalacion'] = str(row['fecha_instalacion'])
            return {'ok': True, 'message': 'OK', 'data': db.result}
        return {'ok': False, 'message': 'No encontrada.', 'data': []}

    def selectAsTuples(self, d):
        db = Db(getRowsAsDicts=False)
        q_sel = "SELECT id, tamano_tubo, material, presion_maxima, fecha_instalacion, estado, ST_AsText(geom) FROM d.tuberias WHERE id=%s"
        success, msg = db.query(q_sel, [d['id']])
        if success and db.result:
            return {'ok': True, 'message': 'OK', 'data': db.result}
        return {'ok': False, 'message': 'No encontrada.', 'data': []}