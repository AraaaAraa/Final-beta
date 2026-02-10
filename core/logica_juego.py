# =============================================================================
# LÓGICA PRINCIPAL DEL JUEGO
# =============================================================================
# Orquesta el flujo del juego sin dependencias de UI
# =============================================================================

from data.repositorio_preguntas import (
    cargar_preguntas_desde_csv,
    filtrar_preguntas_por_nivel,
    seleccionar_pregunta_aleatoria
)
from data.repositorio_usuarios import guardar_estadisticas_usuario
from core.logica_preguntas import (
    evaluar_respuesta,
    construir_resultado_respuesta,
    calcular_racha_actual,
    determinar_intentos_maximos,
    contar_errores_totales
)
from core.logica_buffeos import (
    calcular_puntos_buffeo,
    puede_usar_reintento,
    usar_raciones,
    usar_bolsa_monedas,
    verificar_merecimiento_objeto,
    verificar_objeto_equipado
)
from core.logica_puntaje import calcular_puntos_base
from config.constantes import (
    PREGUNTAS_POR_NIVEL,
    MAX_ERRORES_PERMITIDOS,
    RUTA_PREGUNTAS,
    RUTA_USUARIOS
)

# =============================================================================
# PROCESAR_PREGUNTA_COMPLETA
# =============================================================================
# Descripción: Procesa una pregunta completa con sus intentos
# 
# Uso en Pygame: Retorna datos del resultado, la UI decide cómo mostrarlo
#
# Parámetros:
#   - pregunta (dict): Pregunta a procesar
#   - nombre_usuario (str): Nombre del usuario
#   - racha_actual (int): Racha de respuestas correctas
#   - respuesta_usuario (str): Respuesta del usuario
#   - numero_intento (int): Número de intento actual
#   - max_intentos (int): Máximo de intentos permitidos
#
# Retorna:
#   - dict: Resultado de procesar la respuesta
#
# Ejemplo de uso:
#   resultado = procesar_pregunta_completa(pregunta, "Juan", 3, "A", 1, 2)
# =============================================================================
def procesar_pregunta_completa(pregunta: dict, nombre_usuario: str, racha_actual: int,
                              respuesta_usuario: str, numero_intento: int, 
                              max_intentos: int) -> dict:
    """Procesa una pregunta completa con lógica de intentos."""
    # Evaluar respuesta
    evaluacion = evaluar_respuesta(
        respuesta_usuario,
        pregunta["opciones"],
        pregunta["correcta"],
        nombre_usuario
    )
    
    if not evaluacion["valida"]:
        return construir_resultado_respuesta(evaluacion, pregunta["nivel"], 
                                            pregunta["correcta"], {}, False)
    
    # Calcular puntos base
    puntos_base = calcular_puntos_base(evaluacion["es_correcta"], pregunta["dificultad"])
    
    # Calcular buffeo si es correcta
    puntos_buffeo = 0
    if evaluacion["es_correcta"]:
        objeto = verificar_objeto_equipado(nombre_usuario)
        buffeo_data = calcular_puntos_buffeo(racha_actual, objeto)
        puntos_buffeo = buffeo_data["puntos"]
    
    # Usar objetos especiales
    puntos_raciones = 0
    puntos_bolsa = 0
    
    if not evaluacion["es_correcta"]:
        resultado_raciones = usar_raciones(nombre_usuario, evaluacion["es_correcta"])
        puntos_raciones = resultado_raciones["puntos_recuperados"]
    else:
        resultado_bolsa = usar_bolsa_monedas(nombre_usuario, evaluacion["es_correcta"], abs(puntos_base))
        puntos_bolsa = resultado_bolsa["puntos_extra"]
    
    # Construir puntos totales
    puntos = {
        "puntos": puntos_base + puntos_buffeo + puntos_raciones + puntos_bolsa,
        "puntos_base": puntos_base,
        "puntos_buffeo": puntos_buffeo,
        "puntos_raciones": puntos_raciones,
        "puntos_bolsa": puntos_bolsa
    }
    
    # Verificar si debe mostrar la respuesta correcta
    puede_reintentar = puede_usar_reintento(racha_actual, verificar_objeto_equipado(nombre_usuario))
    es_ultimo_intento = (numero_intento >= max_intentos - 1) and not puede_reintentar
    mostrar_correcta = es_ultimo_intento and not evaluacion["es_correcta"]
    
    resultado = construir_resultado_respuesta(
        evaluacion,
        pregunta["nivel"],
        pregunta["correcta"],
        puntos,
        mostrar_correcta
    )
    
    # Agregar información de reintento
    resultado["puede_reintentar"] = puede_reintentar and not evaluacion["es_correcta"]
    resultado["numero_intento"] = numero_intento
    resultado["max_intentos"] = max_intentos
    
    return resultado


