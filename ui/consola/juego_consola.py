# =============================================================================
# JUEGO CONSOLA
# =============================================================================
# Implementación del flujo de juego en modo consola
# Esta capa solo se encarga de mostrar información y recibir inputs
# Toda la lógica está en el módulo core/
# =============================================================================

import time
from data.repositorio_preguntas import cargar_preguntas_desde_csv
from data.repositorio_usuarios import guardar_estadisticas_usuario
from core.logica_juego import (
    obtener_pregunta_para_nivel,
    procesar_pregunta_completa,
    construir_estadisticas_partida,
    verificar_condicion_fin_partida,
    calcular_datos_buffeo_para_ui
)
from core.logica_preguntas import calcular_racha_actual, determinar_intentos_maximos
from core.logica_buffeos import (
    verificar_merecimiento_objeto,
    guardar_objeto_equipado,
    obtener_opciones_objetos
)
from utils.formateadores import quitar_espacios_extremos, convertir_a_mayusculas
from config.constantes import PREGUNTAS_POR_NIVEL
from config.mensajes import *

# =============================================================================
# MOSTRAR_PREGUNTA_CONSOLA
# =============================================================================
# Descripción: Muestra una pregunta en la consola y obtiene la respuesta
# 
# Uso en Pygame: En pygame, se mostraría en un panel gráfico con botones
#
# Parámetros:
#   - pregunta (dict): Datos de la pregunta
#
# Retorna:
#   - str: Respuesta del usuario (A, B, C, D)
#
# Ejemplo de uso:
#   respuesta = mostrar_pregunta_consola(pregunta)
# =============================================================================
def mostrar_pregunta_consola(pregunta: dict) -> str:
    """Muestra una pregunta en la consola."""
    print(f"\n🎯 NIVEL {pregunta['nivel']} - {convertir_a_mayusculas(pregunta['categoria'])}")
    print(f"📝 {pregunta['descripcion']}")
    print()
    opciones = pregunta['opciones']
    letras = "ABCD"
    i = 0
    while i < len(opciones):
        print(f"{letras[i]}) {opciones[i]}")
        i = i + 1
    respuesta = input("\n🤔 Tu respuesta (A/B/C/D): ")
    respuesta = convertir_a_mayusculas(quitar_espacios_extremos(respuesta))
    return respuesta


# =============================================================================
# MOSTRAR_RESULTADO_CONSOLA
# =============================================================================
# Descripción: Muestra el resultado de una respuesta en consola
# 
# Uso en Pygame: Mostraría animación o panel con el resultado
#
# Parámetros:
#   - resultado (dict): Datos del resultado
#
# Retorna:
#   - None
#
# Ejemplo de uso:
#   mostrar_resultado_consola(resultado)
# =============================================================================
def mostrar_resultado_consola(resultado: dict) -> None:
    """Muestra el resultado de una respuesta en consola."""
    print(f"\n{resultado['mensaje']}")
    
    # Mostrar si fue protegido por armadura
    if resultado.get("protegido_por_armadura", False):
        print(ARMADURA_ACTIVADA)
        print(ELIMINANDO_ARMADURA)
    
    puntos_buffeo = resultado.get("puntos_buffeo", 0)
    
    if puntos_buffeo > 0:
        puntos_base = resultado.get("puntos_base", 0)
        print(f"📊 Puntos base: {puntos_base}")
        print(f"🔥 Puntos buffeo: +{puntos_buffeo}")
        print(f"📊 Puntos totales: {resultado['puntos']}")
    else:
        print(f"📊 Puntos obtenidos: {resultado['puntos']}")


