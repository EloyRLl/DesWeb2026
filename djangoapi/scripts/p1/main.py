import sys
import json
from zonas_servicio.zonasServicioOps import ZonasServicioOps
from tuberias.tuberiasOps import TuberiasOps
from arquetas_pozos.arquetasPozosOps import ArquetasPozosOps

def run_tests():
    # El diseño visual que solicitaste
    print("=" * 50)
    print("--- INICIANDO TEST DEL PROYECTO PRÁCTICO (4.9.2) ---")
    print("=" * 50)
    
    zonas_ops = ZonasServicioOps()
    tuberias_ops = TuberiasOps()
    arquetas_ops = ArquetasPozosOps()

    # 1. PRUEBA: ZONAS DE SERVICIO
    print("\n1. Insertando Zona de Servicio (Polígono)...")
    zona_data = {
        'nombre': 'Sector Norte Centro',
        'poblacion_afectada': 2500,
        'fecha_creacion': '2023-05-12',
        'responsable': 'Aguas y Saneamientos S.A.',
        'activa': True,
        'geom': 'POLYGON((0 0, 0 100, 100 100, 100 0, 0 0))'
    }
    print(zonas_ops.insert(zona_data))

    # 2. PRUEBA: TUBERÍAS
    print("\n2. Insertando Tubería (Línea)...")
    tuberia_data = {
        'tamano_tubo': 1001,
        'material': 'Fundición Dúctil',
        'presion_maxima': 16.5,
        'fecha_instalacion': '2023-06-01',
        'estado': 'Óptimo',
        'geom': 'LINESTRING(10 50, 50 10, 100 50)'
    }
    print(tuberias_ops.insert(tuberia_data))

    # 3. PRUEBA: ARQUETAS (DENTRO)
    print("\n3. Insertando Arqueta DENTRO de la Zona (Debería funcionar)...")
    arqueta_dentro = {
        'tipo_elemento': 'Pozo de Registro',
        'profundidad': 2.5,
        'fecha_mantenimiento': '2024-01-15',
        'accesible': True,
        'estado_conservacion': 'Limpio',
        'geom': 'POINT(50 50)' 
    }
    print(arquetas_ops.insert(arqueta_dentro))

    # 4. PRUEBA: ARQUETAS (FUERA)
    print("\n4. Insertando Arqueta FUERA de la Zona (Debería dar error topológico)...")
    arqueta_fuera = {
        'tipo_elemento': 'Arqueta de Válvula',
        'profundidad': 1.2,
        'fecha_mantenimiento': '2024-02-10',
        'accesible': False,
        'estado_conservacion': 'Tapa atascada',
        'geom': 'POINT(200 200)' 
    }
    print(arquetas_ops.insert(arqueta_fuera))

    print("\n" + "=" * 50)
    print("--- FIN DE LOS TESTS ---")
    print("=" * 50)

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        run_tests()
        return

    # Lógica para comandos individuales
    if len(sys.argv) >= 3:
        tableName = sys.argv[1]
        functionName = sys.argv[2]
        
        # Diccionarios de mapeo
        ops_map = {
            "zonas_servicio": ZonasServicioOps(),
            "tuberias": TuberiasOps(),
            "arquetas_pozos": ArquetasPozosOps()
        }
        
        if tableName in ops_map:
            target_ops = ops_map[tableName]
            if hasattr(target_ops, functionName):
                # Intentar leer JSON si existe el 4º argumento
                data = json.loads(sys.argv[3]) if len(sys.argv) == 4 else {}
                print(getattr(target_ops, functionName)(data))
            else:
                print(f"Error: {functionName} no existe.")
        else:
            print(f"Error: Tabla {tableName} no válida.")
    else:
        print("Uso: python main.py test")

if __name__ == "__main__":
    main()