# =============================================================================
# PROCESAR_NIVEL_COMPLETO
# =============================================================================
# Descripción: Procesa todas las preguntas de un nivel
# 
# Uso en Pygame: La UI llamará a esta función para cada nivel
#
# Parámetros:
#   - nivel (int): Número del nivel (1, 2, 3)
#   - preguntas (dict): Todas las preguntas disponibles
#   - preguntas_usadas (list): IDs de preguntas ya usadas
#   - nombre_usuario (str): Nombre del usuario
#   - respuestas_partida (list): Respuestas de la partida actual
#
# Retorna:
#   - dict: Resultado del nivel con estadísticas
#
# Ejemplo de uso:
#   resultado_nivel = procesar_nivel_completo(1, preguntas, [], "Juan", [])
# =============================================================================
def procesar_nivel_completo(nivel: int, preguntas: dict, preguntas_usadas: list,
                           nombre_usuario: str, respuestas_partida: list) -> dict:
    """Procesa todas las preguntas de un nivel."""
    cantidad = PREGUNTAS_POR_NIVEL[nivel]
    
    resultado_nivel = {
        "nivel": nivel,
        "preguntas_respondidas": [],
        "total_puntos": 0,
        "total_buffeo": 0,
        "correctas": 0,
        "tiempo_total": 0,
        "preguntas_usadas": []
    }
    
    return resultado_nivel


# =============================================================================
# OBTENER_PREGUNTA_PARA_NIVEL
# =============================================================================
# Descripción: Obtiene una pregunta disponible para un nivel
# 
# Uso en Pygame: La UI pedirá la siguiente pregunta
#
# Parámetros:
#   - preguntas (dict): Todas las preguntas
#   - nivel (int): Nivel actual
#   - preguntas_usadas (list): IDs ya usados
#
# Retorna:
#   - dict: Pregunta seleccionada o None si no hay disponibles
#
# Ejemplo de uso:
#   pregunta = obtener_pregunta_para_nivel(preguntas, 1, [])
# =============================================================================
def obtener_pregunta_para_nivel(preguntas: dict, nivel: int, preguntas_usadas: list) -> dict:
    """Obtiene una pregunta disponible para un nivel."""
    preguntas_disponibles = filtrar_preguntas_por_nivel(preguntas, nivel, preguntas_usadas)
    
    if not preguntas_disponibles:
        return None
    
    pregunta = seleccionar_pregunta_aleatoria(preguntas_disponibles)
    return pregunta


# =============================================================================
# CONSTRUIR_ESTADISTICAS_PARTIDA
# =============================================================================
# Descripción: Construye las estadísticas finales de una partida
# 
# Uso en Pygame: Se usa para guardar y mostrar resumen final
#
# Parámetros:
#   - respuestas (list): Todas las respuestas de la partida
#   - puntos_totales (int): Puntos totales obtenidos
#   - puntos_buffeo (int): Puntos de buffeo obtenidos
#   - tiempo_total (float): Tiempo total en segundos
#
# Retorna:
#   - dict: Estadísticas de la partida
#
# Ejemplo de uso:
#   stats = construir_estadisticas_partida(respuestas, 45, 10, 120.5)
# =============================================================================
def construir_estadisticas_partida(respuestas: list, puntos_totales: int,
                                   puntos_buffeo: int, tiempo_total: float) -> dict:
    """Construye las estadísticas finales de una partida."""
    total_preguntas = len(respuestas)
    respuestas_correctas = 0
    
    for respuesta in respuestas:
        if respuesta.get("es_correcta", False):
            respuestas_correctas = respuestas_correctas + 1
    
    estadisticas = {
        "puntos_totales": puntos_totales,
        "puntos_buffeo": puntos_buffeo,
        "respuestas_correctas": respuestas_correctas,
        "total_preguntas": total_preguntas,
        "tiempo_total_segundos": tiempo_total,
        "detalle": respuestas
    }
    
    return estadisticas


