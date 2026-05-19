-- initdb.sql

-- Crear el esquema si no existe
CREATE SCHEMA IF NOT EXISTS d;

-- 1. Tabla de Polígonos: Zonas de Servicio
CREATE TABLE IF NOT EXISTS d.zonas_servicio (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    poblacion_afectada INTEGER,
    fecha_creacion DATE,
    responsable VARCHAR(100),
    activa BOOLEAN,
    geom GEOMETRY(POLYGON, 25830)
);

-- 2. Tabla de Líneas: Tuberías
CREATE TABLE IF NOT EXISTS d.tuberias (
    id SERIAL PRIMARY KEY,
    tamano_tubo INTEGER,
    material VARCHAR(50),
    presion_maxima DOUBLE PRECISION,
    fecha_instalacion DATE,
    estado VARCHAR(50),
    geom GEOMETRY(LINESTRING, 25830)
);

-- 3. Tabla de Puntos: Arquetas y Pozos
CREATE TABLE IF NOT EXISTS d.arquetas_pozos (
    id SERIAL PRIMARY KEY,
    tipo_elemento VARCHAR(50),
    profundidad DOUBLE PRECISION,
    fecha_mantenimiento DATE,
    accesible BOOLEAN,
    estado_conservacion VARCHAR(50),
    geom GEOMETRY(POINT, 25830)
);