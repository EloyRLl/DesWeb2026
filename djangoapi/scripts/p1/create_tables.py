from myLib.db import Db

def setup_db():
    db = Db()
    sql = """
    CREATE SCHEMA IF NOT EXISTS d;

    CREATE TABLE IF NOT EXISTS d.zonas_servicio (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100),
        poblacion_afectada INTEGER,
        fecha_creacion DATE,
        responsable VARCHAR(100),
        activa BOOLEAN,
        geom GEOMETRY(POLYGON, 25830)
    );

    CREATE TABLE IF NOT EXISTS d.tuberias (
        id SERIAL PRIMARY KEY,
        tamano_tubo INTEGER,
        material VARCHAR(50),
        presion_maxima DOUBLE PRECISION,
        fecha_instalacion DATE,
        estado VARCHAR(50),
        geom GEOMETRY(LINESTRING, 25830)
    );

    CREATE TABLE IF NOT EXISTS d.arquetas_pozos (
        id SERIAL PRIMARY KEY,
        tipo_elemento VARCHAR(50),
        profundidad DOUBLE PRECISION,
        fecha_mantenimiento DATE,
        accesible BOOLEAN,
        estado_conservacion VARCHAR(50),
        geom GEOMETRY(POINT, 25830)
    );
    """
    success, msg = db.query(sql)
    if success:
        print("✅ ¡Tablas creadas correctamente en PostGIS!")
    else:
        print("❌ Error al crear las tablas:", msg)

if __name__ == "__main__":
    setup_db()
