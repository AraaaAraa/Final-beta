# =============================================================================
# LÓGICA DE BUFFEOS Y OBJETOS ESPECIALES
# =============================================================================
# Maneja todo el sistema de buffeos y objetos especiales sin UI
# =============================================================================

from data.archivos_json import cargar_json, guardar_json
from config.constantes import (
    RUTA_ESTADO_BUFF, 
    PUNTOS_BUFFEO_POR_RACHA,
    OBJETOS_ESPECIALES,
    RESPUESTAS_CORRECTAS_PARA_OBJETO,
    TOTAL_PREGUNTAS_PARA_OBJETO
)

# =============================================================================
# CALCULAR_PUNTOS_BUFFEO
# =============================================================================
# Descripción: Calcula los puntos extra por racha y objeto equipado
# 
# Uso en Pygame: Esta función se usa igual, solo cambia dónde se muestran
#                los puntos calculados
#
# Parámetros:
#   - racha_actual (int): Número de respuestas correctas consecutivas
#   - objeto (str): Nombre del objeto especial equipado (o None)
#
# Retorna:
#   - dict: {"puntos": int, "por_racha": int, "por_objeto": int, "racha": int, "objeto": str}
#
# Ejemplo de uso:
#   buffeo = calcular_puntos_buffeo(8, "espada")
# =============================================================================
def calcular_puntos_buffeo(racha_actual: int, objeto: str) -> dict:
    """Calcula puntos de buffeo sin mostrar nada."""
    puntos_racha = 0
    
    # Calcular puntos por racha usando las constantes
    if racha_actual > 7:
        puntos_racha = PUNTOS_BUFFEO_POR_RACHA[7]
    elif racha_actual > 5:
        puntos_racha = PUNTOS_BUFFEO_POR_RACHA[5]
    elif racha_actual > 3:
        puntos_racha = PUNTOS_BUFFEO_POR_RACHA[3]
    
    puntos_objeto = 0
    if objeto == "espada":
        puntos_objeto = OBJETOS_ESPECIALES["espada"]["puntos_extra"]
    
    resultado = {
        "puntos": puntos_racha + puntos_objeto,
        "por_racha": puntos_racha,
        "por_objeto": puntos_objeto,
        "racha": racha_actual,
        "objeto": objeto
    }
    
    return resultado


# =============================================================================
# PUEDE_USAR_REINTENTO
# =============================================================================
# Descripción: Verifica si el jugador puede usar un reintento
# 
# Uso en Pygame: Se usa igual para habilitar botón de reintento
#
# Parámetros:
#   - racha_actual (int): Racha de respuestas correctas
#   - objeto (str): Objeto especial equipado (o None)
#
# Retorna:
#   - bool: True si puede reintentar, False en caso contrario
#
# Ejemplo de uso:
#   if puede_usar_reintento(5, "espada"):
#       # mostrar opción de reintento
# =============================================================================
def puede_usar_reintento(racha_actual: int, objeto: str) -> bool:
    """Verifica si el jugador puede usar un reintento."""
    # Puede reintentar si tiene racha > 1 o tiene espada
    if racha_actual > 1 or objeto == "espada":
        return True
    return False


# =============================================================================
# OBTENER_DATOS_REINTENTO
# =============================================================================
# Descripción: Obtiene información sobre el reintento disponible
# 
# Uso en Pygame: Útil para mostrar tooltip o mensaje de reintento
#
# Parámetros:
#   - racha (int): Racha actual
#   - objeto (str): Objeto equipado
#
# Retorna:
#   - dict: Información del reintento o None si no hay
#
# Ejemplo de uso:
#   info = obtener_datos_reintento(5, None)
# =============================================================================
def obtener_datos_reintento(racha: int, objeto: str) -> dict:
    """Obtiene información sobre el reintento disponible."""
    if not puede_usar_reintento(racha, objeto):
        return None
    
    resultado = {
        "disponible": True,
        "por_racha": racha > 1,
        "por_objeto": objeto == "espada",
        "racha": racha,
        "objeto": objeto
    }
    
    return resultado


