# =============================================================================
# UTILIDADES DE MANEJO DE EVENTOS PYGAME
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Funciones para detectar y procesar eventos de usuario en Pygame.
#    Simplifica la detección de clicks en múltiples botones.
#
# 📥 USADO EN:
#    - Estados/Menu.py - Detectar clicks en botones de menú
#    - Estados/Gameplay/gestor_respuestas.py - Detectar respuesta seleccionada
#    - Estados/Rankings.py - Detectar click en botón volver
#    - Estados/Game_Over.py - Detectar clicks en botones finales
#
# 💡 BENEFICIO:
#    Simplifica detección de clicks en múltiples botones.
#    Evita duplicar bucles de detección de eventos.
#
# 🔗 DEPENDENCIAS:
#    - pygame: Para manejo de eventos y mouse
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Abstrae lógica común de detección de eventos
#    - Usa algoritmo manual (while con contador) en lugar de enumerate
#    - Tipado explícito en todos los parámetros
#    - Un solo return por función
# =============================================================================

import pygame


def detectar_click_en_botones(evento: pygame.event.Event, 
                              botones: list) -> int:
    """
    Detecta en qué botón de una lista se hizo click.
    
    Args:
        evento (pygame.event.Event): Evento de pygame a procesar
        botones (list): Lista de objetos Boton
    
    Returns:
        int: Índice del botón clickeado, -1 si ninguno fue clickeado
    
    Usado en:
        - Menu.py - Detectar qué opción del menú fue clickeada
        - Gameplay/gestor_respuestas.py - Detectar qué opción fue seleccionada
        - Game_Over.py - Detectar si se clickeó reintentar o volver al menú
    
    Ejemplo:
        for evento in pygame.event.get():
            indice = detectar_click_en_botones(evento, lista_botones)
            if indice != -1:
                print(f"Se clickeó el botón {indice}")
    """
    indice_clickeado = -1
    
    if evento.type == pygame.MOUSEBUTTONDOWN:
        pos = evento.pos
        i = 0
        while i < len(botones):
            if botones[i].fue_clickeado(pos):
                indice_clickeado = i
                break
            i = i + 1
    
    return indice_clickeado


def obtener_posicion_mouse() -> tuple:
    """
    Obtiene posición actual del mouse.
    
    Returns:
        tuple: Posición (x, y) del mouse
    
    Usado en:
        - Menu.py (línea ~101) - Actualizar hover de botones
        - Gameplay/gestor_respuestas.py - Actualizar hover de opciones
        - Rankings.py - Actualizar hover del botón volver
    
    Ejemplo:
        pos = obtener_posicion_mouse()
        boton.actualizar(pos)
    """
    posicion = pygame.mouse.get_pos()
    return posicion
