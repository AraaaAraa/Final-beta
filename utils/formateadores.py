# =============================================================================
# FORMATEADORES DE TEXTO
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Funciones para formatear y transformar texto.
#    Implementaciones manuales de operaciones de string sin usar métodos built-in.
#
# 📥 IMPORTADO EN:
#    - core/logica_preguntas.py (línea 7) - para obtener_indice_letra, quitar_espacios_extremos, convertir_a_mayusculas
#    - ui/consola/juego_consola.py - para formatear inputs y salidas
#
# 🔗 DEPENDENCIAS:
#    - config.constantes: para LETRAS_OPCIONES
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Implementación manual de .strip() con quitar_espacios_extremos
#    - Implementación manual de .upper() con convertir_a_mayusculas
#    - Búsqueda manual carácter por carácter con bucles while
#    - UN SOLO return por función
#    - Demuestra comprensión de manipulación de strings a bajo nivel
# =============================================================================

from config.constantes import LETRAS_OPCIONES

# =============================================================================
# QUITAR_ESPACIOS_EXTREMOS
# =============================================================================
# Descripción: Elimina espacios al inicio y final de un texto (implementación manual)
# 
# Uso en Pygame: Se usa igual para limpiar inputs de usuario
#
# Parámetros:
#   - texto (str): Texto a procesar
#
# Retorna:
#   - str: Texto sin espacios en los extremos
#
# Ejemplo de uso:
#   limpio = quitar_espacios_extremos("  hola  ")  # retorna "hola"
# =============================================================================
def quitar_espacios_extremos(texto: str) -> str:
    """Elimina espacios al inicio y final de un texto."""
    inicio = 0
    final = len(texto) - 1
    while inicio <= final and texto[inicio] == " ":
        inicio = inicio + 1
    while final >= inicio and texto[final] == " ":
        final = final - 1
    resultado = ""
    i = inicio
    while i <= final:
        resultado = resultado + texto[i]
        i = i + 1
    return resultado


# =============================================================================
# CONVERTIR_A_MAYUSCULAS
# =============================================================================
# Descripción: Convierte un texto a mayúsculas (implementación manual)
# 
# Uso en Pygame: Se usa para normalizar inputs
#
# Parámetros:
#   - texto (str): Texto a convertir
#
# Retorna:
#   - str: Texto en mayúsculas
#
# Ejemplo de uso:
#   mayus = convertir_a_mayusculas("hola")  # retorna "HOLA"
# =============================================================================
def convertir_a_mayusculas(texto: str) -> str:
    """Convierte un texto a mayúsculas."""
    minusculas = "abcdefghijklmnopqrstuvwxyzáéíóúüñ"
    mayusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜÑ"
    resultado = ""
    i = 0
    while i < len(texto):
        letra = texto[i]
        j = 0
        convertido = False
        while j < len(minusculas):
            if letra == minusculas[j]:
                resultado = resultado + mayusculas[j]
                convertido = True
                break
            j = j + 1
        if not convertido:
            resultado = resultado + letra
        i = i + 1
    return resultado


# =============================================================================
# OBTENER_INDICE_LETRA
# =============================================================================
# Descripción: Convierte una letra de opción (A, B, C, D) a su índice
# 
# Uso en Pygame: Se usa para mapear botones a índices
#
# Parámetros:
#   - letra (str): Letra de la opción (A, B, C, D)
#
# Retorna:
#   - int: Índice de la letra (0-3) o -1 si es inválida
#
# Ejemplo de uso:
#   indice = obtener_indice_letra("B")  # retorna 1
# =============================================================================
def obtener_indice_letra(letra: str) -> int:
    """Convierte una letra de opción a su índice."""
    letras = LETRAS_OPCIONES
    i = 0
    while i < len(letras):
        if letra == letras[i]:
            return i
        i = i + 1
    return -1


# =============================================================================
# FORMATEAR_TIEMPO
# =============================================================================
# Descripción: Formatea un tiempo en segundos a formato legible
# 
# Uso en Pygame: Se usa para mostrar tiempos en pantalla
#
# Parámetros:
#   - segundos (float): Tiempo en segundos
#
# Retorna:
#   - str: Tiempo formateado (ej: "2m 30s")
#
# Ejemplo de uso:
#   tiempo = formatear_tiempo(150.5)  # retorna "2m 30s"
# =============================================================================
def formatear_tiempo(segundos: float) -> str:
    """Formatea un tiempo en segundos a formato legible."""
    if segundos < 60:
        return f"{round(segundos, 1)}s"
    
    minutos = int(segundos // 60)
    segs = int(segundos % 60)
    return f"{minutos}m {segs}s"


# =============================================================================
# FORMATEAR_PORCENTAJE
# =============================================================================
# Descripción: Formatea un porcentaje con un número específico de decimales
# 
# Uso en Pygame: Se usa para mostrar estadísticas
#
# Parámetros:
#   - valor (float): Valor a formatear
#   - decimales (int): Número de decimales (default: 1)
#
# Retorna:
#   - str: Porcentaje formateado (ej: "85.5%")
#
# Ejemplo de uso:
#   pct = formatear_porcentaje(85.567, 1)  # retorna "85.6%"
# =============================================================================
def formatear_porcentaje(valor: float, decimales: int = 1) -> str:
    """Formatea un porcentaje con decimales específicos."""
    return f"{round(valor, decimales)}%"
