# =============================================================================
# UTILIDADES DE RENDERIZADO PYGAME
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Funciones reutilizables para renderizar elementos comunes en Pygame.
#    Centraliza lógica de renderizado para evitar duplicación de código.
#
# 📥 USADO EN:
#    - Estados/Menu.py - Renderizar título y texto
#    - Estados/Gameplay/gestor_hud.py - Renderizar puntos, nivel, racha
#    - Estados/Gameplay/gestor_preguntas.py - Renderizar preguntas
#    - Estados/Rankings.py - Renderizar tabla de ranking
#    - Estados/Game_Over.py - Renderizar mensajes finales
#
# 💡 BENEFICIO:
#    Centraliza lógica de renderizado para no repetir código.
#    Facilita mantenimiento y consistencia visual.
#
# 🔗 DEPENDENCIAS:
#    - pygame: Para renderizado de superficies y texto
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Principio DRY (Don't Repeat Yourself)
#    - Funciones puras sin efectos secundarios (solo dibujan)
#    - Tipado explícito en todos los parámetros
#    - Un solo return por función
# =============================================================================

import pygame


def renderizar_texto(pantalla: pygame.Surface, texto: str, 
                    posicion: tuple, fuente: pygame.font.Font, 
                    color: tuple) -> None:
    """
    Renderiza texto centrado en una posición.
    
    Args:
        pantalla (pygame.Surface): Superficie donde dibujar
        texto (str): Texto a mostrar
        posicion (tuple): Posición (x, y) del centro
        fuente (pygame.font.Font): Fuente a usar
        color (tuple): Color RGB del texto
    
    Returns:
        None
    
    Usado en:
        - Menu.py - Renderizar título del menú
        - Gameplay/gestor_hud.py (línea ~80) - Renderizar puntos, nivel, racha
        - Gameplay/gestor_preguntas.py (línea ~50) - Renderizar pregunta
        - Rankings.py - Renderizar nombres y puntajes
    
    Ejemplo:
        fuente = pygame.font.Font(None, 40)
        renderizar_texto(screen, "Hola Mundo", (400, 300), fuente, (255, 255, 255))
    """
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=posicion)
    pantalla.blit(superficie, rect)
    return None


def renderizar_rectangulo_con_borde(pantalla: pygame.Surface, rect: pygame.Rect,
                                    color_fondo: tuple, color_borde: tuple,
                                    grosor_borde: int = 3) -> None:
    """
    Renderiza rectángulo con borde.
    
    Args:
        pantalla (pygame.Surface): Superficie donde dibujar
        rect (pygame.Rect): Rectángulo a dibujar
        color_fondo (tuple): Color RGB del fondo
        color_borde (tuple): Color RGB del borde
        grosor_borde (int): Grosor del borde en píxeles (por defecto 3)
    
    Returns:
        None
    
    Usado en:
        - Rankings.py - Dibujar paneles de ranking
        - Gameplay.py - Dibujar paneles informativos
    
    Ejemplo:
        rect = pygame.Rect(100, 100, 200, 150)
        renderizar_rectangulo_con_borde(
            screen, rect, (50, 50, 50), (255, 255, 0), 5
        )
    """
    pygame.draw.rect(pantalla, color_fondo, rect)
    pygame.draw.rect(pantalla, color_borde, rect, grosor_borde)
    return None


def limpiar_pantalla(pantalla: pygame.Surface, color: tuple) -> None:
    """
    Limpia la pantalla con un color sólido.
    
    Args:
        pantalla (pygame.Surface): Superficie a limpiar
        color (tuple): Color RGB de fondo
    
    Returns:
        None
    
    Usado en:
        - Menu.py (línea ~118) - Limpiar antes de renderizar
        - Gameplay/gameplay.py - Limpiar en cada frame
        - Rankings.py - Limpiar pantalla de rankings
    
    Ejemplo:
        limpiar_pantalla(screen, (0, 0, 0))  # Fondo negro
    """
    pantalla.fill(color)
    return None
