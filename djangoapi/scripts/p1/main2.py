import sys
import ast
from zonas_servicio.zonasServicioOps import ZonasServicioOps

def main():
    # Comprobamos que nos pasen 3 parámetros: tabla, operacion, diccionario
    if len(sys.argv) == 4:
        tableName = sys.argv[1]
        functionName = sys.argv[2]
        
        # Convertimos el string que llega de Bash a un diccionario de Python
        try:
            d = ast.literal_eval(sys.argv[3])
        except Exception as e:
            print("Error: El formato del diccionario no es válido.")
            sys.exit(1)
            
        if tableName == "zonas_servicio" and functionName == "insert":
            ops = ZonasServicioOps()
            print(ops.insert(d))
            
    else:
        print("Uso: python main.py <tabla> <funcion> \"<diccionario>\"")

if __name__ == "__main__":
    main()