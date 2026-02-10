# =============================================================================
# ARCHIVOS JSON - OPERACIONES GENÉRICAS
# =============================================================================
# Módulo para operaciones de lectura/escritura de archivos JSON
# =============================================================================

import os
import json

# =============================================================================
# VERIFICAR_ARCHIVO_EXISTE
# =============================================================================
# Descripción: Verifica si un archivo existe en el sistema
# 
# Uso en Pygame: Se usa igual para validar archivos de datos
#
# Parámetros:
#   - archivo (str): Ruta del archivo a verificar
#   - mensaje_error (str): Mensaje a mostrar si no existe (vacío para no mostrar)
#
# Retorna:
#   - bool: True si el archivo existe, False en caso contrario
#
# Ejemplo de uso:
#   if verificar_archivo_existe("datos.json", ""):
#       # cargar datos
# =============================================================================
def verificar_archivo_existe(archivo: str, mensaje_error: str = "") -> bool:
    """Verifica si un archivo existe en el sistema."""
    if not os.path.exists(archivo):
        if mensaje_error:
            print(f"{mensaje_error}")
        return False
    return True


# =============================================================================
# CARGAR_JSON
# =============================================================================
# Descripción: Carga datos desde un archivo JSON
# 
# Uso en Pygame: Se usa igual para cargar datos guardados
#
# Parámetros:
#   - archivo (str): Ruta del archivo JSON
#   - default: Valor por defecto si el archivo no existe o hay error
#
# Retorna:
#   - dict/list: Datos cargados o valor por defecto
#
# Ejemplo de uso:
#   datos = cargar_json("usuarios.json", {})
# =============================================================================
def cargar_json(archivo: str, default=None):
    """Carga datos desde un archivo JSON."""
    if default is None:
        default = {}
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default


# =============================================================================
# GUARDAR_JSON
# =============================================================================
# Descripción: Guarda datos en un archivo JSON
# 
# Uso en Pygame: Se usa igual para persistir datos
#
# Parámetros:
#   - archivo (str): Ruta del archivo JSON
#   - datos: Datos a guardar (dict o list)
#
# Retorna:
#   - bool: True si se guardó correctamente
#
# Ejemplo de uso:
#   guardar_json("usuarios.json", datos_usuarios)
# =============================================================================
def guardar_json(archivo: str, datos) -> bool:
    """Guarda datos en un archivo JSON."""
    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error al guardar JSON: {e}")
        return False


# =============================================================================
# VERIFICAR_Y_OBTENER_RUTA
# =============================================================================
# Descripción: Verifica que un archivo existe y retorna su ruta absoluta
# 
# Uso en Pygame: Útil para validar recursos del juego
#
# Parámetros:
#   - path (str): Ruta relativa del archivo
#   - base_dir (str): Directorio base (opcional)
#
# Retorna:
#   - str: Ruta absoluta si existe, cadena vacía si no existe
#
# Ejemplo de uso:
#   ruta = verificar_y_obtener_ruta("preguntas.csv")
# =============================================================================
def verificar_y_obtener_ruta(path: str, base_dir: str = None) -> str:
    """Verifica que un archivo existe y retorna su ruta absoluta."""
    if base_dir is None:
        base_dir = os.path.dirname(__file__)
    
    abs_path = os.path.join(base_dir, path)
    if verificar_archivo_existe(abs_path, f"No se encontró el archivo: {abs_path}"):
        return abs_path
    return ""