# =============================================================================
# PREGUNTAR_REINTENTO
# =============================================================================
# Descripción: Pregunta al usuario si quiere usar su reintento
# 
# Uso en Pygame: Mostraría un diálogo con botones Sí/No
#
# Parámetros:
#   Ninguno
#
# Retorna:
#   - bool: True si quiere reintentar, False en caso contrario
#
# Ejemplo de uso:
#   if preguntar_reintento():
#       # procesar reintento
# =============================================================================
def preguntar_reintento() -> bool:
    """Pregunta al usuario si quiere usar su reintento."""
    usar_reintento = input("\n🛡️ ¿Quieres usar tu buffeo de reintento? (s/n): ").lower().strip()
    if usar_reintento == "s":
        print("🔄 Usando reintento...")
        return True
    return False


# =============================================================================
# PROCESAR_PREGUNTA_CON_UI
# =============================================================================
# Descripción: Procesa una pregunta completa con interfaz de consola
# 
# Uso en Pygame: Similar pero con interfaz gráfica
#
# Parámetros:
#   - pregunta (dict): Pregunta a procesar
#   - nombre_usuario (str): Nombre del usuario
#   - racha_actual (int): Racha de respuestas correctas
#
# Retorna:
#   - dict: Resultado completo de la pregunta
#
# Ejemplo de uso:
#   resultado = procesar_pregunta_con_ui(pregunta, "Juan", 3)
# =============================================================================
def procesar_pregunta_con_ui(pregunta: dict, nombre_usuario: str, racha_actual: int) -> dict:
    """Procesa una pregunta completa con interfaz de consola."""
    max_intentos = determinar_intentos_maximos(nombre_usuario)
    intentos = 0
    resultado_final = None
    
    while intentos < max_intentos:
        if intentos > 0:
            print(f"\n🛡️ REINTENTO #{intentos + 1}")
            print("=" * 20)
        
        # Mostrar pregunta y obtener respuesta
        inicio = time.time()
        respuesta = mostrar_pregunta_consola(pregunta)
        fin = time.time()
        duracion = round(fin - inicio, 2)
        
        # Procesar respuesta
        resultado = procesar_pregunta_completa(
            pregunta, nombre_usuario, racha_actual,
            respuesta, intentos, max_intentos
        )
        
        # Mostrar resultado
        mostrar_resultado_consola(resultado)
        
        # Si es válida y correcta, terminar
        if resultado["valida"] and resultado["es_correcta"]:
            resultado_final = resultado
            resultado_final["tiempo_segundos"] = duracion
            resultado_final["intentos_usados"] = intentos + 1
            break
        
        # Si es inválida, continuar sin contar intento
        if not resultado["valida"]:
            continue
        
        # Si es incorrecta y puede reintentar
        if resultado.get("puede_reintentar", False):
            if preguntar_reintento():
                intentos += 1
                continue
            else:
                resultado_final = resultado
                resultado_final["tiempo_segundos"] = duracion
                resultado_final["intentos_usados"] = intentos + 1
                break
        else:
            resultado_final = resultado
            resultado_final["tiempo_segundos"] = duracion
            resultado_final["intentos_usados"] = intentos + 1
            break
        
        intentos += 1
    
    if resultado_final is None:
        resultado_final = resultado
        resultado_final["tiempo_segundos"] = duracion
        resultado_final["intentos_usados"] = intentos
    
    return resultado_final


