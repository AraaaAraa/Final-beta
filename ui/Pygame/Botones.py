# =============================================================================
# CLASE BOTON Y CONFIGURACIÓN
# =============================================================================
# Clase para crear y gestionar botones interactivos en Pygame
# =============================================================================

import pygame
from .recursos import cargar_imagen

# =============================================================================
# CONFIGURACIÓN ESTÁNDAR DE BOTONES
# =============================================================================
BOTON_ANCHO_GRANDE = 345
BOTON_ALTO_GRANDE = 200
BOTON_ESPACIADO_GRANDE = 100
BOTON_Y_INICIAL_GRANDE = 160

BOTON_ANCHO_PEQUENO = 290
BOTON_ALTO_PEQUENO = 168
BOTON_ESPACIADO_PEQUENO = 80

BOTON_COLOR_TEXTO = (255, 255, 255)


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


# =============================================================================
# FUNCIONES HELPER PARA CREAR BOTONES
# =============================================================================

def crear_boton_menu(texto: str, centro_x: int, indice: int, fuente: pygame.font.Font, tamano: str = "grande") -> Boton:
    """
    Crea un botón con el estilo del menú principal.
    
    Parámetros:
        texto (str): Texto del botón
        centro_x (int): Posición X del centro de la pantalla
        indice (int): Índice del botón (0, 1, 2, 3, 4...)
        fuente (pygame.font.Font): Fuente para el texto
        tamano (str): "grande" o "pequeno"
    
    Retorna:
        Boton: Botón configurado
    
    Ejemplo:
        boton_jugar = crear_boton_menu("Jugar", 400, 0, fuente)
        boton_salir = crear_boton_menu("Salir", 400, 1, fuente, "pequeno")
    """
    if tamano == "grande":
        ancho = BOTON_ANCHO_GRANDE
        alto = BOTON_ALTO_GRANDE
        espaciado = BOTON_ESPACIADO_GRANDE
        y_inicial = BOTON_Y_INICIAL_GRANDE
    else:
        ancho = BOTON_ANCHO_PEQUENO
        alto = BOTON_ALTO_PEQUENO
        espaciado = BOTON_ESPACIADO_PEQUENO
        y_inicial = 350  # Posición inicial para botones pequeños
    
    x = centro_x - (ancho // 2)
    y = y_inicial + (indice * espaciado)
    
    return Boton(texto, x, y, ancho, alto, fuente, BOTON_COLOR_TEXTO)


def crear_botones_centrados(textos: list, centro_x: int, fuente: pygame.font.Font,
                            tamano: str = "pequeno", y_inicial: int = None) -> list:
    """
    Crea múltiples botones centrados verticalmente.
    
    Parámetros:
        textos (list): Lista de textos para los botones
        centro_x (int): Posición X del centro
        fuente (pygame.font.Font): Fuente para el texto
        tamano (str): "grande" o "pequeno"
        y_inicial (int): Posición Y inicial (opcional)
    
    Retorna:
        list: Lista de botones creados
    
    Ejemplo:
        botones = crear_botones_centrados(["Reintentar", "Menú"], 400, fuente)
    """
    botones = []
    
    if tamano == "grande":
        ancho = BOTON_ANCHO_GRANDE
        alto = BOTON_ALTO_GRANDE
        espaciado = BOTON_ESPACIADO_GRANDE
        y_start = y_inicial if y_inicial else BOTON_Y_INICIAL_GRANDE
    else:
        ancho = BOTON_ANCHO_PEQUENO
        alto = BOTON_ALTO_PEQUENO
        espaciado = BOTON_ESPACIADO_PEQUENO
        y_start = y_inicial if y_inicial else 350
    
    for i, texto in enumerate(textos):
        x = centro_x - (ancho // 2)
        y = y_start + (i * espaciado)
        boton = Boton(texto, x, y, ancho, alto, fuente, BOTON_COLOR_TEXTO)
        botones.append(boton)
    
    return botones