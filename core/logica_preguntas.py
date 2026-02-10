# =============================================================================
# LÓGICA DE PREGUNTAS
# =============================================================================
# Maneja la lógica de selección y evaluación de preguntas
# =============================================================================

from utils.formateadores import obtener_indice_letra, quitar_espacios_extremos, convertir_a_mayusculas
from utils.validaciones import validar_indice_opcion
from core.logica_buffeos import verificar_objeto_equipado, usar_armadura

# =============================================================================
# EVALUAR_RESPUESTA
# =============================================================================
# Descripción: Evalúa una respuesta del usuario (solo lógica, sin UI)
# 
# Uso en Pygame: Se usa igual, retorna datos para que la UI los muestre
#
# Parámetros:
#   - respuesta_usuario (str): Letra de la respuesta (A, B, C, D)
#   - opciones (list): Lista de opciones de la pregunta
#   - respuesta_correcta (str): Respuesta correcta
#   - nombre_usuario (str): Nombre del usuario
#
# Retorna:
#   - dict: {"valida": bool, "es_correcta": bool, "seleccion": str, 
#            "protegido_por_armadura": bool}
#
# Ejemplo de uso:
#   resultado = evaluar_respuesta("B", opciones, correcta, "Juan")
# =============================================================================
def evaluar_respuesta(respuesta_usuario: str, opciones: list, 
                     respuesta_correcta: str, nombre_usuario: str) -> dict:
    """Evalúa una respuesta del usuario sin hacer prints."""
    respuesta_limpia = convertir_a_mayusculas(quitar_espacios_extremos(respuesta_usuario))
    indice = obtener_indice_letra(respuesta_limpia)
    es_valido = validar_indice_opcion(indice, opciones)

    resultado = {
        "valida": es_valido,
        "es_correcta": False,
        "seleccion": "",
        "protegido_por_armadura": False
    }

    if es_valido:
        seleccion = opciones[indice]
        es_correcta = seleccion == respuesta_correcta
        
        # Verificar si usa armadura
        if not es_correcta:
            resultado_armadura = usar_armadura(nombre_usuario, es_correcta)
            if resultado_armadura["protegido"]:
                es_correcta = True
                resultado["protegido_por_armadura"] = True
        
        resultado["seleccion"] = seleccion
        resultado["es_correcta"] = es_correcta
    
    return resultado


# =============================================================================
# CONSTRUIR_MENSAJE_RESULTADO
# =============================================================================
# Descripción: Construye el mensaje de resultado según nivel y corrección
# 
# Uso en Pygame: Se usa para obtener el texto a mostrar en UI
#
# Parámetros:
#   - nivel (int): Nivel de la pregunta (1, 2, 3)
#   - es_correcta (bool): Si la respuesta es correcta
#   - respuesta_correcta (str): La respuesta correcta
#   - mostrar_correcta (bool): Si se debe mostrar la respuesta correcta
#
# Retorna:
#   - str: Mensaje formateado
#
# Ejemplo de uso:
#   mensaje = construir_mensaje_resultado(1, False, "Zeus", True)
# =============================================================================
def construir_mensaje_resultado(nivel: int, es_correcta: bool, 
                               respuesta_correcta: str, 
                               mostrar_correcta: bool = True) -> str:
    """Construye el mensaje de resultado según nivel y corrección."""
    mensaje = ""
    
    # Determinar el mensaje base usando condicionales
    if nivel == 1:
        if es_correcta:
            mensaje = "✅ CORRECTO\nFELICIDADES NO SOS UN BURRO!!!"
        else:
            mensaje = "❌ INCORRECTO\nSos un burro"
    elif nivel == 2:
        if es_correcta:
            mensaje = "✅ CORRECTO\nFuaaaa qué inteligente!!!"
        else:
            mensaje = "❌ INCORRECTO\nBue... ¿qué pasó?"
    elif nivel == 3:
        if es_correcta:
            mensaje = "✅ CORRECTO\nNi yo la sabía!!!"
        else:
            mensaje = "❌ INCORRECTO\nTe entiendo la verdad"
    
    # Agregar respuesta correcta si es necesario
    if not es_correcta and mostrar_correcta:
        mensaje += "\n💡 La respuesta correcta era: " + respuesta_correcta
    
    return mensaje


