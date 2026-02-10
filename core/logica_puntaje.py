# =============================================================================
# LÓGICA DE PUNTAJE
# =============================================================================
# Maneja todo el cálculo de puntajes sin dependencias de UI
# =============================================================================

from config.constantes import PUNTOS_POR_DIFICULTAD

# =============================================================================
# CALCULAR_PUNTOS_BASE
# =============================================================================
# Descripción: Calcula los puntos base según respuesta y dificultad
# 
# Uso en Pygame: Se usa igual, solo cambia donde se muestran los puntos
#
# Parámetros:
#   - es_correcta (bool): Si la respuesta es correcta
#   - dificultad (int): Nivel de dificultad (1, 2 o 3)
#
# Retorna:
#   - int: Puntos obtenidos (positivos si correcta, negativos si incorrecta)
#
# Ejemplo de uso:
#   puntos = calcular_puntos_base(True, 3)  # retorna 3
#   puntos = calcular_puntos_base(False, 2)  # retorna -2
# =============================================================================
def calcular_puntos_base(es_correcta: bool, dificultad: int) -> int:
    """Calcula los puntos base según respuesta y dificultad."""
    # Obtener puntos según dificultad
    puntos = 0
    for nivel, pts in PUNTOS_POR_DIFICULTAD.items():
        if nivel == dificultad:
            puntos = pts
            break
    
    # Si es incorrecta, los puntos son negativos
    var = puntos if es_correcta else -puntos
    return var


# =============================================================================
# CALCULAR_PUNTAJE_CON_BUFFEO
# =============================================================================
# Descripción: Calcula el puntaje total incluyendo puntos de buffeo
# 
# Uso en Pygame: Se usa igual para calcular puntos totales
#
# Parámetros:
#   - puntos_base (int): Puntos base de la respuesta
#   - puntos_buffeo (int): Puntos extra por buffeos
#   - puntos_raciones (int): Puntos recuperados por raciones
#   - puntos_bolsa (int): Puntos extra por bolsa de monedas
#
# Retorna:
#   - dict: Diccionario con puntos totales y desglose
#
# Ejemplo de uso:
#   resultado = calcular_puntaje_con_buffeo(3, 2, 0, 0)
# =============================================================================
def calcular_puntaje_con_buffeo(puntos_base: int, puntos_buffeo: int, 
                                puntos_raciones: int, puntos_bolsa: int) -> dict:
    """Calcula el puntaje total incluyendo puntos de buffeo."""
    total = puntos_base + puntos_buffeo + puntos_raciones + puntos_bolsa

    resultado = {
        "total": total,
        "base": puntos_base,
        "buffeo": puntos_buffeo,
        "raciones": puntos_raciones,
        "bolsa": puntos_bolsa
    }

    return resultado
