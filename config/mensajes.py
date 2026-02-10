# =============================================================================
# MENSAJES Y TEXTOS DEL JUEGO
# =============================================================================
# Este archivo centraliza todos los mensajes y textos del juego
# Facilita la traducción y personalización de mensajes
# =============================================================================

# =============================================================================
# MENSAJES DE BIENVENIDA Y MENÚ
# =============================================================================

BIENVENIDA = "¡Bienvenid@ soldado! ¿Listo para la batalla?"
PEDIR_NOMBRE = "🗡️ Ingresá tu nombre de usuario: "
NOMBRE_VACIO = "🗡️ El nombre no puede estar vacío. Intentá de nuevo."
DESPEDIDA = "👋 ¡Gracias por jugar! ¡Hasta la próxima!"

# =============================================================================
# MENSAJES DE BUFFEOS
# =============================================================================

BUFFEO_ACTIVADO = "🔥 ¡BUFFEO ACTIVADO! Has recibido {} puntos extra por tu racha de {} respuestas correctas!"
BUFFEO_TOTAL = "🔥 ¡BUFFEO TOTAL! Has recibido {} puntos extra (racha: {}, espada: +2)!"
ESPADA_ACTIVADA = "⚔️ ¡ESPADA ACTIVADA! +2 puntos extra por la espada"
REINTENTO_RACHA = "🛡️ ¡BUFFEO DE REINTENTO! Tienes derecho a un reintento gracias a tu racha de {} respuestas correctas."
REINTENTO_ESPADA = "⚔️ ¡REINTENTO DE ESPADA! Tienes derecho a un reintento especial gracias a tu espada!"
ARMADURA_ACTIVADA = "🛡️ ¡ARMADURA ACTIVADA! Tu respuesta incorrecta ha sido protegida."
ELIMINANDO_ARMADURA = "🔧 Eliminando armadura del inventario..."
RACIONES_ACTIVADAS = "🍖 ¡RACIONES ACTIVADAS! Has recuperado 3 puntos de vida."
CONSUMIENDO_RACIONES = "🔧 Consumiendo raciones del inventario..."
BOLSA_MONEDAS_ACTIVADA = "💰 ¡BOLSA DE MONEDAS ACTIVADA! Has duplicado tus puntos: +{}"
CONSUMIENDO_BOLSA = "🔧 Consumiendo bolsa de monedas del inventario..."

# =============================================================================
# MENSAJES DE RESPUESTAS POR NIVEL
# =============================================================================

RESPUESTAS_NIVEL_1 = {
    "correcta": "✅ CORRECTO\nFELICIDADES NO SOS UN BURRO!!!",
    "incorrecta": "❌ INCORRECTO\nSos un burro"
}

RESPUESTAS_NIVEL_2 = {
    "correcta": "✅ CORRECTO\nFuaaaa qué inteligente!!!",
    "incorrecta": "❌ INCORRECTO\nBue... ¿qué pasó?"
}

RESPUESTAS_NIVEL_3 = {
    "correcta": "✅ CORRECTO\nNi yo la sabía!!!",
    "incorrecta": "❌ INCORRECTO\nTe entiendo la verdad"
}

RESPUESTA_CORRECTA_ERA = "\n💡 La respuesta correcta era: {}"

# =============================================================================
# MENSAJES DE OBJETOS ESPECIALES
# =============================================================================

FELICITACIONES_OBJETO = "\n🌟 ¡FELICIDADES! Has logrado un rendimiento excepcional."
ELIGE_OBJETO = "\nHas obtenido una recompensa EXCEPCIONAL de Esfinge:\nElige tu objeto:"

MENSAJE_ESPADA = """⚔️ ¡Has obtenido la ESPADA DE LA ESFINGE!
   • +2 puntos extra por respuesta correcta
   • Un reintento especial disponible"""

MENSAJE_ARMADURA = """🛡️ ¡Has obtenido la ARMADURA DE LA ESFINGE!
   • Protección automática contra una respuesta incorrecta"""

MENSAJE_RACIONES = """🍖 ¡Has obtenido las RACIONES DE LA ESFINGE!
   • Recupera 3 puntos de vida cuando falles una pregunta"""

MENSAJE_BOLSA_MONEDAS = """💰 ¡Has obtenido la BOLSA DE MONEDAS DE LA ESFINGE!
   • Duplica los puntos de la última pregunta correcta"""

# =============================================================================
# MENSAJES DE MINIJUEGO
# =============================================================================

MINIJUEGO_TITULO = "\n=== GUARDIANES DE PIEDRA ==="
MINIJUEGO_OBJETIVO = "Objetivo: Llegar desde (0,0) hasta la esquina inferior derecha"
MINIJUEGO_REGLA = "Regla: Solo puedes moverte a casillas con valores MAYORES al actual"
MINIJUEGO_LEYENDA = "Leyenda: [XX] = Tu posición, XX* = Camino recorrido\n"
MINIJUEGO_MATRIZ_GENERADA = "Matriz con solución garantizada generada!\n"
MINIJUEGO_VICTORIA = "\n🎉 ¡FELICITACIONES! 🎉\n¡Has liberado correctamente a los guardianes!\nObtienes una mejora especial para tu aventura."
MINIJUEGO_DERROTA = "\n¡No hay movimientos válidos! Has quedado atrapado.\nLos guardianes permanecen petrificados..."
MINIJUEGO_SALIENDO = "Saliendo del juego..."
MINIJUEGO_REINICIANDO = "Reiniciando juego..."

# =============================================================================
# MENSAJES DE ERRORES
# =============================================================================

OPCION_INVALIDA = "❌ Opción inválida."
OPCION_INVALIDA_MENU = "❌ Opción inválida. Intenta de nuevo."
ERROR_SIN_ESTADISTICAS = "No hay estadísticas guardadas"
ERROR_CARGA_ESTADISTICAS = "Error al cargar estadísticas"
ERROR_USUARIO_NO_ENCONTRADO = "Usuario '{}' no encontrado"
ERROR_SIN_PREGUNTAS_NIVEL = "❌ No hay preguntas disponibles para el nivel {}"
ERROR_SIN_PREGUNTAS_DISPONIBLES = "❌ No hay más preguntas disponibles para el nivel {}"

# =============================================================================
# MENSAJES DE PARTIDA
# =============================================================================

INICIANDO_PARTIDA = "\n{}\n🎮 INICIANDO PARTIDA\n{}"
NIVEL_INICIADO = "\n🎯 === NIVEL {} === 🎯\nResponderás {} preguntas de este nivel"
FIN_PARTIDA_ERRORES = "\n❌ Has fallado 2 veces. Fin de la partida."
