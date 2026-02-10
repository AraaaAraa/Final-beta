# =============================================================================
# ESTADO GAME OVER
# =============================================================================
# Pantalla de fin de juego mostrando resultados
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton, crear_botones_centrados
from ..efectos import dibujar_degradado_vertical
from ..recursos import cargar_imagen
from models.usuario import guardar_usuario


class gameOver(BaseEstado):
    """
    Estado de Game Over.
    
    Muestra los resultados de la partida y permite:
    - Reintentar el juego
    - Volver al menú principal
    """
    
    def __init__(self):
        """Inicializa el estado de game over."""
        super(gameOver, self).__init__()
        self.sig_estado = "Gameplay"
        
        # Cargar fondo
        ancho, alto = self.screen_rect.size
        self.fondo = cargar_imagen("FondoDesertico.png", escalar=(ancho, alto))
        
        # Colores
        self.color_fondo_1 = (40, 20, 20)
        self.color_fondo_2 = (80, 40, 40)
        self.color_texto = (255, 255, 255)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente_stats = pygame.font.Font(None, 36)
        self.fuente_boton = pygame.font.Font(None, 32)
        
        # Botones usando helper
        centro_x = self.screen_rect.centerx
        botones_lista = crear_botones_centrados(
            ["Reintentar", "Menú Principal"],
            centro_x,
            self.fuente_boton,
            tamano="pequeno",
            y_inicial=420
        )
        
        self.boton_reintentar = botones_lista[0]
        self.boton_menu = botones_lista[1]
        self.botones = botones_lista
    
    def startup(self, persist: dict):
        """
        Inicializa el estado al comenzar.
        
        Parámetros:
            persist (dict): Datos persistentes entre estados
        """
        self.persist = persist
        self.done = False
        
        # Guardar estadísticas del usuario
        nombre_jugador = self.persist.get("nombre_jugador", "Invitado")
        puntos = self.persist.get("puntos_totales", 0)
        respuestas_correctas = self.persist.get("respuestas_correctas", 0)
        total_preguntas = self.persist.get("total_preguntas", 0)
        
        # Guardar en el archivo de usuarios
        guardar_usuario(nombre_jugador, puntos, respuestas_correctas, total_preguntas)
    
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
            
            # Verificar en orden inverso
            for boton in reversed(self.botones):
                if boton == self.boton_menu and boton.verificar_click(pos):
                    self.sig_estado = "Menu"
                    self.done = True
                    break
                elif boton == self.boton_reintentar and boton.verificar_click(pos):
                    self.sig_estado = "Gameplay"
                    self.done = True
                    break
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Reintentar con Enter
                self.sig_estado = "Gameplay"
                self.done = True
            elif event.key == pygame.K_ESCAPE:
                # Volver al menú con ESC
                self.sig_estado = "Menu"
                self.done = True
    
    def update(self, dt: float):
        """
        Actualiza el estado de game over.
        
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
        Dibuja la pantalla de game over.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Dibujar fondo de imagen
        surface.blit(self.fondo, (0, 0))
        
        # Overlay semi-transparente
        overlay = pygame.Surface(self.screen_rect.size)
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Título "GAME OVER"
        titulo = "GAME OVER"
        titulo_render = self.fuente_titulo.render(titulo, True, (255, 100, 100))
        titulo_rect = titulo_render.get_rect(center=(self.screen_rect.centerx, 150))
        surface.blit(titulo_render, titulo_rect)
        
        # Estadísticas
        puntos = self.persist.get("puntos_totales", 0)
        respuestas_correctas = self.persist.get("respuestas_correctas", 0)
        total_preguntas = self.persist.get("total_preguntas", 0)
        nombre_jugador = self.persist.get("nombre_jugador", "Invitado")
        
        stats = [
            f"Jugador: {nombre_jugador}",
            f"Puntos: {puntos}",
            f"Respuestas correctas: {respuestas_correctas}/{total_preguntas}"
        ]
        
        y_offset = 250
        for stat in stats:
            stat_render = self.fuente_stats.render(stat, True, self.color_texto)
            stat_rect = stat_render.get_rect(center=(self.screen_rect.centerx, y_offset))
            surface.blit(stat_render, stat_rect)
            y_offset += 50
        
        # Botones
        for boton in self.botones:
            boton.draw(surface)