# =============================================================================
# VERIFICAR_OBJETO_EQUIPADO
# =============================================================================
# Descripción: Verifica qué objeto especial tiene equipado un usuario
# 
# Uso en Pygame: Se usa para mostrar iconos de objetos en HUD
#
# Parámetros:
#   - nombre_usuario (str): Nombre del usuario
#   - estado_path (str): Ruta al archivo de estado de buffs
#
# Retorna:
#   - str: Tipo de objeto o None si no tiene ninguno
#
# Ejemplo de uso:
#   objeto = verificar_objeto_equipado("Juan", ruta_estado)
# =============================================================================
def verificar_objeto_equipado(nombre_usuario: str, estado_path: str = None) -> str:
    """Verifica qué objeto especial tiene equipado un usuario."""
    if estado_path is None:
        estado_path = RUTA_ESTADO_BUFF
    
    resultado = None
    
    try:
        estado = cargar_json(estado_path, {})
        
        # Verificar si el usuario existe en el estado
        usuario_existe = False
        for usuario in estado:
            if usuario == nombre_usuario:
                usuario_existe = True
                break
        
        if usuario_existe:
            # Verificar si tiene objeto_excepcional
            objeto_excepcional_existe = False
            for clave in estado[nombre_usuario]:
                if clave == "objeto_excepcional":
                    objeto_excepcional_existe = True
                    break
            
            if objeto_excepcional_existe:
                resultado = estado[nombre_usuario]["objeto_excepcional"]
    except:
        pass
    
    return resultado


# =============================================================================
# GUARDAR_OBJETO_EQUIPADO
# =============================================================================
# Descripción: Guarda el objeto especial equipado para un usuario
# 
# Uso en Pygame: Se usa cuando el usuario elige un objeto
#
# Parámetros:
#   - nombre_usuario (str): Nombre del usuario
#   - objeto (str): Tipo de objeto a guardar
#   - estado_path (str): Ruta al archivo de estado
#
# Retorna:
#   - None
#
# Ejemplo de uso:
#   guardar_objeto_equipado("Juan", "espada", ruta_estado)
# =============================================================================
def guardar_objeto_equipado(nombre_usuario: str, objeto: str, estado_path: str = None) -> None:
    """Guarda el objeto especial equipado para un usuario."""
    if estado_path is None:
        estado_path = RUTA_ESTADO_BUFF
    
    estado = cargar_json(estado_path, {})

    existe = False
    for usuario in estado:
        if usuario == nombre_usuario:
            existe = True
            break

    if not existe:
        estado[nombre_usuario] = {}

    estado[nombre_usuario]["objeto_excepcional"] = objeto
    guardar_json(estado_path, estado)
    return None


# =============================================================================
# ELIMINAR_OBJETO_EQUIPADO
# =============================================================================
# Descripción: Elimina el objeto equipado de un usuario (objetos consumibles)
# 
# Uso en Pygame: Se usa cuando se consume un objeto
#
# Parámetros:
#   - nombre_usuario (str): Nombre del usuario
#   - estado_path (str): Ruta al archivo de estado
#
# Retorna:
#   - bool: True si se eliminó correctamente
#
# Ejemplo de uso:
#   eliminado = eliminar_objeto_equipado("Juan", ruta_estado)
# =============================================================================
def eliminar_objeto_equipado(nombre_usuario: str, estado_path: str = None) -> bool:
    """Elimina el objeto equipado de un usuario."""
    if estado_path is None:
        estado_path = RUTA_ESTADO_BUFF
    
    try:
        estado = cargar_json(estado_path, {})
        
        # Verificar si el usuario existe en el estado
        usuario_existe = False
        for usuario in estado:
            if usuario == nombre_usuario:
                usuario_existe = True
                break
        
        if usuario_existe:
            # Verificar si tiene objeto_excepcional
            objeto_excepcional_existe = False
            for clave in estado[nombre_usuario]:
                if clave == "objeto_excepcional":
                    objeto_excepcional_existe = True
                    break
            
            if objeto_excepcional_existe:
                # Crear nuevo diccionario sin objeto_excepcional
                nuevo_usuario_estado = {}
                for clave in estado[nombre_usuario]:
                    if clave != "objeto_excepcional":
                        nuevo_usuario_estado[clave] = estado[nombre_usuario][clave]
                estado[nombre_usuario] = nuevo_usuario_estado
                guardar_json(estado_path, estado)
                return True
    except:
        pass
    
    return False


# =============================================================================
# USAR_ARMADURA
# =============================================================================
# Descripción: Usa la armadura si está disponible y es necesario
# 
# Uso en Pygame: Se usa automáticamente en respuesta incorrecta
#
# Parámetros:
#   - nombre_usuario (str): Nombre del usuario
#   - es_correcta (bool): Si la respuesta fue correcta
#
# Retorna:
#   - dict: {"protegido": bool, "objeto_usado": bool}
#
# Ejemplo de uso:
#   resultado = usar_armadura("Juan", False)
# =============================================================================
def usar_armadura(nombre_usuario: str, es_correcta: bool) -> dict:
    """Usa la armadura si está disponible y es necesario."""
    resultado = {
        "protegido": False,
        "objeto_usado": False
    }
    
    if not es_correcta:
        objeto = verificar_objeto_equipado(nombre_usuario)
        if objeto == "armadura":
            eliminado = eliminar_objeto_equipado(nombre_usuario)
            resultado["protegido"] = True
            resultado["objeto_usado"] = eliminado
    
    return resultado


