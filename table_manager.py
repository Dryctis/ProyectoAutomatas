import json
from tkinter import filedialog
import sys

NOMBRE_ARCHIVO_DEFAULT = "tabla.json"
ESTADOS = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6']
ENTRADAS = ['+', 'E', '-', '*', '/', 'digito']

def obtener_tabla_default():
    print("Generando tabla de transiciones por defecto.")

    return {
        'q0': {'E': 'q2', '*': 'q3', '+': 'q1', '-': 'q1', 'digito': 'q4', '/': 'q3'},
        'q1': {'E': 'q2', '*': 'q3', '+': 'q1', '-': 'q1', 'digito': 'q4', '/': 'q3'},
        'q2': {'E': 'q2', '*': 'q3', '+': 'q1', '-': 'q1', 'digito': 'q6', '/': 'q3'},
        'q3': {'E': 'q2', '*': 'q3', '+': 'q1', '-': 'q1', 'digito': 'q4', '/': 'q3'},
        'q4': {'E': 'q5', '*': 'q3', '+': 'q1', '-': 'q1', 'digito': 'q4', '/': 'q3'},
        'q5': {'E': 'q2', '*': 'q3', '+': 'q1', '-': 'q1', 'digito': 'q6', '/': 'q3'},
        'q6': {'E': 'q2', '*': 'q3', '+': 'q1', '-': 'q1', 'digito': 'q6', '/': 'q3'}
    }

def cargar_tabla_default():
    try:
        with open(NOMBRE_ARCHIVO_DEFAULT, 'r') as f:
            tabla = json.load(f)
            print(f"Tabla cargada exitosamente desde '{NOMBRE_ARCHIVO_DEFAULT}'.")
            return tabla
    except FileNotFoundError:
        print(f"Advertencia: No se encontró '{NOMBRE_ARCHIVO_DEFAULT}'. Usando tabla por defecto.")
        return obtener_tabla_default()
    except json.JSONDecodeError:
        print(f"Error: El archivo '{NOMBRE_ARCHIVO_DEFAULT}' está corrupto. Usando tabla por defecto.")
        return obtener_tabla_default()

def guardar_tabla_default(tabla):
    try:
        with open(NOMBRE_ARCHIVO_DEFAULT, 'w') as f:
            json.dump(tabla, f, indent=4)
        print(f"Tabla guardada exitosamente en '{NOMBRE_ARCHIVO_DEFAULT}'.")
        return True
    except IOError as e:
        print(f"Error al guardar el archivo: {e}")
        return False

def importar_tabla():
    ruta_archivo = filedialog.askopenfilename(
        title="Importar Tabla",
        filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
    )
    
    if not ruta_archivo:
        return None

    try:
        with open(ruta_archivo, 'r') as f:
            tabla = json.load(f)
            if not isinstance(tabla, dict):
                print("Error: El JSON importado no es un diccionario (tabla).")
                return None
            print(f"Tabla importada desde '{ruta_archivo}'.")
            return tabla
    except Exception as e:
        print(f"Error al importar archivo: {e}")
        return None

def exportar_tabla(tabla):
    ruta_archivo = filedialog.asksaveasfilename(
        title="Exportar Tabla Como...",
        defaultextension=".json",
        filetypes=[("Archivos JSON", "*.json")]
    )
    
    if not ruta_archivo:
        return
        
    try:
        with open(ruta_archivo, 'w') as f:
            json.dump(tabla, f, indent=4)
        print(f"Tabla exportada exitosamente a '{ruta_archivo}'.")
    except Exception as e:
        print(f"Error al exportar archivo: {e}")