# =============================================================================
# MENÚ CONSOLA
# =============================================================================
# Implementación del menú principal en modo consola
# =============================================================================

from data.repositorio_usuarios import obtener_usuario, obtener_ranking
from utils.formateadores import quitar_espacios_extremos
from utils.algoritmos import calcular_estadisticas_lista
from config.constantes import RUTA_USUARIOS, RUTA_PREGUNTAS
from config.mensajes import BIENVENIDA, PEDIR_NOMBRE, NOMBRE_VACIO, DESPEDIDA, OPCION_INVALIDA_MENU

# =============================================================================
# PEDIR_NOMBRE_USUARIO
# =============================================================================
# Descripción: Solicita el nombre de usuario en consola
# 
# Uso en Pygame: En pygame, esto sería un cuadro de texto gráfico
#
# Parámetros:
#   Ninguno
#
# Retorna:
#   - str: Nombre del usuario
#
# Ejemplo de uso:
#   nombre = pedir_nombre_usuario()
# =============================================================================
def pedir_nombre_usuario() -> str:
    """Solicita el nombre de usuario en consola."""
    while True:
        nombre = input(PEDIR_NOMBRE)
        nombre = quitar_espacios_extremos(nombre)
        if nombre:
            return nombre
        print(NOMBRE_VACIO)


# =============================================================================
# MOSTRAR_MENU_OPCIONES
# =============================================================================
# Descripción: Muestra las opciones del menú principal
# 
# Uso en Pygame: En pygame, serían botones gráficos
#
# Parámetros:
#   Ninguno
#
# Retorna:
#   - str: Opción seleccionada
#
# Ejemplo de uso:
#   opcion = mostrar_menu_opciones()
# =============================================================================
def mostrar_menu_opciones() -> str:
    """Muestra las opciones del menú principal."""
    print("\n===== MENÚ PRINCIPAL =====")
    print("1. Juego principal")
    print("2. Ver mis estadísticas")
    print("3. Ver ranking")
    print("4. Mini juego extra")
    print("5. Salir")
    
    opcion = input("Selecciona una opción (1-5): ").strip()
    return opcion


# =============================================================================
# MOSTRAR_ESTADISTICAS_CONSOLA
# =============================================================================
# Descripción: Muestra las estadísticas de un usuario en consola
# 
# Uso en Pygame: Se mostraría en un panel gráfico
#
# Parámetros:
#   - nombre (str): Nombre del usuario
#   - archivo_usuarios (str): Ruta al archivo de usuarios
#
# Retorna:
#   - None
#
# Ejemplo de uso:
#   mostrar_estadisticas_consola("Juan", ruta_usuarios)
# =============================================================================
def mostrar_estadisticas_consola(nombre: str, archivo_usuarios: str = None) -> None:
    """Muestra las estadísticas de un usuario en consola."""
    if not archivo_usuarios:
        archivo_usuarios = RUTA_USUARIOS
    
    usuario = obtener_usuario(nombre, archivo_usuarios)
    
    # Verificar si hay error
    tiene_error = False
    for clave in usuario:
        if clave == "error":
            tiene_error = True
            break
    
    if tiene_error:
        print(f"❌ {usuario['error']}")
        return
    
    # Calcular estadísticas
    stats = {
        "puntajes": calcular_estadisticas_lista(usuario.get("puntajes", [])),
        "tiempos": calcular_estadisticas_lista(usuario.get("tiempos", [])),
        "aciertos": calcular_estadisticas_lista(usuario.get("aciertos", [])),
        "porcentajes": calcular_estadisticas_lista(usuario.get("porcentajes", [])),
        "total_preguntas": calcular_estadisticas_lista(usuario.get("total_preguntas", []))
    }
    
    intentos = usuario.get("intentos", 0)
    ultimo_puntaje = usuario["puntajes"][-1] if usuario.get("puntajes") else 0
    ultimo_porcentaje = usuario["porcentajes"][-1] if usuario.get("porcentajes") else 0
    promedio_preguntas = stats["total_preguntas"]["promedio"]
    
    # Mostrar estadísticas
    print(f"\n📊 === ESTADÍSTICAS DE {nombre} ===")
    print(f"🎮 Partidas jugadas: {intentos}")
    print(f"📈 Promedio preguntas por partida: {round(promedio_preguntas, 1)}")
    print()
    print("🏆 PUNTAJES:")
    print(f"   • Mejor puntaje: {stats['puntajes']['mejor']}")
    print(f"   • Promedio: {round(stats['puntajes']['promedio'], 2)}")
    print(f"   • Último: {ultimo_puntaje}")
    print()
    print("✅ ACIERTOS:")
    print(f"   • Mejor porcentaje: {stats['porcentajes']['mejor']}%")
    print(f"   • Promedio porcentaje: {round(stats['porcentajes']['promedio'], 2)}%")
    print(f"   • Último porcentaje: {ultimo_porcentaje}%")
    print(f"   • Promedio respuestas correctas: {round(stats['aciertos']['promedio'], 2)}")
    print()
    print("⏱️ TIEMPOS:")
    print(f"   • Mejor tiempo: {stats['tiempos']['peor']} segundos")
    print(f"   • Promedio: {round(stats['tiempos']['promedio'], 2)} segundos")


