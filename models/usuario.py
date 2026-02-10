# =============================================================================
# MODELO: USUARIO
# =============================================================================
# Representa un usuario del juego con sus estadísticas
# =============================================================================

# =============================================================================
# CREAR_USUARIO_NUEVO
# =============================================================================
# Descripción: Inicializa un nuevo usuario con estadísticas en cero
# 
# Uso en Pygame: Se usa igual para crear perfiles de usuario
#
# Parámetros:
#   - nombre (str): Nombre del usuario
#
# Retorna:
#   - dict: Diccionario con estructura de usuario nuevo
#
# Ejemplo de uso:
#   usuario = crear_usuario_nuevo("Juan")
# =============================================================================
def crear_usuario_nuevo(nombre: str) -> dict:
    """Inicializa un nuevo usuario con estadísticas en cero."""
    usuario = {}
    usuario["nombre"] = nombre
    usuario["intentos"] = 0
    usuario["puntajes"] = []
    usuario["tiempos"] = []
    usuario["aciertos"] = []
    usuario["total_preguntas"] = []
    usuario["porcentajes"] = []
    usuario["historial"] = []
    
    return usuario


# =============================================================================
# ACTUALIZAR_ESTADISTICAS_USUARIO
# =============================================================================
# Descripción: Actualiza las estadísticas de un usuario después de una partida
# 
# Uso en Pygame: Se usa igual, solo cambia donde se muestran las stats
#
# Parámetros:
#   - usuario (dict): Datos del usuario
#   - puntos (int): Puntos obtenidos en la partida
#   - tiempo (float): Tiempo total de la partida
#   - aciertos (int): Cantidad de respuestas correctas
#   - total_preguntas (int): Total de preguntas respondidas
#   - historial (list): Detalle de respuestas de la partida
#
# Retorna:
#   - dict: Usuario con estadísticas actualizadas
#
# Ejemplo de uso:
#   usuario = actualizar_estadisticas_usuario(usuario, 45, 120.5, 8, 10, [...])
# =============================================================================
def actualizar_estadisticas_usuario(usuario: dict, puntos: int, tiempo: float, 
                                    aciertos: int, total_preguntas: int, 
                                    historial: list) -> dict:
    """Actualiza las estadísticas de un usuario después de una partida."""
    usuario["intentos"] = usuario["intentos"] + 1
    usuario["puntajes"].append(puntos)
    usuario["tiempos"].append(tiempo)
    usuario["aciertos"].append(aciertos)
    usuario["total_preguntas"].append(total_preguntas)
    
    porcentaje = 0
    if total_preguntas > 0:
        porcentaje = (aciertos / total_preguntas) * 100
    usuario["porcentajes"].append(round(porcentaje, 1))
    usuario["historial"].append(historial)
    
    return usuario


# =============================================================================
# OBTENER_MEJOR_PUNTAJE
# =============================================================================
# Descripción: Obtiene el mejor puntaje de un usuario
# 
# Uso en Pygame: Útil para mostrar achievements y records
#
# Parámetros:
#   - usuario (dict): Datos del usuario
#
# Retorna:
#   - int: Mejor puntaje del usuario (0 si no tiene partidas)
#
# Ejemplo de uso:
#   mejor = obtener_mejor_puntaje(usuario)
# =============================================================================
def obtener_mejor_puntaje(usuario: dict) -> int:
    """Obtiene el mejor puntaje de un usuario."""
    # Verificar si existe la clave "puntajes"
    tiene_puntajes = False
    for clave in usuario:
        if clave == "puntajes":
            tiene_puntajes = True
            break
    
    if not tiene_puntajes or len(usuario["puntajes"]) == 0:
        return 0
    
    mejor = usuario["puntajes"][0]
    i = 1
    while i < len(usuario["puntajes"]):
        if usuario["puntajes"][i] > mejor:
            mejor = usuario["puntajes"][i]
        i = i + 1
    
    return mejor
