# =============================================================================
# REPOSITORIO DE USUARIOS
# =============================================================================
# Módulo para gestionar operaciones CRUD de usuarios
# =============================================================================

from data.archivos_json import cargar_json, guardar_json, verificar_archivo_existe
from models.usuario import crear_usuario_nuevo, actualizar_estadisticas_usuario
from utils.algoritmos import calcular_estadisticas_lista
from config.constantes import RUTA_USUARIOS, RUTA_ESTADO_BUFF

# =============================================================================
# OBTENER_USUARIO
# =============================================================================
# Descripción: Obtiene los datos de un usuario desde el archivo
# 
# Uso en Pygame: Se usa igual para cargar perfil de usuario
#
# Parámetros:
#   - nombre_usuario (str): Nombre del usuario
#   - archivo (str): Ruta del archivo de usuarios
#
# Retorna:
#   - dict: Datos del usuario o dict con "error" si no existe
#
# Ejemplo de uso:
#   usuario = obtener_usuario("Juan", "usuarios.json")
# =============================================================================
def obtener_usuario(nombre_usuario: str, archivo: str) -> dict:
    """Obtiene los datos de un usuario desde el archivo."""
    resultado = {"error": ""}
    
    if verificar_archivo_existe(archivo, "No hay estadísticas guardadas") == False:
        resultado["error"] = "No hay estadísticas guardadas"
    else:
        datos = cargar_json(archivo)
        if not datos:
            resultado["error"] = "Error al cargar estadísticas"
        else:
            # Buscar el usuario iterando por las claves del diccionario
            usuario_encontrado = False
            for clave in datos:
                if clave == nombre_usuario:
                    usuario_encontrado = True
                    break
            
            if not usuario_encontrado:
                resultado["error"] = "Usuario '" + nombre_usuario + "' no encontrado"
            else:
                resultado = datos[nombre_usuario]
    
    return resultado


# =============================================================================
# GUARDAR_ESTADISTICAS_USUARIO
# =============================================================================
# Descripción: Guarda las estadísticas de una partida para un usuario
# 
# Uso en Pygame: Se usa igual después de cada partida
#
# Parámetros:
#   - nombre_usuario (str): Nombre del usuario
#   - resultado (dict): Resultado de la partida
#   - archivo_usuarios (str): Ruta del archivo de usuarios
#
# Retorna:
#   - None
#
# Ejemplo de uso:
#   guardar_estadisticas_usuario("Juan", resultado_partida, "usuarios.json")
# =============================================================================
def guardar_estadisticas_usuario(nombre_usuario: str, resultado: dict, archivo_usuarios: str) -> None:
    """Guarda las estadísticas de una partida para un usuario."""
    datos = cargar_json(archivo_usuarios, {})
    datos = inicializar_datos_usuario(nombre_usuario, datos)
    usuario = datos[nombre_usuario]
    usuario = actualizar_listas_estadisticas(usuario, resultado)
    datos[nombre_usuario] = usuario
    guardar_json(archivo_usuarios, datos)
    return None


# =============================================================================
# INICIALIZAR_DATOS_USUARIO
# =============================================================================
# Descripción: Inicializa un usuario nuevo si no existe en los datos
# 
# Uso en Pygame: Se usa automáticamente al guardar estadísticas
#
# Parámetros:
#   - nombre (str): Nombre del usuario
#   - datos (dict): Diccionario de todos los usuarios
#
# Retorna:
#   - dict: Datos actualizados con el usuario inicializado
#
# Ejemplo de uso:
#   datos = inicializar_datos_usuario("Juan", datos)
# =============================================================================
def inicializar_datos_usuario(nombre: str, datos: dict) -> dict:
    """Inicializa un usuario nuevo si no existe en los datos."""
    resultado = None
    usuario_encontrado = False
    
    # Buscar el nombre de usuario iterando por las claves del diccionario
    for clave in datos:
        if clave == nombre:
            usuario_encontrado = True
            break
    
    if usuario_encontrado:
        resultado = datos
    else:
        datos[nombre] = {
            "intentos": 0,
            "puntajes": [],
            "tiempos": [],
            "aciertos": [],
            "total_preguntas": [],
            "porcentajes": [],
            "historial": []
        }
        resultado = datos
    
    return resultado


