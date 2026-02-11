# =============================================================================
# ESTADO RANKINGS
# =============================================================================
# Pantalla que muestra el ranking de jugadores
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton, crear_botones_centrados
from ..efectos import dibujar_degradado_vertical
from ..recursos import cargar_imagen, cargar_fuente_principal
from data.repositorio_usuarios import obtener_ranking
from config.constantes import RUTA_USUARIOS


class rankings(BaseEstado):
    """
    Estado de Rankings.
    
    Muestra la tabla de clasificación de los mejores jugadores
    ordenados por puntaje.
    """
    
    def __init__(self):
        """Inicializa el estado de rankings."""
        super(rankings, self).__init__()
        self.sig_estado = "Menu"
        
        # Cargar fondo
        ancho, alto = self.screen_rect.size
        self.fondo = cargar_imagen("pared_egipcia.webp", escalar=(ancho, alto))
        
        # Colores
        self.color_fondo_1 = (20, 30, 50)
        self.color_fondo_2 = (50, 30, 80)
        self.color_titulo = (255, 215, 0)
        self.color_texto = (255, 255, 255)
        self.color_oro = (255, 215, 0)
        self.color_plata = (192, 192, 192)
        self.color_bronce = (205, 127, 50)
        
        # Fuentes con Jacquard12
        self.fuente_titulo = cargar_fuente_principal(70)
        self.fuente_ranking = cargar_fuente_principal(32)
        self.fuente_boton = cargar_fuente_principal(40)
        
        # Datos del ranking
        self.ranking_data = []
        
        # Botón volver usando helper
        centro_x = self.screen_rect.centerx
        botones_lista = crear_botones_centrados(
            ["Volver"],
            centro_x,
            self.fuente_boton,
            tamano="grande",
            y_inicial=600
        )
        
        self.boton_volver = botones_lista[0]
        self.botones = botones_lista
    
    def startup(self, persist: dict):
        """
        Inicializa el estado al comenzar.
        
        Parámetros:
            persist (dict): Datos persistentes entre estados
        """
        self.persist = persist
        self.done = False
        
        # Cargar ranking
        self.ranking_data = obtener_ranking(RUTA_USUARIOS)
        
        # Limitar a top 10
        if len(self.ranking_data) > 10:
            self.ranking_data = self.ranking_data[:10]
    
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
            if self.boton_volver.verificar_click(pos):
                self.sig_estado = "Menu"
                self.done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.sig_estado = "Menu"
                self.done = True
    
    def update(self, dt: float):
        """
        Actualiza el estado de rankings.
        
        Parámetros:
            dt (float): Delta time en milisegundos
        """
        # Actualizar hover del botón
        mouse_pos = pygame.mouse.get_pos()
        self.boton_volver.hover = self.boton_volver.rect.collidepoint(mouse_pos)
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja la pantalla de rankings.
        
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
        
        # Título
        titulo = "RANKINGS"
        titulo_render = self.fuente_titulo.render(titulo, True, self.color_titulo)
        titulo_rect = titulo_render.get_rect(center=(self.screen_rect.centerx, 60))
        surface.blit(titulo_render, titulo_rect)
        
        # Fondo semi-transparente para el ranking
        ranking_bg_width = 600
        ranking_bg_height = 450
        ranking_bg_x = (self.screen_rect.width - ranking_bg_width) // 2
        ranking_bg_y = 130
        
        ranking_bg = pygame.Surface((ranking_bg_width, ranking_bg_height))
        ranking_bg.set_alpha(150)
        ranking_bg.fill((30, 30, 50))
        surface.blit(ranking_bg, (ranking_bg_x, ranking_bg_y))
        
        # Borde del fondo
        pygame.draw.rect(surface, self.color_titulo, 
                        (ranking_bg_x, ranking_bg_y, ranking_bg_width, ranking_bg_height), 3)
        
        # Mostrar ranking
        if self.ranking_data:
            y_offset = ranking_bg_y + 30
            
            for i, jugador in enumerate(self.ranking_data):
                # Determinar color según posición
                if i == 0:
                    color = self.color_oro
                    medalla = "1."
                elif i == 1:
                    color = self.color_plata
                    medalla = "2."
                elif i == 2:
                    color = self.color_bronce
                    medalla = "3."
                else:
                    color = self.color_texto
                    medalla = f"{i + 1}."
                
                # Formatear texto
                nombre = jugador.get("nombre", "Desconocido")
                mejor_puntaje = jugador.get("mejor_puntaje", 0)
                promedio = jugador.get("promedio_puntaje", 0)
                
                texto = f"{medalla} {nombre} - Mejor: {mejor_puntaje} pts (Prom: {promedio:.1f})"
                
                # Renderizar
                texto_render = self.fuente_ranking.render(texto, True, color)
                texto_rect = texto_render.get_rect(center=(self.screen_rect.centerx, y_offset))
                surface.blit(texto_render, texto_rect)
                
                y_offset += 40
        else:
            # No hay datos
            no_data_text = "No hay rankings disponibles"
            no_data_render = self.fuente_ranking.render(no_data_text, True, self.color_texto)
            no_data_rect = no_data_render.get_rect(center=(self.screen_rect.centerx, 300))
            surface.blit(no_data_render, no_data_rect)
        
        # Botón volver
        self.boton_volver.draw(surface)