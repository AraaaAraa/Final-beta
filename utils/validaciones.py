# =============================================================================
# VALIDACIONES
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Funciones para validar datos y entradas del usuario.
#    Verifica rangos, formatos y valores permitidos.
#
# 📥 IMPORTADO EN:
#    - core/logica_preguntas.py (línea 8) - para validar_indice_opcion
#    - ui/consola/menu_consola.py - para validar_nombre_usuario
#
# 🔗 DEPENDENCIAS:
#    Ninguna (validaciones puras)
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Validaciones explícitas para evitar errores en runtime
#    - Retornos booleanos simples y claros
#    - Validación manual sin usar funciones built-in prohibidas
#    - UN SOLO return por función
# =============================================================================

# =============================================================================
# VALIDAR_INDICE_OPCION
# =============================================================================
# Descripción: Valida que un índice esté dentro del rango de opciones
# 
# Uso en Pygame: Se usa para validar clics en botones
#
# Parámetros:
#   - indice (int): Índice a validar
#   - opciones (list): Lista de opciones disponibles
#
# Retorna:
#   - bool: True si el índice es válido, False en caso contrario
#
# Ejemplo de uso:
#   if validar_indice_opcion(1, ["A", "B", "C", "D"]):
#       # índice válido
# =============================================================================
def validar_indice_opcion(indice: int, opciones: list) -> bool:
    """Valida que un índice esté dentro del rango de opciones."""
    es_valido = 0 <= indice < len(opciones)
    return es_valido


# =============================================================================
# VALIDAR_NOMBRE_USUARIO
# =============================================================================
# Descripción: Valida que un nombre de usuario sea válido
# 
# Uso en Pygame: Se usa en pantalla de login/registro
#
# Parámetros:
#   - nombre (str): Nombre a validar
#
# Retorna:
#   - bool: True si el nombre es válido, False en caso contrario
#
# Ejemplo de uso:
#   if validar_nombre_usuario("Juan"):
#       # nombre válido
# =============================================================================
def validar_nombre_usuario(nombre: str) -> bool:
    """Valida que un nombre de usuario sea válido."""
    # El nombre no puede estar vacío ni ser solo espacios
    nombre_limpio = nombre.strip()
    return len(nombre_limpio) > 0


# =============================================================================
# VALIDAR_NIVEL
# =============================================================================
# Descripción: Valida que un nivel esté en el rango válido (1-3)
# 
# Uso en Pygame: Se usa para validar progresión del juego
#
# Parámetros:
#   - nivel (int): Nivel a validar
#
# Retorna:
#   - bool: True si el nivel es válido (1, 2 o 3)
#
# Ejemplo de uso:
#   if validar_nivel(2):
#       # nivel válido
# =============================================================================
def validar_nivel(nivel: int) -> bool:
    """Valida que un nivel esté en el rango válido."""
    return nivel in [1, 2, 3]


# =============================================================================
# VALIDAR_DIFICULTAD
# =============================================================================
# Descripción: Valida que una dificultad esté en el rango válido (1-3)
# 
# Uso en Pygame: Se usa para validar preguntas
#
# Parámetros:
#   - dificultad (int): Dificultad a validar
#
# Retorna:
#   - bool: True si la dificultad es válida (1, 2 o 3)
#
# Ejemplo de uso:
#   if validar_dificultad(3):
#       # dificultad válida
# =============================================================================
def validar_dificultad(dificultad: int) -> bool:
    """Valida que una dificultad esté en el rango válido."""
    return dificultad in [1, 2, 3]


# =============================================================================
# VALIDAR_RESPUESTA_USUARIO
# =============================================================================
# Descripción: Valida que una respuesta de usuario sea una opción válida
# 
# Uso en Pygame: Se usa para validar inputs de respuesta
#
# Parámetros:
#   - respuesta (str): Respuesta del usuario
#   - opciones_validas (list): Lista de opciones válidas
#
# Retorna:
#   - bool: True si la respuesta es válida
#
# Ejemplo de uso:
#   if validar_respuesta_usuario("A", ["A", "B", "C", "D"]):
#       # respuesta válida
# =============================================================================
def validar_respuesta_usuario(respuesta: str, opciones_validas: list) -> bool:
    """Valida que una respuesta de usuario sea una opción válida."""
    for opcion in opciones_validas:
        if respuesta == opcion:
            return True
    return False
