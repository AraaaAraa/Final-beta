# =============================================================================
# MODELO: USUARIO
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Modelo de datos que representa un usuario/jugador del juego.
#    Gestiona estadísticas acumuladas, historial de partidas y mejores puntajes.
#
# 📥 IMPORTADO EN:
#    - data/repositorio_usuarios.py (línea ~8) - para crear_usuario_nuevo, actualizar_estadisticas_usuario
#    - data/repositorio_usuarios.py (línea ~50) - para obtener_mejor_puntaje
#
# 🔗 DEPENDENCIAS:
#    Ninguna (modelo de datos puro)
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Estructura de usuario con estadísticas detalladas por partida
#    - Actualización manual de estadísticas sin usar funciones built-in
#    - Búsqueda del mejor puntaje con algoritmo manual (bucle while)
#    - Verificación de claves sin usar .get() para cumplir principios
# =============================================================================

# =============================================================================
# CREAR_USUARIO_NUEVO
# =============================================================================
# 📄 Descripción: 
#    Inicializa un nuevo usuario con estadísticas en cero
# 
# 📥 Parámetros:
#    - nombre (str): Nombre del usuario
#
# 📤 Retorna:
#    - dict: Diccionario con estructura de usuario nuevo
#
# 🔧 Importado en:
#    - data/repositorio_usuarios.py (línea ~25) - para crear nuevos usuarios
#
# 💡 Algoritmo:
#    - Paso 1: Crear diccionario vacío
#    - Paso 2: Asignar nombre y campos de estadísticas como listas vacías
#    - Paso 3: Retornar usuario inicializado (un solo return)
#
# 📝 Ejemplo de uso:
#    usuario = crear_usuario_nuevo("Juan")
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
# 📄 Descripción: 
#    Actualiza las estadísticas de un usuario después de una partida
# 
# 📥 Parámetros:
#    - usuario (dict): Datos del usuario
#    - puntos (int): Puntos obtenidos en la partida
#    - tiempo (float): Tiempo total de la partida
#    - aciertos (int): Cantidad de respuestas correctas
#    - total_preguntas (int): Total de preguntas respondidas
#    - historial (list): Detalle de respuestas de la partida
#
# 📤 Retorna:
#    - dict: Usuario con estadísticas actualizadas
#
# 🔧 Importado en:
#    - data/repositorio_usuarios.py (línea ~45) - para guardar estadísticas de partida
#
# 💡 Algoritmo:
#    - Paso 1: Incrementar contador de intentos manualmente
#    - Paso 2: Agregar puntos, tiempo, aciertos a listas usando append
#    - Paso 3: Calcular porcentaje manualmente (sin usar funciones built-in)
#    - Paso 4: Agregar historial completo
#    - Paso 5: Retornar usuario actualizado (un solo return)
#
# 📝 Ejemplo de uso:
#    usuario = actualizar_estadisticas_usuario(usuario, 45, 120.5, 8, 10, [...])
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
# 📄 Descripción: 
#    Obtiene el mejor puntaje de un usuario usando algoritmo manual
# 
# 📥 Parámetros:
#    - usuario (dict): Datos del usuario
#
# 📤 Retorna:
#    - int: Mejor puntaje del usuario (0 si no tiene partidas)
#
# 🔧 Importado en:
#    - data/repositorio_usuarios.py (línea ~90) - para obtener récord del usuario
#    - ui/Pygame/Estados/Game_Over.py - para mostrar mejor puntaje en pantalla
#
# 💡 Algoritmo:
#    - Paso 1: Buscar manualmente si existe clave "puntajes" (sin .get())
#    - Paso 2: Si no hay puntajes, retornar 0
#    - Paso 3: Inicializar mejor con primer elemento
#    - Paso 4: Recorrer con bucle while comparando cada puntaje
#    - Paso 5: Retornar el mejor encontrado (un solo return)
#
# 📝 Ejemplo de uso:
#    mejor = obtener_mejor_puntaje(usuario)
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