# =============================================================================
# ACTUALIZAR_LISTAS_ESTADISTICAS
# =============================================================================
# Descripción: Actualiza las listas de estadísticas de un usuario
# 
# Uso en Pygame: Se usa internamente al guardar estadísticas
#
# Parámetros:
#   - usuario (dict): Datos del usuario
#   - resultado (dict): Resultado de la partida
#
# Retorna:
#   - dict: Usuario con estadísticas actualizadas
#
# Ejemplo de uso:
#   usuario = actualizar_listas_estadisticas(usuario, resultado)
# =============================================================================
def actualizar_listas_estadisticas(usuario: dict, resultado: dict) -> dict:
    """Actualiza las listas de estadísticas de un usuario."""
    usuario["intentos"] = usuario["intentos"] + 1
    usuario["puntajes"].append(resultado["puntos_totales"])
    usuario["tiempos"].append(resultado["tiempo_total_segundos"])
    usuario["aciertos"].append(resultado["respuestas_correctas"])
    usuario["total_preguntas"].append(resultado["total_preguntas"])
    
    porcentaje = 0
    if resultado["total_preguntas"] > 0:
        porcentaje = (resultado["respuestas_correctas"] / resultado["total_preguntas"]) * 100
    usuario["porcentajes"].append(round(porcentaje, 1))
    usuario["historial"].append(resultado["detalle"])

    return usuario


# =============================================================================
# OBTENER_RANKING
# =============================================================================
# Descripción: Obtiene el ranking de todos los jugadores
# 
# Uso en Pygame: Se usa para mostrar tabla de posiciones
#
# Parámetros:
#   - archivo (str): Ruta del archivo de usuarios
#
# Retorna:
#   - list: Lista de usuarios ordenados por mejor puntaje
#
# Ejemplo de uso:
#   ranking = obtener_ranking("usuarios.json")
# =============================================================================
def obtener_ranking(archivo: str) -> list:
    """Obtiene el ranking de todos los jugadores."""
    datos = cargar_json(archivo)
    ranking = []
    
    if datos:
        for nombre in datos:
            stats = datos[nombre]
            
            # Verificar con 'in' en lugar de iterar
            if "puntajes" in stats and len(stats["puntajes"]) > 0:
                stats_puntajes = calcular_estadisticas_lista(stats["puntajes"])
                
                # Usar .get() con valores por defecto
                if "porcentajes" in stats:
                    stats_porcentajes = calcular_estadisticas_lista(stats["porcentajes"])
                else:
                    stats_porcentajes = {"mejor": 0, "promedio": 0}
                
                intentos = stats.get("intentos", 0)
                
                ranking.append({
                    "nombre": nombre,
                    "mejor_puntaje": stats_puntajes["mejor"],
                    "promedio_puntaje": round(stats_puntajes["promedio"], 2),
                    "mejor_porcentaje": stats_porcentajes["mejor"],
                    "promedio_porcentaje": round(stats_porcentajes["promedio"], 1),
                    "intentos": intentos
                })
    
    return ordenar_ranking(ranking)


def ordenar_ranking(ranking: list) -> list:
    """Ordena el ranking por mejor puntaje usando insertion sort optimizado."""
    if len(ranking) <= 1:
        return ranking
    
    # Insertion sort in-place - mucho más eficiente
    for i in range(1, len(ranking)):
        usuario_actual = ranking[i]
        j = i - 1
        
        # Mover elementos menores una posición adelante
        while j >= 0 and ranking[j]["mejor_puntaje"] < usuario_actual["mejor_puntaje"]:
            ranking[j + 1] = ranking[j]
            j -= 1
        
        # Insertar el usuario en su posición correcta
        ranking[j + 1] = usuario_actual
    
    return ranking

# =============================================================================
# FUNCIONES PARA VIDAS EXTRA
# =============================================================================

def obtener_vidas_extra(nombre_usuario: str, ruta_archivo: str = RUTA_ESTADO_BUFF) -> int:
    """
    Obtiene las vidas extra del usuario desde EstadoBuff.json.
    
    Parámetros:
        nombre_usuario (str): Nombre del usuario
        ruta_archivo (str): Ruta del archivo EstadoBuff.json
    
    Retorna:
        int: Número de vidas extra disponibles
    """
    import json
    from pathlib import Path
    
    ruta = Path(ruta_archivo)
    
    if not ruta.exists():
        return 0
    
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            
            if nombre_usuario in datos:
                usuario_data = datos[nombre_usuario]
                return usuario_data.get("vidas_extra", 0)
            
            return 0
    except:
        return 0


def guardar_vidas_extra(nombre_usuario: str, vidas_extra: int, ruta_archivo: str = RUTA_ESTADO_BUFF):
    """
    Guarda las vidas extra del usuario en EstadoBuff.json.
    
    Parámetros:
        nombre_usuario (str): Nombre del usuario
        vidas_extra (int): Número de vidas extra a guardar
        ruta_archivo (str): Ruta del archivo EstadoBuff.json
    """
    import json
    from pathlib import Path
    
    ruta = Path(ruta_archivo)
    
    # Cargar datos existentes
    if ruta.exists():
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
        except:
            datos = {}
    else:
        datos = {}
    
    # Crear entrada del usuario si no existe
    if nombre_usuario not in datos:
        datos[nombre_usuario] = {}
    
    # Actualizar vidas extra
    datos[nombre_usuario]["vidas_extra"] = vidas_extra
    
    # Guardar
    with open(ruta, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)
    
    print(f"💾 Vidas extra guardadas para {nombre_usuario}: {vidas_extra}")