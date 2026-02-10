# =============================================================================
# CLASE BOTON
# =============================================================================
# Clase para crear y gestionar botones interactivos en Pygame
# =============================================================================

import pygame
from .recursos import cargar_imagen


class Boton:
    """
    Clase para crear botones interactivos con imágenes.
    
    Soporta hover (cambio de imagen al pasar el mouse) y detección de clics.
    """
    
    def __init__(self, texto: str, x: int, y: int, ancho: int, alto: int, fuente: pygame.font.Font, color_texto: tuple = (255, 255, 255)):
        """
        Inicializa un botón.
        
        Parámetros:
            texto (str): Texto del botón
            x (int): Posición X
            y (int): Posición Y
            ancho (int): Ancho del botón
            alto (int): Alto del botón
            fuente (pygame.font.Font): Fuente para el texto
            color_texto (tuple): Color del texto (RGB)
        """
        self.texto = texto
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.fuente = fuente
        self.color_texto = color_texto
        
        # Cargar imágenes de botón
        self.imagen_normal = cargar_imagen("BotonNormal.png", escalar=(ancho, alto))
        self.imagen_hover = cargar_imagen("BotonOscuro.png", escalar=(ancho, alto))
        
        # Estado del botón
        self.hover = False
        self.activo = True
        
    def verificar_click(self, pos: tuple) -> bool:
        """
        Verifica si se hizo clic en el botón.
        
        Parámetros:
            pos (tuple): Posición del clic (x, y)
        
        Retorna:
            bool: True si se hizo clic en el botón
        """
        if self.activo and self.rect.collidepoint(pos):
            return True
        return False
    
    def actualizar_hover(self, pos: tuple):
        """
        Actualiza el estado hover del botón según la posición del mouse.
        
        Parámetros:
            pos (tuple): Posición del mouse (x, y)
        """
        if self.activo and self.rect.collidepoint(pos):
            self.hover = True
        else:
            self.hover = False
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja el botón en la superficie.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Seleccionar imagen según estado
        if self.hover or not self.activo:
            imagen = self.imagen_hover
        else:
            imagen = self.imagen_normal
        
        # Dibujar imagen del botón
        surface.blit(imagen, self.rect.topleft)
        
        # Dibujar texto centrado
        texto_render = self.fuente.render(self.texto, True, self.color_texto)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        
        # Si el botón está inactivo, hacer el texto más oscuro
        if not self.activo:
            # Crear una superficie semi-transparente
            texto_surface = pygame.Surface(texto_render.get_size(), pygame.SRCALPHA)
            texto_surface.blit(texto_render, (0, 0))
            texto_surface.set_alpha(128)
            surface.blit(texto_surface, texto_rect)
        else:
            surface.blit(texto_render, texto_rect)
    
    def set_activo(self, activo: bool):
        """
        Establece si el botón está activo o no.
        
        Parámetros:
            activo (bool): True si el botón debe estar activo
        """
        self.activo = activo