# =============================================================================
# JUGAR_NIVEL_CONSOLA
# =============================================================================
# Descripción: Juega un nivel completo en consola
# 
# Uso en Pygame: Similar pero con interfaz gráfica
#
# Parámetros:
#   - nivel (int): Número del nivel
#   - preguntas (dict): Todas las preguntas
#   - preguntas_usadas (list): IDs de preguntas ya usadas
#   - nombre_usuario (str): Nombre del usuario
#   - respuestas_partida (list): Respuestas de la partida
#
# Retorna:
#   - dict: Resultado del nivel
#
# Ejemplo de uso:
#   resultado = jugar_nivel_consola(1, preguntas, [], "Juan", [])
# =============================================================================
def jugar_nivel_consola(nivel: int, preguntas: dict, preguntas_usadas: list,
                       nombre_usuario: str, respuestas_partida: list) -> dict:
    """Juega un nivel completo en consola."""
    cantidad = PREGUNTAS_POR_NIVEL[nivel]
    
    print(NIVEL_INICIADO.format(nivel, cantidad))
    
    respuestas_nivel = []
    puntos_nivel = 0
    buffeo_nivel = 0
    correctas_nivel = 0
    tiempo_nivel = 0.0
    
    i = 0
    while i < cantidad:
        print(f"\n--- Pregunta {i + 1} de {cantidad} ---")
        
        # Calcular racha
        racha = calcular_racha_actual(respuestas_partida)
        if racha > 0:
            print(f"🔥 Racha actual: {racha} respuestas correctas")
        
        # Obtener pregunta
        pregunta = obtener_pregunta_para_nivel(preguntas, nivel, preguntas_usadas)
        if pregunta is None:
            print(f"❌ No hay más preguntas disponibles para el nivel {nivel}")
            break
        
        # Procesar pregunta
        resultado = procesar_pregunta_con_ui(pregunta, nombre_usuario, racha)
        
        # Registrar respuesta
        respuesta_completa = {
            "pregunta_id": pregunta["id"],
            "nivel": nivel,
            "es_correcta": resultado["es_correcta"],
            "puntos": resultado["puntos"],
            "puntos_base": resultado.get("puntos_base", 0),
            "puntos_buffeo": resultado.get("puntos_buffeo", 0),
            "tiempo_segundos": resultado.get("tiempo_segundos", 0),
            "seleccion": resultado.get("seleccion", ""),
            "intentos_usados": resultado.get("intentos_usados", 1)
        }
        
        respuestas_nivel.append(respuesta_completa)
        respuestas_partida.append(respuesta_completa)
        preguntas_usadas.append(pregunta["id"])
        
        # Acumular estadísticas
        puntos_nivel += resultado["puntos"]
        buffeo_nivel += resultado.get("puntos_buffeo", 0)
        tiempo_nivel += resultado.get("tiempo_segundos", 0)
        if resultado["es_correcta"]:
            correctas_nivel += 1
        
        i += 1
    
    return {
        "respuestas": respuestas_nivel,
        "total_puntos": puntos_nivel,
        "total_buffeo": buffeo_nivel,
        "correctas": correctas_nivel,
        "tiempo": tiempo_nivel
    }


# =============================================================================
# MOSTRAR_RESUMEN_FINAL
# =============================================================================
# Descripción: Muestra el resumen final de la partida
# 
# Uso en Pygame: Pantalla de resumen con gráficos
#
# Parámetros:
#   - nombre (str): Nombre del jugador
#   - estadisticas (dict): Estadísticas de la partida
#
# Retorna:
#   - None
#
# Ejemplo de uso:
#   mostrar_resumen_final("Juan", estadisticas)
# =============================================================================
def mostrar_resumen_final(nombre: str, estadisticas: dict) -> None:
    """Muestra el resumen final de la partida."""
    correctas = estadisticas["respuestas_correctas"]
    total = estadisticas["total_preguntas"]
    puntos_totales = estadisticas["puntos_totales"]
    puntos_buffeo = estadisticas["puntos_buffeo"]
    tiempo_total = estadisticas["tiempo_total_segundos"]
    
    print("\n" + "="*50)
    print("🏁 RESUMEN FINAL")
    print("="*50)
    print(f"👤 Jugador: {nombre}")
    print(f"✅ Respuestas correctas: {correctas}/{total}")
    print(f"📊 Puntos base: {puntos_totales - puntos_buffeo}")
    if puntos_buffeo > 0:
        print(f"🔥 Puntos por buffeo: +{puntos_buffeo}")
    print(f"📊 Puntos totales: {puntos_totales}")
    print(f"⏱️ Tiempo total: {round(tiempo_total, 2)} segundos")
    if total > 0:
        porcentaje = (correctas / total) * 100
        print(f"📈 Porcentaje de aciertos: {round(porcentaje, 1)}%")


