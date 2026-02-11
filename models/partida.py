# =============================================================================
# MODELO: PARTIDA
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Modelo que representa el estado completo de una partida en curso.
#    Mantiene información de jugador, nivel, respuestas, puntos, tiempo
#    y estadísticas en tiempo real.
#
# 📥 IMPORTADO EN:
#    - ui/Pygame/Estados/Gameplay.py - para gestionar estado de partida en UI gráfica
#    - ui/consola/juego_consola.py - para gestionar estado en UI de consola
#
# 🔗 DEPENDENCIAS:
#    - time: para calcular tiempo transcurrido de la partida
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Estructura centralizada del estado de la partida
#    - Separación entre modelo de datos y presentación (UI)
#    - Cálculo manual de estadísticas sin usar funciones built-in prohibidas
#    - Uso de time.time() para tracking temporal preciso
# =============================================================================

import time

# =============================================================================
# CREAR_PARTIDA_NUEVA
# =============================================================================
# Descripción: Inicializa una nueva partida con todos sus datos
# 
# Uso en Pygame: Se usa igual, el estado es independiente de la UI
#
# Parámetros:
#   - nombre_jugador (str): Nombre del jugador
#
# Retorna:
#   - dict: Diccionario con el estado inicial de la partida
#
# Ejemplo de uso:
#   partida = crear_partida_nueva("Juan")
# =============================================================================
def crear_partida_nueva(nombre_jugador: str) -> dict:
    """Inicializa una nueva partida."""
    partida = {}
    partida["jugador"] = nombre_jugador
    partida["nivel_actual"] = 1
    partida["respuestas"] = []
    partida["puntos_totales"] = 0
    partida["puntos_buffeo"] = 0
    partida["tiempo_inicio"] = time.time()
    partida["preguntas_usadas"] = []
    partida["errores_acumulados"] = 0
    partida["racha_actual"] = 0
    
    return partida


# =============================================================================
# ACTUALIZAR_PUNTOS_PARTIDA
# =============================================================================
# Descripción: Actualiza los puntos de una partida
# 
# Uso en Pygame: Se usa igual para actualizar el HUD de puntos
#
# Parámetros:
#   - partida (dict): Estado de la partida
#   - puntos_base (int): Puntos base obtenidos
#   - puntos_buffeo (int): Puntos de buffeo obtenidos
#
# Retorna:
#   - dict: Partida con puntos actualizados
#
# Ejemplo de uso:
#   partida = actualizar_puntos_partida(partida, 3, 2)
# =============================================================================
def actualizar_puntos_partida(partida: dict, puntos_base: int, puntos_buffeo: int) -> dict:
    """Actualiza los puntos de una partida."""
    partida["puntos_totales"] = partida["puntos_totales"] + puntos_base + puntos_buffeo
    partida["puntos_buffeo"] = partida["puntos_buffeo"] + puntos_buffeo
    return partida


# =============================================================================
# REGISTRAR_RESPUESTA_PARTIDA
# =============================================================================
# Descripción: Registra una respuesta en el historial de la partida
# 
# Uso en Pygame: Se usa igual para guardar el progreso
#
# Parámetros:
#   - partida (dict): Estado de la partida
#   - respuesta (dict): Datos de la respuesta dada
#
# Retorna:
#   - dict: Partida con respuesta registrada
#
# Ejemplo de uso:
#   partida = registrar_respuesta_partida(partida, respuesta_data)
# =============================================================================
def registrar_respuesta_partida(partida: dict, respuesta: dict) -> dict:
    """Registra una respuesta en el historial de la partida."""
    partida["respuestas"].append(respuesta)
    
    # Actualizar errores si la respuesta es incorrecta
    if not respuesta.get("es_correcta", False):
        partida["errores_acumulados"] = partida["errores_acumulados"] + 1
    
    return partida


# =============================================================================
# CALCULAR_TIEMPO_TRANSCURRIDO
# =============================================================================
# Descripción: Calcula el tiempo transcurrido desde el inicio de la partida
# 
# Uso en Pygame: Útil para mostrar timer en pantalla
#
# Parámetros:
#   - partida (dict): Estado de la partida
#
# Retorna:
#   - float: Segundos transcurridos desde el inicio
#
# Ejemplo de uso:
#   tiempo = calcular_tiempo_transcurrido(partida)
# =============================================================================
def calcular_tiempo_transcurrido(partida: dict) -> float:
    """Calcula el tiempo transcurrido desde el inicio de la partida."""
    tiempo_actual = time.time()
    tiempo_inicio = partida.get("tiempo_inicio", tiempo_actual)
    return round(tiempo_actual - tiempo_inicio, 2)


# =============================================================================
# OBTENER_ESTADISTICAS_PARTIDA
# =============================================================================
# Descripción: Obtiene estadísticas resumidas de la partida
# 
# Uso en Pygame: Útil para pantalla de resumen final
#
# Parámetros:
#   - partida (dict): Estado de la partida
#
# Retorna:
#   - dict: Estadísticas de la partida
#
# Ejemplo de uso:
#   stats = obtener_estadisticas_partida(partida)
# =============================================================================
def obtener_estadisticas_partida(partida: dict) -> dict:
    """Obtiene estadísticas resumidas de la partida."""
    total_preguntas = len(partida["respuestas"])
    respuestas_correctas = 0
    
    for respuesta in partida["respuestas"]:
        if respuesta.get("es_correcta", False):
            respuestas_correctas = respuestas_correctas + 1
    
    estadisticas = {
        "total_preguntas": total_preguntas,
        "respuestas_correctas": respuestas_correctas,
        "puntos_totales": partida["puntos_totales"],
        "puntos_buffeo": partida["puntos_buffeo"],
        "errores": partida["errores_acumulados"],
        "tiempo_total": calcular_tiempo_transcurrido(partida)
    }
    
    return estadisticas
