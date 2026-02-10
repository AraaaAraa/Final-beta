# =============================================================================
# ESTADO MENU
# =============================================================================
# Pantalla del menú principal del juego
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton, crear_boton_menu
from ..efectos import dibujar_degradado_vertical, dibujar_sombra_texto
from ..recursos import cargar_imagen


class menu(BaseEstado):
    """
    Estado del menú principal.
    
    Ofrece opciones para:
    - Jugar
    - Ver Historia
    - Rankings
    - Minijuego
    - Salir
    """
    
    def __init__(self):
        """Inicializa el estado del menú."""
        super(menu, self).__init__()
        self.sig_estado = "Gameplay"
        
        # Cargar imagen de fondo
        ancho, alto = self.screen_rect.size
        self.fondo = cargar_imagen("pared_egipcia.webp", escalar=(ancho, alto))
        
        # Colores
        self.color_fondo_1 = (20, 20, 50)
        self.color_fondo_2 = (50, 20, 70)
        self.color_titulo = (255, 215, 0)
        self.color_sombra = (50, 50, 50)
        self.color_nombre = (100, 255, 100)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 90)
        self.fuente_boton = pygame.font.Font(None, 50)
        self.fuente_nombre = pygame.font.Font(None, 32)
        
        # Título
        self.titulo = "Que desea hacer soldado?"
        
        # Configuración de botones usando helpers
        centro_x = self.screen_rect.centerx
        
        self.boton_jugar = crear_boton_menu("Jugar", centro_x, 0, self.fuente_boton)
        self.boton_historia = crear_boton_menu("Historia", centro_x, 1, self.fuente_boton)
        self.boton_rankings = crear_boton_menu("Rankings", centro_x, 2, self.fuente_boton)
        self.boton_minijuego = crear_boton_menu("Minijuego", centro_x, 3, self.fuente_boton)
        self.boton_salir = crear_boton_menu("Salir", centro_x, 4, self.fuente_boton)
        
        # Lista de todos los botones para facilitar el hover
        self.botones = [
            self.boton_jugar,
            self.boton_historia,
            self.boton_rankings,
            self.boton_minijuego,
            self.boton_salir
        ]
    
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
            
            # VERIFICAR EN ORDEN INVERSO (de abajo hacia arriba)
            # Así el botón "encima" tiene prioridad sobre los que están "debajo"
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
                elif boton == self.boton_historia and boton.verificar_click(pos):
                    self.sig_estado = "Historia"
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
            dt (float): Tiempo delta desde el último frame
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # PRIMERO: Resetear hover de todos los botones
        for boton in self.botones:
            boton.hover = False
        
        # SEGUNDO: Verificar hover en orden INVERSO (de abajo hacia arriba)
        # Así el botón que está "encima" visualmente tiene prioridad
        for boton in reversed(self.botones):
            if boton.rect.collidepoint(mouse_pos):
                boton.hover = True
                break  # IMPORTANTE: Solo activar hover del primer botón encontrado
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja el menú en la superficie.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Dibujar fondo de imagen
        surface.blit(self.fondo, (0, 0))
        
        # Overlay semi-transparente para mejorar legibilidad
        overlay = pygame.Surface(self.screen_rect.size)
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Título con sombra
        pos_titulo = (self.screen_rect.centerx, 120)
        dibujar_sombra_texto(
            surface, 
            self.titulo, 
            self.fuente_titulo,
            self.color_titulo,
            self.color_sombra,
            pos_titulo,
            offset=5
        )
        
        # Mostrar nombre del jugador
        nombre_jugador = self.persist.get("nombre_jugador", "Invitado")
        nombre_texto = f"Jugador: {nombre_jugador}"
        nombre_render = self.fuente_nombre.render(nombre_texto, True, self.color_nombre)
        nombre_rect = nombre_render.get_rect(topright=(self.screen_rect.width - 30, 30))
        surface.blit(nombre_render, nombre_rect)
        
        # Botones
        for boton in self.botones:
            boton.draw(surface)