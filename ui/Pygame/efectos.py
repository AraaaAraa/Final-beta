# =============================================================================
# MÓDULO DE EFECTOS VISUALES
# =============================================================================
# Proporciona funciones para efectos visuales en Pygame
# =============================================================================

import pygame


def dibujar_degradado_vertical(surface: pygame.Surface, color1: tuple, color2: tuple) -> None:
    """
    Dibuja un degradado vertical en una superficie.
    
    Parámetros:
        surface (pygame.Surface): Superficie donde dibujar
        color1 (tuple): Color RGB inicial (arriba)
        color2 (tuple): Color RGB final (abajo)
    """
    rect = surface.get_rect()
    for y in range(rect.height):
        ratio = y / rect.height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (rect.width, y))


def dibujar_sombra_texto(surface: pygame.Surface, texto: str, fuente: pygame.font.Font, 
                        color_texto: tuple, color_sombra: tuple, pos: tuple, offset: int = 2) -> None:
    """
    Dibuja texto con sombra.
    
    Parámetros:
        surface (pygame.Surface): Superficie donde dibujar
        texto (str): Texto a dibujar
        fuente (pygame.font.Font): Fuente a usar
        color_texto (tuple): Color RGB del texto
        color_sombra (tuple): Color RGB de la sombra
        pos (tuple): Posición (x, y) del centro del texto
        offset (int): Desplazamiento de la sombra en píxeles
    """
    # Dibujar sombra
    sombra = fuente.render(texto, True, color_sombra)
    sombra_rect = sombra.get_rect(center=(pos[0] + offset, pos[1] + offset))
    surface.blit(sombra, sombra_rect)
    
    # Dibujar texto
    texto_render = fuente.render(texto, True, color_texto)
    texto_rect = texto_render.get_rect(center=pos)
    surface.blit(texto_render, texto_rect)
