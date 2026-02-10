# =============================================================================
# REPOSITORIO DE USUARIOS
# =============================================================================
# Módulo para gestionar operaciones CRUD de usuarios
# =============================================================================

from data.archivos_json import cargar_json, guardar_json, verificar_archivo_existe
from models.usuario import crear_usuario_nuevo, actualizar_estadisticas_usuario
from utils.algoritmos import calcular_estadisticas_lista
from config.constantes import RUTA_USUARIOS

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
            
            # Verificar si existe "puntajes" y tiene elementos
            tiene_puntajes = False
            for clave in stats:
                if clave == "puntajes":
                    tiene_puntajes = True
                    break
            
            if tiene_puntajes and len(stats["puntajes"]) > 0:
                stats_puntajes = calcular_estadisticas_lista(stats["puntajes"])
                
                # Verificar si existe "porcentajes"
                tiene_porcentajes = False
                for clave in stats:
                    if clave == "porcentajes":
                        tiene_porcentajes = True
                        break
                
                if tiene_porcentajes:
                    stats_porcentajes = calcular_estadisticas_lista(stats["porcentajes"])
                else:
                    stats_porcentajes = {"mejor": 0, "promedio": 0}
                
                # Verificar si existe "intentos"
                intentos = 0
                for clave in stats:
                    if clave == "intentos":
                        intentos = stats["intentos"]
                        break
                
                ranking.append({
                    "nombre": nombre,
                    "mejor_puntaje": stats_puntajes["mejor"],
                    "promedio_puntaje": round(stats_puntajes["promedio"], 2),
                    "mejor_porcentaje": stats_porcentajes["mejor"],
                    "promedio_porcentaje": round(stats_porcentajes["promedio"], 1),
                    "intentos": intentos
                })
    
    return ordenar_ranking(ranking)


# =============================================================================
# ORDENAR_RANKING
# =============================================================================
# Descripción: Ordena el ranking por mejor puntaje (implementación manual)
# 
# Uso en Pygame: Se usa internamente para mostrar tabla ordenada
#
# Parámetros:
#   - ranking (list): Lista de usuarios sin ordenar
#
# Retorna:
#   - list: Lista ordenada por mejor puntaje (descendente)
#
# Ejemplo de uso:
#   ranking_ordenado = ordenar_ranking(ranking)
# =============================================================================
def ordenar_ranking(ranking: list) -> list:
    """Ordena el ranking por mejor puntaje."""
    ordenado = []
    for usuario in ranking:
        insertado = False
        nueva_lista_ordenada = []
        i = 0
        while i < len(ordenado):
            if not insertado and usuario["mejor_puntaje"] > ordenado[i]["mejor_puntaje"]:
                nueva_lista_ordenada.append(usuario)
                insertado = True
            nueva_lista_ordenada.append(ordenado[i])
            i = i + 1
        if not insertado:
            nueva_lista_ordenada.append(usuario)
        ordenado = nueva_lista_ordenada
    return ordenado