# =============================================================================
# VERIFICAR_CONDICION_FIN_PARTIDA
# =============================================================================
# Descripción: Verifica si la partida debe terminar
# 
# Uso en Pygame: Se usa después de cada respuesta
#
# Parámetros:
#   - respuestas (list): Respuestas de la partida
#
# Retorna:
#   - bool: True si debe terminar la partida
#
# Ejemplo de uso:
#   if verificar_condicion_fin_partida(respuestas):
#       # terminar partida
# =============================================================================
def verificar_condicion_fin_partida(respuestas: list) -> bool:
    """Verifica si la partida debe terminar."""
    errores = contar_errores_totales(respuestas)
    return errores >= MAX_ERRORES_PERMITIDOS


# =============================================================================
# PREPARAR_DATOS_PREGUNTA_PARA_UI
# =============================================================================
# Descripción: Prepara los datos de una pregunta para la UI
# 
# Uso en Pygame: Retorna todo lo necesario para mostrar la pregunta
#
# Parámetros:
#   - pregunta (dict): Pregunta a mostrar
#   - racha_actual (int): Racha de respuestas correctas
#   - numero_pregunta (int): Número de la pregunta actual
#   - total_preguntas (int): Total de preguntas del nivel
#
# Retorna:
#   - dict: Datos preparados para la UI
#
# Ejemplo de uso:
#   datos = preparar_datos_pregunta_para_ui(pregunta, 3, 1, 5)
# =============================================================================
def preparar_datos_pregunta_para_ui(pregunta: dict, racha_actual: int,
                                   numero_pregunta: int, total_preguntas: int) -> dict:
    """Prepara los datos de una pregunta para la UI."""
    datos = {
        "pregunta": pregunta,
        "nivel": pregunta.get("nivel", 1),
        "categoria": pregunta.get("categoria", ""),
        "descripcion": pregunta.get("descripcion", ""),
        "opciones": pregunta.get("opciones", []),
        "dificultad": pregunta.get("dificultad", 1),
        "racha_actual": racha_actual,
        "numero_pregunta": numero_pregunta,
        "total_preguntas": total_preguntas,
        "mostrar_racha": racha_actual > 0
    }
    
    return datos


# =============================================================================
# CALCULAR_DATOS_BUFFEO_PARA_UI
# =============================================================================
# Descripción: Calcula datos de buffeo para mostrar en la UI
# 
# Uso en Pygame: Retorna información para animaciones/mensajes
#
# Parámetros:
#   - racha_actual (int): Racha actual
#   - nombre_usuario (str): Nombre del usuario
#
# Retorna:
#   - dict: Datos del buffeo para mostrar
#
# Ejemplo de uso:
#   buffeo_ui = calcular_datos_buffeo_para_ui(5, "Juan")
# =============================================================================
def calcular_datos_buffeo_para_ui(racha_actual: int, nombre_usuario: str) -> dict:
    """Calcula datos de buffeo para mostrar en la UI."""
    objeto = verificar_objeto_equipado(nombre_usuario)
    buffeo_data = calcular_puntos_buffeo(racha_actual, objeto)
    
    datos_ui = {
        "tiene_buffeo": buffeo_data["puntos"] > 0,
        "puntos_totales": buffeo_data["puntos"],
        "puntos_racha": buffeo_data["por_racha"],
        "puntos_objeto": buffeo_data["por_objeto"],
        "racha": racha_actual,
        "objeto": objeto,
        "mensaje": ""
    }
    
    # Construir mensaje
    if buffeo_data["puntos"] > 0:
        if objeto == "espada":
            datos_ui["mensaje"] = f"⚔️ ¡ESPADA ACTIVADA! +2 puntos\n🔥 ¡BUFFEO TOTAL! +{buffeo_data['puntos']} puntos"
        else:
            datos_ui["mensaje"] = f"🔥 ¡BUFFEO ACTIVADO! +{buffeo_data['puntos']} puntos por racha de {racha_actual}"
    
    return datos_ui