# =============================================================================
# MOSTRAR_RANKING_CONSOLA
# =============================================================================
# Descripción: Muestra el ranking de jugadores en consola
# 
# Uso en Pygame: Se mostraría en una tabla gráfica
#
# Parámetros:
#   - archivo_usuarios (str): Ruta al archivo de usuarios
#
# Retorna:
#   - None
#
# Ejemplo de uso:
#   mostrar_ranking_consola(ruta_usuarios)
# =============================================================================
def mostrar_ranking_consola(archivo_usuarios: str = None) -> None:
    """Muestra el ranking de jugadores en consola."""
    if not archivo_usuarios:
        archivo_usuarios = RUTA_USUARIOS
    
    ranking = obtener_ranking(archivo_usuarios)
    
    print("\n" + "=" * 60)
    print("🏆 RANKING DE JUGADORES")
    print("=" * 60)

    if len(ranking) == 0:
        print("❌ No hay jugadores con estadísticas")
    else:
        i = 0
        while i < len(ranking):
            usuario = ranking[i]
            posicion = i + 1
            print(f"{posicion}. {usuario['nombre']}")
            print(f"   🏆 Mejor puntaje: {usuario['mejor_puntaje']}")
            print(f"   📊 Promedio: {usuario['promedio_puntaje']}")
            print(f"   📈 Mejor %: {usuario['mejor_porcentaje']}%")
            print(f"   🎮 Partidas: {usuario['intentos']}")
            print("-" * 40)
            i = i + 1


# =============================================================================
# EJECUTAR_MENU_CONSOLA
# =============================================================================
# Descripción: Ejecuta el menú principal en modo consola
# 
# Uso en Pygame: En pygame, esto sería un panel con botones gráficos
#                en lugar de texto
#
# Parámetros:
#   Ninguno
#
# Retorna:
#   - None
#
# Ejemplo de uso:
#   ejecutar_menu_consola()
# =============================================================================
def ejecutar_menu_consola() -> None:
    """Menú principal versión consola."""
    # Importar aquí para evitar importación circular
    from ui.consola.juego_consola import jugar_partida_completa_consola
    from ui.consola.minijuego_consola import ejecutar_minijuego_consola
    
    print(BIENVENIDA)
    print("=" * 50)
    nombre = pedir_nombre_usuario()
    
    ejecutando = True
    while ejecutando:
        opcion = mostrar_menu_opciones()
        
        if opcion == "1":
            jugar_partida_completa_consola(nombre, RUTA_USUARIOS, RUTA_PREGUNTAS)
        elif opcion == "2":
            mostrar_estadisticas_consola(nombre, RUTA_USUARIOS)
        elif opcion == "3":
            mostrar_ranking_consola(RUTA_USUARIOS)
        elif opcion == "4":
            ejecutar_minijuego_consola()
        elif opcion == "5":
            print(DESPEDIDA)
            ejecutando = False
        else:
            print(OPCION_INVALIDA_MENU)