# =============================================================================
# SELECCIONAR_OBJETO_ESPECIAL
# =============================================================================
# Descripción: Permite al usuario seleccionar un objeto especial
# 
# Uso en Pygame: Menú gráfico de selección
#
# Parámetros:
#   Ninguno
#
# Retorna:
#   - str: Tipo de objeto seleccionado
#
# Ejemplo de uso:
#   objeto = seleccionar_objeto_especial()
# =============================================================================
def seleccionar_objeto_especial() -> str:
    """Permite al usuario seleccionar un objeto especial."""
    opciones = obtener_opciones_objetos()
    
    print(ELIGE_OBJETO)
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}) {opcion['nombre']} ({opcion['descripcion']})")
    
    while True:
        eleccion = input("¿Cuál eliges? (1-4): ").strip()
        if eleccion in ["1", "2", "3", "4"]:
            return opciones[int(eleccion) - 1]["tipo"]
        print("Opción inválida. Por favor elige 1, 2, 3 o 4.")


# =============================================================================
# JUGAR_PARTIDA_COMPLETA_CONSOLA
# =============================================================================
# Descripción: Ejecuta una partida completa en modo consola
# 
# Uso en Pygame: Similar pero con interfaz gráfica
#
# Parámetros:
#   - nombre (str): Nombre del usuario
#   - archivo_usuarios (str): Ruta al archivo de usuarios
#   - archivo_preguntas (str): Ruta al archivo de preguntas
#
# Retorna:
#   - None
#
# Ejemplo de uso:
#   jugar_partida_completa_consola("Juan", ruta_usuarios, ruta_preguntas)
# =============================================================================
def jugar_partida_completa_consola(nombre: str, archivo_usuarios: str, archivo_preguntas: str) -> None:
    """Ejecuta una partida completa en modo consola."""
    print(INICIANDO_PARTIDA.format("="*50, "="*50))
    
    # Cargar preguntas
    preguntas = cargar_preguntas_desde_csv(archivo_preguntas)
    
    # Inicializar estado
    preguntas_usadas = []
    respuestas_partida = []
    puntos_totales = 0
    buffeo_totales = 0
    correctas_totales = 0
    tiempo_total = 0.0
    
    # Jugar niveles
    for nivel in [1, 2, 3]:
        resultado_nivel = jugar_nivel_consola(
            nivel, preguntas, preguntas_usadas, 
            nombre, respuestas_partida
        )
        
        puntos_totales += resultado_nivel["total_puntos"]
        buffeo_totales += resultado_nivel["total_buffeo"]
        correctas_totales += resultado_nivel["correctas"]
        tiempo_total += resultado_nivel["tiempo"]
        
        # Verificar si debe terminar
        if verificar_condicion_fin_partida(respuestas_partida):
            print(FIN_PARTIDA_ERRORES)
            break
    
    # Verificar si merece objeto especial
    total_preguntas = len(respuestas_partida)
    if verificar_merecimiento_objeto(nombre, correctas_totales, total_preguntas):
        print(FELICITACIONES_OBJETO)
        objeto = seleccionar_objeto_especial()
        guardar_objeto_equipado(nombre, objeto)
        # Mostrar mensaje del objeto
        if objeto == "espada":
            print(MENSAJE_ESPADA)
        elif objeto == "armadura":
            print(MENSAJE_ARMADURA)
        elif objeto == "raciones":
            print(MENSAJE_RACIONES)
        elif objeto == "bolsa_monedas":
            print(MENSAJE_BOLSA_MONEDAS)
    
    # Construir y guardar estadísticas
    estadisticas = construir_estadisticas_partida(
        respuestas_partida, puntos_totales, buffeo_totales, tiempo_total
    )
    
    guardar_estadisticas_usuario(nombre, estadisticas, archivo_usuarios)
    mostrar_resumen_final(nombre, estadisticas)
