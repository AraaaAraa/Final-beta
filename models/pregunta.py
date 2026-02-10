# =============================================================================
# MODELO: PREGUNTA
# =============================================================================
# Representa una pregunta del juego con toda su información
# =============================================================================

# =============================================================================
# CREAR_PREGUNTA
# =============================================================================
# Descripción: Crea un objeto pregunta con todos sus datos
# 
# Uso en Pygame: Este modelo se usa igual, los datos se mostrarán
#                en widgets de pygame en lugar de prints
#
# Parámetros:
#   - id_pregunta (int): Identificador único de la pregunta
#   - nivel (int): Nivel de la pregunta (1, 2 o 3)
#   - descripcion (str): Texto de la pregunta
#   - dificultad (int): Dificultad (1=fácil, 2=medio, 3=difícil)
#   - categoria (str): Categoría temática de la pregunta
#   - opciones (list): Lista de opciones de respuesta
#   - respuesta_correcta (str): Respuesta correcta
#
# Retorna:
#   - dict: Diccionario con toda la información de la pregunta
#
# Ejemplo de uso:
#   pregunta = crear_pregunta(1, 1, "¿Quién era Zeus?", 2, "Mitología", 
#                             ["Dios", "Mortal", "Titán", "Héroe"], "Dios")
# =============================================================================
def crear_pregunta(id_pregunta: int, nivel: int, descripcion: str, 
                   dificultad: int, categoria: str, opciones: list, 
                   respuesta_correcta: str) -> dict:
    """Crea un objeto pregunta con todos sus datos."""
    pregunta = {}
    pregunta["id"] = id_pregunta
    pregunta["nivel"] = nivel
    pregunta["descripcion"] = descripcion
    pregunta["dificultad"] = dificultad
    pregunta["categoria"] = categoria
    pregunta["opciones"] = opciones
    pregunta["correcta"] = respuesta_correcta
    
    return pregunta


# =============================================================================
# VALIDAR_PREGUNTA
# =============================================================================
# Descripción: Verifica que una pregunta tenga todos los campos requeridos
# 
# Uso en Pygame: Validación igual, útil al cargar preguntas de archivos
#
# Parámetros:
#   - pregunta (dict): Diccionario con datos de la pregunta
#
# Retorna:
#   - bool: True si la pregunta es válida, False en caso contrario
#
# Ejemplo de uso:
#   if validar_pregunta(pregunta):
#       # usar pregunta
# =============================================================================
def validar_pregunta(pregunta: dict) -> bool:
    """Verifica que una pregunta tenga todos los campos requeridos."""
    campos_requeridos = ["id", "nivel", "descripcion", "dificultad", 
                        "categoria", "opciones", "correcta"]
    
    for campo in campos_requeridos:
        campo_existe = False
        for clave in pregunta:
            if clave == campo:
                campo_existe = True
                break
        if not campo_existe:
            return False
    
    return True


# =============================================================================
# OBTENER_CAMPO_PREGUNTA
# =============================================================================
# Descripción: Obtiene un campo específico de una pregunta de forma segura
# 
# Uso en Pygame: Útil para acceder a datos sin errores
#
# Parámetros:
#   - pregunta (dict): Diccionario con datos de la pregunta
#   - campo (str): Nombre del campo a obtener
#   - default: Valor por defecto si el campo no existe
#
# Retorna:
#   - any: Valor del campo o default si no existe
#
# Ejemplo de uso:
#   nivel = obtener_campo_pregunta(pregunta, "nivel", 1)
# =============================================================================
def obtener_campo_pregunta(pregunta: dict, campo: str, default=None):
    """Obtiene un campo específico de una pregunta de forma segura."""
    for clave in pregunta:
        if clave == campo:
            return pregunta[clave]
    return default
