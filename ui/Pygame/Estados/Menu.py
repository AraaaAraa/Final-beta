# =============================================================================
# ESTADO MENU
# =============================================================================
# Menú principal del juego
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton, crear_botones_centrados
from ..efectos import dibujar_degradado_vertical
from ..recursos import cargar_imagen, cargar_fuente_principal  # ⬅️ IMPORT AGREGADO


class menu(BaseEstado):
    """
    Estado del menú principal.
    
    Presenta las opciones principales del juego y maneja
    la navegación hacia otros estados.
    """
    
    def __init__(self):
        """Inicializa el estado del menú."""
        super(menu, self).__init__()
        self.sig_estado = "Gameplay"
        
        # Cargar fondo
        ancho, alto = self.screen_rect.size
        self.fondo = cargar_imagen("FondoDesertico.png", escalar=(ancho, alto))
        
        # Colores
        self.color_fondo_1 = (20, 30, 50)
        self.color_fondo_2 = (50, 30, 80)
        self.color_titulo = (255, 215, 0)
        
        # ⬅️ FUENTES CON JACQUARD12
        self.fuente_titulo = cargar_fuente_principal(80)
        self.fuente_boton = cargar_fuente_principal(48)
        
        # Crear botones usando helper (SIN "Historia")
        centro_x = self.screen_rect.centerx
        botones_lista = crear_botones_centrados(
            ["Jugar", "Rankings", "Minijuego", "Salir"],
            centro_x,
            self.fuente_boton,
            tamano="grande",
            y_inicial=250
        )
        
        self.boton_jugar = botones_lista[0]
        self.boton_rankings = botones_lista[1]
        self.boton_minijuego = botones_lista[2]
        self.boton_salir = botones_lista[3]
        
        self.botones = botones_lista
    
    def startup(self, persist: dict):
        """
        Inicializa el estado al comenzar.
        
        Parámetros:
            persist (dict): Datos persistentes entre estados
        """
        self.persist = persist
        self.done = False
    
    def get_event(self, event: pygame.event.Event):
        """
        Procesa eventos de Pygame.
        
        Parámetros:
            event (pygame.event.Event): Evento a procesar
        """
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Verificar clics en orden inverso
            for boton in reversed(self.botones):
                if boton == self.boton_salir and boton.verificar_click(pos):
                    self.quit = True
                    break
                elif boton == self.boton_minijuego and boton.verificar_click(pos):
                    self.sig_estado = "Minijuego"
                    self.done = True
                    break
                elif boton == self.boton_rankings and boton.verificar_click(pos):
                    self.sig_estado = "Rankings"
                    self.done = True
                    break
                elif boton == self.boton_jugar and boton.verificar_click(pos):
                    self.sig_estado = "Gameplay"
                    self.done = True
                    break
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit = True
    
    def update(self, dt: float):
        """
        Actualiza el estado del menú.
        
        Parámetros:
            dt (float): Delta time en milisegundos
        """
        # Actualizar hover de los botones
        mouse_pos = pygame.mouse.get_pos()
        for boton in self.botones:
            boton.hover = False
        
        for boton in reversed(self.botones):
            if boton.rect.collidepoint(mouse_pos):
                boton.hover = True
                break
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja el menú en la superficie.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Dibujar fondo de imagen
        surface.blit(self.fondo, (0, 0))
        
        # Overlay semi-transparente
        overlay = pygame.Surface(self.screen_rect.size)
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Título
        titulo = "Las preguntas de la esfingue "
        titulo_render = self.fuente_titulo.render(titulo, True, self.color_titulo)
        titulo_rect = titulo_render.get_rect(center=(self.screen_rect.centerx, 120))
        surface.blit(titulo_render, titulo_rect)
        
        # Botones
        for boton in self.botones:
            boton.draw(surface)