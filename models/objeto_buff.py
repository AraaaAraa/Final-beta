# =============================================================================
# MODELO: OBJETO BUFF
# =============================================================================
# Representa los objetos especiales/buffs del juego
# =============================================================================

# =============================================================================
# CREAR_OBJETO_BUFF
# =============================================================================
# Descripción: Crea un objeto buff con sus propiedades
# 
# Uso en Pygame: Se usa igual, los objetos se mostrarán con iconos
#
# Parámetros:
#   - tipo (str): Tipo de objeto ("espada", "armadura", "raciones", "bolsa_monedas")
#   - nombre (str): Nombre del objeto
#   - descripcion (str): Descripción del efecto
#   - propiedades (dict): Propiedades específicas del objeto
#
# Retorna:
#   - dict: Diccionario con información del objeto
#
# Ejemplo de uso:
#   espada = crear_objeto_buff("espada", "Espada de la Esfinge", 
#                              "Da puntos extra", {"puntos": 2})
# =============================================================================
def crear_objeto_buff(tipo: str, nombre: str, descripcion: str, propiedades: dict) -> dict:
    """Crea un objeto buff con sus propiedades."""
    objeto = {}
    objeto["tipo"] = tipo
    objeto["nombre"] = nombre
    objeto["descripcion"] = descripcion
    objeto["propiedades"] = propiedades
    
    return objeto


# =============================================================================
# OBTENER_EFECTO_OBJETO
# =============================================================================
# Descripción: Obtiene el efecto de un objeto buff
# 
# Uso en Pygame: Útil para mostrar información del objeto
#
# Parámetros:
#   - objeto_tipo (str): Tipo de objeto
#
# Retorna:
#   - dict: Información del efecto del objeto
#
# Ejemplo de uso:
#   efecto = obtener_efecto_objeto("espada")
# =============================================================================
def obtener_efecto_objeto(objeto_tipo: str) -> dict:
    """Obtiene el efecto de un objeto buff."""
    efectos = {
        "espada": {
            "puntos_extra": 2,
            "permite_reintento": True,
            "consumible": False
        },
        "armadura": {
            "proteccion": True,
            "consumible": True
        },
        "raciones": {
            "recuperacion_vida": 3,
            "consumible": True
        },
        "bolsa_monedas": {
            "duplica_puntos": True,
            "consumible": True
        }
    }
    
    # Buscar el efecto del objeto
    for tipo in efectos:
        if tipo == objeto_tipo:
            return efectos[tipo]
    
    return {}


# =============================================================================
# ES_OBJETO_CONSUMIBLE
# =============================================================================
# Descripción: Verifica si un objeto es consumible (se usa una sola vez)
# 
# Uso en Pygame: Útil para saber si eliminar el objeto del inventario
#
# Parámetros:
#   - objeto_tipo (str): Tipo de objeto
#
# Retorna:
#   - bool: True si el objeto es consumible, False en caso contrario
#
# Ejemplo de uso:
#   if es_objeto_consumible("armadura"):
#       # eliminar del inventario
# =============================================================================
def es_objeto_consumible(objeto_tipo: str) -> bool:
    """Verifica si un objeto es consumible."""
    efecto = obtener_efecto_objeto(objeto_tipo)
    
    # Buscar la clave "consumible"
    for clave in efecto:
        if clave == "consumible":
            return efecto["consumible"]
    
    return False
