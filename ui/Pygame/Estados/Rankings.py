# =============================================================================
# ESTADO RANKINGS
# =============================================================================
# Pantalla que muestra los rankings de jugadores
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton, crear_botones_centrados
from ..efectos import dibujar_degradado_vertical, dibujar_sombra_texto
from ..recursos import cargar_imagen
from models.usuario import obtener_ranking_global, obtener_estadisticas_usuario


class rankings(BaseEstado):
    """
    Estado de Rankings.
    
    Muestra dos tabs:
    - Personal: Estadísticas del jugador actual
    - Global: Top 10 de todos los jugadores
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
        self.color_fondo_2 = (40, 50, 80)
        self.color_titulo = (255, 215, 0)
        self.color_sombra = (50, 50, 50)
        self.color_texto = (255, 255, 255)
        self.color_fila_par = (60, 70, 100)
        self.color_fila_impar = (50, 60, 90)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 70)
        self.fuente_tab = pygame.font.Font(None, 32)
        self.fuente_tabla = pygame.font.Font(None, 28)
        self.fuente_boton = pygame.font.Font(None, 32)
        
        # Tab actual
        self.tab_actual = "personal"  # "personal" o "global"
        
        # Botones de tabs (más pequeños, en la parte superior)
        centro_x = self.screen_rect.centerx
        
        # Botones de tabs (personalizados, no usar helper porque tienen posición especial)
        self.boton_personal = Boton(
            "Personal",
            centro_x - 250,
            100,
            120,
            40,
            self.fuente_tab,
            (255, 255, 255)
        )
        
        self.boton_global = Boton(
            "Global",
            centro_x - 130,
            100,
            120,
            40,
            self.fuente_tab,
            (255, 255, 255)
        )
        
        self.boton_volver = Boton(
            "Volver",
            centro_x + 60,
            100,
            120,
            40,
            self.fuente_tab,
            (255, 255, 255)
        )
        
        self.botones = [self.boton_personal, self.boton_global, self.boton_volver]
    
    def startup(self, persist: dict):
        """
        Inicializa el estado al comenzar.
        
        Parámetros:
            persist (dict): Datos persistentes entre estados
        """
        self.persist = persist
        self.done = False
    
    def obtener_datos_personal(self):
        """Obtiene las estadísticas personales del jugador actual."""
        nombre_jugador = self.persist.get("nombre_jugador", "Invitado")
        stats = obtener_estadisticas_usuario(nombre_jugador)
        
        if stats:
            return {
                "nombre": stats["nombre"],
                "puntos_totales": stats["puntos_totales"],
                "partidas_jugadas": stats["partidas_jugadas"],
                "respuestas_correctas": stats["respuestas_correctas"],
                "respuestas_totales": stats["respuestas_totales"],
                "promedio": stats["promedio_puntos"]
            }
        else:
            return {
                "nombre": nombre_jugador,
                "puntos_totales": 0,
                "partidas_jugadas": 0,
                "respuestas_correctas": 0,
                "respuestas_totales": 0,
                "promedio": 0
            }
    
    def obtener_datos_global(self):
        """Obtiene el ranking global de los mejores jugadores."""
        return obtener_ranking_global(limite=10)
    
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
                if boton == self.boton_volver and boton.verificar_click(pos):
                    self.done = True
                    break
                elif boton == self.boton_global and boton.verificar_click(pos):
                    self.tab_actual = "global"
                    break
                elif boton == self.boton_personal and boton.verificar_click(pos):
                    self.tab_actual = "personal"
                    break
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.done = True
            elif event.key == pygame.K_1:
                self.tab_actual = "personal"
            elif event.key == pygame.K_2:
                self.tab_actual = "global"
    
    def update(self, dt: float):
        """
        Actualiza el estado de rankings.
        
        Parámetros:
            dt (float): Delta time en milisegundos
        """
        # Actualizar hover de todos los botones
        mouse_pos = pygame.mouse.get_pos()
        for boton in self.botones:
            boton.hover = False
        
        for boton in reversed(self.botones):
            if boton.rect.collidepoint(mouse_pos):
                boton.hover = True
                break
    
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
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Título
        titulo = "RANKINGS"
        dibujar_sombra_texto(
            surface,
            titulo,
            self.fuente_titulo,
            self.color_titulo,
            self.color_sombra,
            (self.screen_rect.centerx, 50),
            offset=4
        )
        
        # Botones de tabs
        for boton in self.botones:
            boton.draw(surface)
        
        # Contenido según tab actual
        if self.tab_actual == "personal":
            self.dibujar_personal(surface)
        else:
            self.dibujar_global(surface)
    
    def dibujar_personal(self, surface: pygame.Surface):
        """Dibuja las estadísticas personales del jugador."""
        datos = self.obtener_datos_personal()
        
        # Título del tab
        tab_titulo = f"Estadísticas de {datos['nombre']}"
        tab_render = self.fuente_tab.render(tab_titulo, True, (200, 220, 255))
        tab_rect = tab_render.get_rect(center=(self.screen_rect.centerx, 180))
        surface.blit(tab_render, tab_rect)
        
        # Estadísticas
        stats = [
            f"Puntos totales: {datos['puntos_totales']}",
            f"Partidas jugadas: {datos['partidas_jugadas']}",
            f"Respuestas correctas: {datos['respuestas_correctas']}/{datos['respuestas_totales']}",
            f"Promedio por partida: {datos['promedio']:.1f} puntos"
        ]
        
        y_offset = 250
        for stat in stats:
            # Fondo de la fila
            fila_rect = pygame.Rect(150, y_offset - 20, 500, 50)
            pygame.draw.rect(surface, self.color_fila_par, fila_rect, 0, 10)
            pygame.draw.rect(surface, (100, 120, 150), fila_rect, 2, 10)
            
            # Texto
            stat_render = self.fuente_tabla.render(stat, True, self.color_texto)
            stat_rect = stat_render.get_rect(center=(self.screen_rect.centerx, y_offset))
            surface.blit(stat_render, stat_rect)
            y_offset += 70
    
    def dibujar_global(self, surface: pygame.Surface):
        """Dibuja el ranking global de mejores jugadores."""
        ranking = self.obtener_datos_global()
        
        # Título del tab
        tab_titulo = "Top 10 Mejores Jugadores"
        tab_render = self.fuente_tab.render(tab_titulo, True, (200, 220, 255))
        tab_rect = tab_render.get_rect(center=(self.screen_rect.centerx, 180))
        surface.blit(tab_render, tab_rect)
        
        # Encabezado de tabla
        y_offset = 230
        headers = ["#", "Jugador", "Puntos", "Promedio"]
        x_positions = [180, 280, 480, 600]
        
        for i, header in enumerate(headers):
            header_render = self.fuente_tabla.render(header, True, (255, 215, 0))
            header_rect = header_render.get_rect(left=x_positions[i], centery=y_offset)
            surface.blit(header_render, header_rect)
        
        y_offset += 40
        
        # Ranking
        if not ranking:
            no_datos = "No hay datos de jugadores aún"
            no_datos_render = self.fuente_tabla.render(no_datos, True, (150, 150, 150))
            no_datos_rect = no_datos_render.get_rect(center=(self.screen_rect.centerx, y_offset + 50))
            surface.blit(no_datos_render, no_datos_rect)
        else:
            for i, jugador in enumerate(ranking[:10]):  # Mostrar solo top 10
                # Fondo de la fila
                color_fila = self.color_fila_par if i % 2 == 0 else self.color_fila_impar
                fila_rect = pygame.Rect(150, y_offset - 15, 500, 40)
                pygame.draw.rect(surface, color_fila, fila_rect, 0, 5)
                
                # Datos
                puesto = str(i + 1)
                nombre = jugador["nombre"]
                puntos = str(jugador["puntos_totales"])
                promedio = f"{jugador['promedio_puntos']:.1f}"
                
                datos = [puesto, nombre, puntos, promedio]
                
                for j, dato in enumerate(datos):
                    # Color especial para el top 3
                    if i == 0:
                        color = (255, 215, 0)  # Oro
                    elif i == 1:
                        color = (192, 192, 192)  # Plata
                    elif i == 2:
                        color = (205, 127, 50)  # Bronce
                    else:
                        color = self.color_texto
                    
                    dato_render = self.fuente_tabla.render(dato, True, color)
                    dato_rect = dato_render.get_rect(left=x_positions[j], centery=y_offset)
                    surface.blit(dato_render, dato_rect)
                
                y_offset += 45