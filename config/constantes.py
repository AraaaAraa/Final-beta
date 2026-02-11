# =============================================================================
# CONFIGURACIÓN DEL JUEGO - CONSTANTES
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Centraliza todas las constantes y configuraciones del juego de trivia
#    de mitología. Incluye rutas de archivos, configuración de niveles,
#    dificultades, sistema de buffeos, objetos especiales, minijuegos,
#    límites de errores y configuración de Pygame.
#
# 📥 IMPORTADO EN:
#    - core/logica_juego.py (línea 29) - para PREGUNTAS_POR_NIVEL, MAX_ERRORES_PERMITIDOS, RUTA_PREGUNTAS, RUTA_USUARIOS
#    - core/logica_buffeos.py (línea ~7) - para RACHA_BUFFEO_MINIMA, PUNTOS_BUFFEO_POR_RACHA, OBJETOS_ESPECIALES, RUTA_ESTADO_BUFF
#    - core/logica_puntaje.py (línea ~4) - para PUNTOS_POR_DIFICULTAD
#    - core/logica_minijuego.py (línea ~5) - para TAMAÑO_MATRIZ_MINIJUEGO
#    - data/repositorio_usuarios.py (línea ~6) - para RUTA_USUARIOS
#    - data/repositorio_preguntas.py (línea ~6) - para RUTA_PREGUNTAS
#    - ui/Pygame/Estados/Gameplay.py (línea 9, 23) - para ALTO, ANCHO, PREGUNTAS_POR_NIVEL, MAX_ERRORES_PERMITIDOS, RUTA_PREGUNTAS
#    - ui/Pygame/main.py - para ANCHO, ALTO, FPS
#    - ui/Pygame/Juego.py - para FPS, ANCHO, ALTO
#    - ui/Pygame/Estados/*.py - para dimensiones y constantes de UI
#
# 🔗 DEPENDENCIAS:
#    - os: para manejo de rutas de archivos
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Centralización de configuración facilita mantenimiento y escalabilidad
#    - Separación clara entre constantes de lógica (PREGUNTAS_POR_NIVEL) 
#      y de UI (ANCHO, ALTO, FPS)
#    - Sistema de buffeos configurable permite balancear dificultad del juego
#    - Uso de diccionarios para configuración permite extensibilidad
# =============================================================================

import os
# =============================================================================
# RUTAS DE ARCHIVOS
# =============================================================================
# Descripción: Rutas a los archivos de datos del juego
# Uso en Pygame: Se mantienen iguales, solo cambia la ubicación relativa
# =============================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_USUARIOS = os.path.join(BASE_DIR, "assets", "Usuarios.json")
RUTA_PREGUNTAS = os.path.join(BASE_DIR, "assets", "preguntas.csv")
RUTA_ESTADO_BUFF = os.path.join(BASE_DIR, "assets", "EstadoBuff.json")

# =============================================================================
# CONFIGURACIÓN DE NIVELES
# =============================================================================
# Descripción: Cantidad de preguntas por nivel
# Uso en Pygame: Se usa igual, pero la UI mostrará progreso gráfico
# =============================================================================

PREGUNTAS_POR_NIVEL = {
    1: 5,  # Nivel 1: 5 preguntas
    2: 3,  # Nivel 2: 3 preguntas
    3: 2   # Nivel 3: 2 preguntas
}

# =============================================================================
# CONFIGURACIÓN DE DIFICULTAD
# =============================================================================
# Descripción: Puntos otorgados según dificultad de la pregunta
# Uso en Pygame: Se usa igual para calcular puntajes
# =============================================================================

PUNTOS_POR_DIFICULTAD = {
    1: 1,   # Nivel fácil: 1 punto
    2: 2,   # Nivel medio: 2 puntos
    3: 3    # Nivel difícil: 3 puntos
}

# =============================================================================
# CONFIGURACIÓN DE BUFFEOS
# =============================================================================
# Descripción: Rachas mínimas para activar buffeos de puntos extra
# Uso en Pygame: Se usa igual, pero con efectos visuales
# =============================================================================

RACHA_BUFFEO_MINIMA = {
    "nivel_1": 3,  # +1 punto desde racha 3
    "nivel_2": 5,  # +3 puntos desde racha 5
    "nivel_3": 7   # +5 puntos desde racha 7
}

# Puntos extra por nivel de racha
PUNTOS_BUFFEO_POR_RACHA = {
    3: 1,  # Racha > 3: +1 punto
    5: 3,  # Racha > 5: +3 puntos
    7: 5   # Racha > 7: +5 puntos
}

# =============================================================================
# OBJETOS ESPECIALES
# =============================================================================
# Descripción: Configuración de objetos especiales/buffs del juego
# Uso en Pygame: Mismo comportamiento, con iconos gráficos
# =============================================================================

OBJETOS_ESPECIALES = {
    "espada": {
        "nombre": "Espada de la Esfinge",
        "puntos_extra": 2,
        "permite_reintento": True,
        "descripcion": "+2 puntos extra por respuesta correcta y un reintento especial disponible"
    },
    "armadura": {
        "nombre": "Armadura de la Esfinge",
        "proteccion_auto": True,
        "descripcion": "Protección automática contra una respuesta incorrecta"
    },
    "raciones": {
        "nombre": "Raciones de la Esfinge",
        "recuperacion_vida": 3,
        "descripcion": "Recupera 3 puntos de vida cuando falles una pregunta"
    },
    "bolsa_monedas": {
        "nombre": "Bolsa de Monedas",
        "duplica_puntos": True,
        "descripcion": "Duplica los puntos de la última pregunta correcta"
    }
}

# =============================================================================
# CONFIGURACIÓN DE MINIJUEGO
# =============================================================================
# Descripción: Parámetros del minijuego "Guardianes de Piedra"
# Uso en Pygame: Mismo tamaño, pero con interfaz gráfica
# =============================================================================

TAMAÑO_MATRIZ_MINIJUEGO = 5

# =============================================================================
# CONFIGURACIÓN DE RECOMPENSAS
# =============================================================================
# Descripción: Condiciones para obtener objetos especiales
# Uso en Pygame: Se usa igual para determinar recompensas
# =============================================================================

RESPUESTAS_CORRECTAS_PARA_OBJETO = 8
TOTAL_PREGUNTAS_PARA_OBJETO = 10

# =============================================================================
# CONFIGURACIÓN DE ERRORES
# =============================================================================
# Descripción: Límite de errores antes de terminar la partida
# Uso en Pygame: Se usa igual, con animaciones de game over
# =============================================================================

MAX_ERRORES_PERMITIDOS = 2

# =============================================================================
# OPCIONES DE RESPUESTA
# =============================================================================
# Descripción: Letras para las opciones de respuesta
# Uso en Pygame: Se pueden mapear a botones o teclas
# =============================================================================

LETRAS_OPCIONES = "ABCD"

# =============================================================================
# CONFIGURACIÓN DE PYGAME GENERAL
# =============================================================================
# Descripción: Configuracion para imagenes.
# Uso en Pygame: Se usa igual, pero la UI mostrará progreso gráfico
# =============================================================================

ANCHO = 1000
ALTO = 700
FPS = 60
BLANCO = (255, 255, 255) # Colores como tuplas [7]

# =============================================================================
# SISTEMA DE VIDAS EXTRA
# =============================================================================
# Descripción: Sistema de recompensa de vidas extra por puntos
# =============================================================================

PUNTOS_POR_VIDA_EXTRA = 30  # Cada 30 puntos = 1 vida extra
MAX_VIDAS_EXTRA = 4  # Máximo de vidas extra acumulables (total: 2 base + 4 extra = 6)