# =============================================================================
# USAR_RACIONES
# =============================================================================
# Descripción: Usa las raciones si están disponibles y la respuesta es incorrecta
# 
# Uso en Pygame: Se usa automáticamente en respuesta incorrecta
#
# Parámetros:
#   - nombre_usuario (str): Nombre del usuario
#   - es_correcta (bool): Si la respuesta fue correcta
#
# Retorna:
#   - dict: {"puntos_recuperados": int, "objeto_usado": bool}
#
# Ejemplo de uso:
#   resultado = usar_raciones("Juan", False)
# =============================================================================
def usar_raciones(nombre_usuario: str, es_correcta: bool) -> dict:
    """Usa las raciones si están disponibles y la respuesta es incorrecta."""
    resultado = {
        "puntos_recuperados": 0,
        "objeto_usado": False
    }
    
    if not es_correcta:
        objeto = verificar_objeto_equipado(nombre_usuario)
        if objeto == "raciones":
            puntos = OBJETOS_ESPECIALES["raciones"]["recuperacion_vida"]
            eliminado = eliminar_objeto_equipado(nombre_usuario)
            resultado["puntos_recuperados"] = puntos
            resultado["objeto_usado"] = eliminado
    
    return resultado


# =============================================================================
# USAR_BOLSA_MONEDAS
# =============================================================================
# Descripción: Usa la bolsa de monedas si está disponible y la respuesta es correcta
# 
# Uso en Pygame: Se usa automáticamente en respuesta correcta
#
# Parámetros:
#   - nombre_usuario (str): Nombre del usuario
#   - es_correcta (bool): Si la respuesta fue correcta
#   - puntos_base (int): Puntos base obtenidos
#
# Retorna:
#   - dict: {"puntos_extra": int, "objeto_usado": bool}
#
# Ejemplo de uso:
#   resultado = usar_bolsa_monedas("Juan", True, 3)
# =============================================================================
def usar_bolsa_monedas(nombre_usuario: str, es_correcta: bool, puntos_base: int) -> dict:
    """Usa la bolsa de monedas si está disponible y la respuesta es correcta."""
    resultado = {
        "puntos_extra": 0,
        "objeto_usado": False
    }
    
    if es_correcta:
        objeto = verificar_objeto_equipado(nombre_usuario)
        if objeto == "bolsa_monedas":
            eliminado = eliminar_objeto_equipado(nombre_usuario)
            resultado["puntos_extra"] = puntos_base
            resultado["objeto_usado"] = eliminado
    
    return resultado


# =============================================================================
# VERIFICAR_MERECIMIENTO_OBJETO
# =============================================================================
# Descripción: Verifica si el usuario merece un objeto especial
# 
# Uso en Pygame: Se usa al final de la partida
#
# Parámetros:
#   - nombre_usuario (str): Nombre del usuario
#   - respuestas_correctas (int): Cantidad de respuestas correctas
#   - total_preguntas (int): Total de preguntas respondidas
#
# Retorna:
#   - bool: True si merece un objeto, False en caso contrario
#
# Ejemplo de uso:
#   merece = verificar_merecimiento_objeto("Juan", 9, 10)
# =============================================================================
def verificar_merecimiento_objeto(nombre_usuario: str, respuestas_correctas: int, 
                                 total_preguntas: int) -> bool:
    """Verifica si el usuario merece un objeto especial."""
    # Ya tiene un objeto? No puede obtener otro
    objeto_actual = verificar_objeto_equipado(nombre_usuario)
    if objeto_actual is not None:
        return False
    
    # Verifica si cumple los requisitos
    if respuestas_correctas >= RESPUESTAS_CORRECTAS_PARA_OBJETO and total_preguntas == TOTAL_PREGUNTAS_PARA_OBJETO:
        return True
    
    return False


# =============================================================================
# OBTENER_OPCIONES_OBJETOS
# =============================================================================
# Descripción: Obtiene la lista de objetos disponibles para elegir
# 
# Uso en Pygame: Se usa para mostrar menú de selección de objetos
#
# Parámetros:
#   Ninguno
#
# Retorna:
#   - list: Lista de diccionarios con información de cada objeto
#
# Ejemplo de uso:
#   opciones = obtener_opciones_objetos()
# =============================================================================
def obtener_opciones_objetos() -> list:
    """Obtiene la lista de objetos disponibles para elegir."""
    opciones = []
    
    for tipo, info in OBJETOS_ESPECIALES.items():
        opcion = {
            "tipo": tipo,
            "nombre": info["nombre"],
            "descripcion": info.get("descripcion", "")
        }
        opciones.append(opcion)
    
    return opciones
