# =============================================================================
# ARCHIVOS JSON - OPERACIONES GENÉRICAS
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Módulo de utilidades para operaciones de lectura/escritura de archivos JSON.
#    Proporciona funciones genéricas para cargar, guardar y verificar archivos.
#
# 📥 IMPORTADO EN:
#    - data/repositorio_usuarios.py (línea 7) - para cargar_json, guardar_json, verificar_archivo_existe
#    - data/repositorio_preguntas.py (línea 8) - para verificar_y_obtener_ruta
#    - core/logica_buffeos.py - para cargar/guardar estado de buffs
#
# 🔗 DEPENDENCIAS:
#    - os: para operaciones de archivos y directorios
#    - json: para serialización/deserialización de datos
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Centraliza operaciones de I/O para reducir código duplicado
#    - Manejo robusto de errores con try/except
#    - Creación automática de directorios si no existen
#    - Encoding UTF-8 para soportar caracteres especiales
#    - Separación de responsabilidades: este módulo solo maneja archivos
# =============================================================================

import os
import json

# =============================================================================
# VERIFICAR_ARCHIVO_EXISTE
# =============================================================================
# 📄 Descripción: 
#    Verifica si un archivo existe en el sistema de archivos
# 
# 📥 Parámetros:
#    - archivo (str): Ruta del archivo a verificar
#    - mensaje_error (str, opcional): Mensaje a mostrar si no existe
#
# 📤 Retorna:
#    - bool: True si el archivo existe, False en caso contrario
#
# 🔧 Importado en:
#    - data/repositorio_usuarios.py (línea 33) - para validar archivo de usuarios
#    - data/archivos_json.py (línea 121) - para verificar_y_obtener_ruta
#
# 💡 Algoritmo:
#    - Paso 1: Usar os.path.exists para verificar existencia
#    - Paso 2: Si no existe y hay mensaje_error, imprimirlo
#    - Paso 3: Retornar resultado booleano (un solo return)
#
# 📝 Ejemplo de uso:
#    if verificar_archivo_existe("datos.json", "Archivo no encontrado"):
#        # cargar datos
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
# 📄 Descripción: 
#    Carga datos desde un archivo JSON con manejo de errores
# 
# 📥 Parámetros:
#    - archivo (str): Ruta del archivo JSON
#    - default: Valor por defecto si el archivo no existe o hay error
#
# 📤 Retorna:
#    - dict/list: Datos cargados o valor por defecto
#
# 🔧 Importado en:
#    - data/repositorio_usuarios.py (líneas 36, 75, 181) - para cargar usuarios
#    - core/logica_buffeos.py - para cargar estado de buffs
#
# 💡 Algoritmo:
#    - Paso 1: Abrir archivo con encoding UTF-8
#    - Paso 2: Usar json.load para deserializar
#    - Paso 3: En caso de error, retornar default (un solo return con try/except)
#
# 📝 Ejemplo de uso:
#    datos = cargar_json("usuarios.json", {})
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
# 📄 Descripción: 
#    Guarda datos en un archivo JSON con formato legible
# 
# 📥 Parámetros:
#    - archivo (str): Ruta del archivo JSON
#    - datos: Datos a guardar (dict o list)
#
# 📤 Retorna:
#    - bool: True si se guardó correctamente, False en caso de error
#
# 🔧 Importado en:
#    - data/repositorio_usuarios.py (línea 80) - para guardar estadísticas
#    - core/logica_buffeos.py - para guardar estado de buffs
#
# 💡 Algoritmo:
#    - Paso 1: Crear directorio padre si no existe (os.makedirs)
#    - Paso 2: Abrir archivo con encoding UTF-8
#    - Paso 3: Usar json.dump con indent=2 para formato legible
#    - Paso 4: Retornar True si éxito, False si hay excepción (un solo return)
#
# 📝 Ejemplo de uso:
#    guardar_json("usuarios.json", datos_usuarios)
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