# =============================================================================
# CALCULAR_RACHA_ACTUAL
# =============================================================================
# Descripción: Calcula la racha actual de respuestas correctas
# 
# Uso en Pygame: Se usa para mostrar indicador de racha
#
# Parámetros:
#   - respuestas_actuales (list): Lista de respuestas hasta el momento
#
# Retorna:
#   - int: Número de respuestas correctas consecutivas
#
# Ejemplo de uso:
#   racha = calcular_racha_actual(respuestas)
# =============================================================================
def calcular_racha_actual(respuestas_actuales: list) -> int:
    """Calcula la racha actual de respuestas correctas."""
    if not respuestas_actuales:
        return 0
    
    racha_actual = 0
    i = len(respuestas_actuales) - 1
    
    while i >= 0:
        respuesta = respuestas_actuales[i]
        es_correcta = False
        for clave in respuesta:
            if clave == "es_correcta":
                es_correcta = respuesta[clave]
                break
        
        if es_correcta:
            racha_actual += 1
        else:
            break
        
        i -= 1
    
    return racha_actual


# =============================================================================
# DETERMINAR_INTENTOS_MAXIMOS
# =============================================================================
# Descripción: Determina cuántos intentos tiene el usuario según su objeto
# 
# Uso en Pygame: Se usa para configurar el sistema de intentos
#
# Parámetros:
#   - nombre_usuario (str): Nombre del usuario
#
# Retorna:
#   - int: Número máximo de intentos (1 normal, 2 con espada)
#
# Ejemplo de uso:
#   max_intentos = determinar_intentos_maximos("Juan")
# =============================================================================
def determinar_intentos_maximos(nombre_usuario: str) -> int:
    """Determina cuántos intentos tiene el usuario según su objeto."""
    objeto = verificar_objeto_equipado(nombre_usuario)
    if objeto == "espada":
        return 2
    return 1


# =============================================================================
# CONSTRUIR_RESULTADO_RESPUESTA
# =============================================================================
# Descripción: Construye el resultado completo de una respuesta
# 
# Uso en Pygame: Retorna todos los datos necesarios para actualizar la UI
#
# Parámetros:
#   - evaluacion (dict): Resultado de evaluar_respuesta
#   - nivel (int): Nivel de la pregunta
#   - respuesta_correcta (str): Respuesta correcta
#   - puntos (dict): Diccionario con puntos calculados
#   - mostrar_correcta (bool): Si se debe mostrar la respuesta correcta
#
# Retorna:
#   - dict: Resultado completo con toda la información
#
# Ejemplo de uso:
#   resultado = construir_resultado_respuesta(eval, 1, "Zeus", puntos, True)
# =============================================================================
def construir_resultado_respuesta(evaluacion: dict, nivel: int, 
                                  respuesta_correcta: str, puntos: dict,
                                  mostrar_correcta: bool = True) -> dict:
    """Construye el resultado completo de una respuesta."""
    if not evaluacion["valida"]:
        return {
            "valida": False,
            "es_correcta": False,
            "mensaje": "❌ Opción inválida.",
            "puntos": 0,
            "puntos_base": 0,
            "puntos_buffeo": 0,
            "seleccion": "",
            "protegido_por_armadura": False
        }
    
    mensaje = construir_mensaje_resultado(
        nivel, 
        evaluacion["es_correcta"], 
        respuesta_correcta, 
        mostrar_correcta
    )
    
    resultado = {
        "valida": True,
        "es_correcta": evaluacion["es_correcta"],
        "mensaje": mensaje,
        "puntos": puntos.get("puntos", puntos.get("total", 0)),
        "puntos_base": puntos.get("puntos_base", puntos.get("base", 0)),
        "puntos_buffeo": puntos.get("puntos_buffeo", puntos.get("buffeo", 0)),
        "seleccion": evaluacion["seleccion"],
        "protegido_por_armadura": evaluacion.get("protegido_por_armadura", False)
    }
    
    return resultado


# =============================================================================
# CONTAR_ERRORES_TOTALES
# =============================================================================
# Descripción: Cuenta el total de errores en una lista de respuestas
# 
# Uso en Pygame: Se usa para verificar condición de game over
#
# Parámetros:
#   - respuestas (list): Lista de respuestas
#
# Retorna:
#   - int: Cantidad de respuestas incorrectas
#
# Ejemplo de uso:
#   errores = contar_errores_totales(respuestas)
# =============================================================================
def contar_errores_totales(respuestas: list) -> int:
    """Cuenta el total de errores en una lista de respuestas."""
    errores = 0
    for respuesta in respuestas:
        # Buscar la clave "es_correcta"
        es_correcta = False
        for clave in respuesta:
            if clave == "es_correcta":
                es_correcta = respuesta[clave]
                break
        
        if not es_correcta:
            errores += 1
    
    return errores
