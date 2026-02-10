# =============================================================================
# ESTADO GAME OVER
# =============================================================================
# Pantalla de fin de juego con resultados
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton
from ..efectos import dibujar_degradado_vertical, dibujar_sombra_texto


class gameOver(BaseEstado):
    """
    Estado de Game Over.
    
    Muestra los resultados finales y opciones para reintentar o volver al menú.
    """
    
    def __init__(self):
        """Inicializa el estado de Game Over."""
        super(gameOver, self).__init__()
        self.sig_estado = "Menu"
        
        # Colores
        self.color_fondo_1 = (60, 20, 20)
        self.color_fondo_2 = (20, 20, 60)
        self.color_titulo = (255, 100, 100)
        self.color_sombra = (50, 50, 50)
        self.color_texto = (255, 255, 200)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente_stats = pygame.font.Font(None, 36)
        self.fuente_boton = pygame.font.Font(None, 40)
        
        # Estadísticas de la partida
        self.puntos_totales = 0
        self.respuestas_correctas = 0
        self.total_preguntas = 0
        
        # Botones
        centro_x = self.screen_rect.centerx
        self.boton_reintentar = Boton(
            "Reintentar",
            centro_x - 150,
            420,
            300,
            60,
            self.fuente_boton,
            (255, 255, 255)
        )
        self.boton_menu = Boton(
            "Menú Principal",
            centro_x - 150,
            500,
            300,
            60,
            self.fuente_boton,
            (255, 255, 255)
        )
        
        # Lista de botones para facilitar hover
        self.botones = [self.boton_reintentar, self.boton_menu]
    
    def startup(self, persist: dict):
        """
        Inicializa el estado al comenzar.
        
        Parámetros:
            persist (dict): Datos persistentes entre estados
        """
        self.persist = persist
        self.done = False
        
        # Obtener estadísticas de persist
        self.puntos_totales = persist.get("puntos_totales", 0)
        self.respuestas_correctas = persist.get("respuestas_correctas", 0)
        self.total_preguntas = persist.get("total_preguntas", 0)
    
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
            if self.boton_reintentar.verificar_click(pos):
                self.sig_estado = "Gameplay"
                # Resetear persist
                self.persist = {}
                self.done = True
            elif self.boton_menu.verificar_click(pos):
                self.sig_estado = "Menu"
                self.persist = {}
                self.done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.sig_estado = "Menu"
                self.persist = {}
                self.done = True
    
    def update(self, dt: float):
        """
        Actualiza el estado de Game Over.
        
        Parámetros:
            dt (float): Delta time en milisegundos
        """
        # Actualizar hover de todos los botones
        mouse_pos = pygame.mouse.get_pos()
        for boton in self.botones:
            boton.actualizar_hover(mouse_pos)
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja la pantalla de Game Over.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Fondo con degradado
        dibujar_degradado_vertical(surface, self.color_fondo_1, self.color_fondo_2)
        
        # Título con sombra
        pos_titulo = (self.screen_rect.centerx, 100)
        dibujar_sombra_texto(
            surface,
            "GAME OVER",
            self.fuente_titulo,
            self.color_titulo,
            self.color_sombra,
            pos_titulo,
            offset=5
        )
        
        # Estadísticas
        y_offset = 220
        stats = [
            f"Puntos Totales: {self.puntos_totales}",
            f"Respuestas Correctas: {self.respuestas_correctas}/{self.total_preguntas}",
        ]
        
        for stat in stats:
            texto_render = self.fuente_stats.render(stat, True, self.color_texto)
            texto_rect = texto_render.get_rect(center=(self.screen_rect.centerx, y_offset))
            surface.blit(texto_render, texto_rect)
            y_offset += 50
        
        # Mensaje de resultado
        if self.total_preguntas > 0:
            porcentaje = (self.respuestas_correctas / self.total_preguntas) * 100
            if porcentaje >= 80:
                mensaje = "¡Excelente trabajo!"
            elif porcentaje >= 50:
                mensaje = "¡Buen esfuerzo!"
            else:
                mensaje = "¡Sigue intentándolo!"
            
            mensaje_render = self.fuente_stats.render(mensaje, True, (255, 215, 0))
            mensaje_rect = mensaje_render.get_rect(center=(self.screen_rect.centerx, y_offset + 20))
            surface.blit(mensaje_render, mensaje_rect)
        
        # Botones
        for boton in self.botones:
            boton.draw(surface)