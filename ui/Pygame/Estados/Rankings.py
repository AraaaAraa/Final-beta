# =============================================================================
# ESTADO RANKINGS
# =============================================================================
# Pantalla que muestra el ranking personal del jugador y el ranking global
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton
from ..efectos import dibujar_degradado_vertical, dibujar_sombra_texto
from ..recursos import cargar_imagen
from data.repositorio_usuarios import obtener_usuario
from data.archivos_json import cargar_json
from config.constantes import RUTA_USUARIOS


class rankings(BaseEstado):
    """
    Estado de rankings del juego.
    
    Muestra el ranking personal del jugador actual y el ranking global
    de todos los jugadores.
    """
    
    def __init__(self):
        """Inicializa el estado de rankings."""
        super(rankings, self).__init__()
        self.sig_estado = "Menu"
        
        # Cargar fondo
        ancho, alto = self.screen_rect.size
        self.fondo = cargar_imagen("pared_egipcia.webp", escalar=(ancho, alto))
        
        # Colores
        self.color_fondo_1 = (20, 30, 40)
        self.color_fondo_2 = (40, 30, 60)
        self.color_titulo = (255, 215, 0)
        self.color_subtitulo = (200, 200, 100)
        self.color_texto = (255, 255, 200)
        self.color_texto_destacado = (100, 255, 100)
        self.color_sombra = (50, 50, 50)
        self.color_header = (100, 100, 150)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 60)
        self.fuente_subtitulo = pygame.font.Font(None, 40)
        self.fuente_texto = pygame.font.Font(None, 24)
        self.fuente_boton = pygame.font.Font(None, 32)
        
        # Tabs (Personal / Global)
        self.tab_actual = "personal"  # "personal" o "global"
        
        # Datos de rankings
        self.ranking_personal = []
        self.ranking_global = []
        self.nombre_jugador = ""
        
        # Botones
        centro_x = self.screen_rect.centerx
        
        self.boton_personal = Boton(
            "Personal",
            centro_x - 260,
            100,
            120,
            40,
            self.fuente_boton,
            (255, 255, 255)
        )
        
        self.boton_global = Boton(
            "Global",
            centro_x - 130,
            100,
            120,
            40,
            self.fuente_boton,
            (255, 255, 255)
        )
        
        self.boton_volver = Boton(
            "Volver",
            centro_x + 60,
            100,
            120,
            40,
            self.fuente_boton,
            (255, 255, 255)
        )
    
    def startup(self, persist: dict):
        """
        Inicializa el estado al comenzar.
        
        Parámetros:
            persist (dict): Datos persistentes entre estados
        """
        self.persist = persist
        self.done = False
        
        # Obtener nombre del jugador
        self.nombre_jugador = persist.get("nombre_jugador", "Invitado")
        
        # Cargar rankings
        self.cargar_rankings()
    
    def cargar_rankings(self):
        """Carga los datos de rankings personal y global."""
        # Cargar datos de usuario actual
        usuario = obtener_usuario(self.nombre_jugador, RUTA_USUARIOS)
        
        if "error" not in usuario:
            # Ranking personal (últimas partidas del jugador)
            self.ranking_personal = self.obtener_ranking_personal(usuario)
        else:
            self.ranking_personal = []
        
        # Ranking global (mejores jugadores)
        self.ranking_global = self.obtener_ranking_global()
    
    def obtener_ranking_personal(self, usuario: dict) -> list:
        """
        Obtiene el ranking personal del jugador.
        
        Parámetros:
            usuario (dict): Datos del usuario
        
        Retorna:
            list: Lista de partidas ordenadas por puntaje
        """
        ranking = []
        
        # Verificar que existan los datos necesarios
        if "puntajes" in usuario and "porcentajes" in usuario and "aciertos" in usuario:
            total_partidas = len(usuario["puntajes"])
            
            for i in range(total_partidas):
                partida = {
                    "numero": i + 1,
                    "puntaje": usuario["puntajes"][i],
                    "aciertos": usuario["aciertos"][i],
                    "porcentaje": usuario["porcentajes"][i],
                    "total_preguntas": usuario.get("total_preguntas", [10])[i] if i < len(usuario.get("total_preguntas", [10])) else 10
                }
                ranking.append(partida)
            
            # Ordenar por puntaje descendente
            ranking.sort(key=lambda x: x["puntaje"], reverse=True)
        
        return ranking
    
    def obtener_ranking_global(self) -> list:
        """
        Obtiene el ranking global de todos los jugadores.
        
        Retorna:
            list: Lista de jugadores ordenados por mejor puntaje
        """
        ranking = []
        
        # Cargar todos los usuarios
        datos = cargar_json(RUTA_USUARIOS, {})
        
        for nombre, usuario in datos.items():
            if "puntajes" in usuario and usuario["puntajes"]:
                # Obtener el mejor puntaje del jugador
                mejor_puntaje = max(usuario["puntajes"])
                idx_mejor = usuario["puntajes"].index(mejor_puntaje)
                
                mejor_porcentaje = usuario.get("porcentajes", [0])[idx_mejor] if idx_mejor < len(usuario.get("porcentajes", [0])) else 0
                mejor_aciertos = usuario.get("aciertos", [0])[idx_mejor] if idx_mejor < len(usuario.get("aciertos", [0])) else 0
                total_partidas = len(usuario["puntajes"])
                
                jugador = {
                    "nombre": nombre,
                    "mejor_puntaje": mejor_puntaje,
                    "mejor_porcentaje": mejor_porcentaje,
                    "mejor_aciertos": mejor_aciertos,
                    "total_partidas": total_partidas
                }
                ranking.append(jugador)
        
        # Ordenar por mejor puntaje descendente
        ranking.sort(key=lambda x: x["mejor_puntaje"], reverse=True)
        
        return ranking
    
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
            
            if self.boton_personal.verificar_click(pos):
                self.tab_actual = "personal"
            elif self.boton_global.verificar_click(pos):
                self.tab_actual = "global"
            elif self.boton_volver.verificar_click(pos):
                self.done = True
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
        self.boton_personal.actualizar_hover(mouse_pos)
        self.boton_global.actualizar_hover(mouse_pos)
        self.boton_volver.actualizar_hover(mouse_pos)
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja los rankings en la superficie.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Dibujar fondo de imagen
        surface.blit(self.fondo, (0, 0))
        
        # Overlay oscuro para mejorar legibilidad
        overlay = pygame.Surface(self.screen_rect.size)
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Título principal
        dibujar_sombra_texto(
            surface,
            "RANKINGS",
            self.fuente_titulo,
            self.color_titulo,
            self.color_sombra,
            (self.screen_rect.centerx, 40),
            offset=3
        )
        
        # Marcar botón activo como "siempre hover" (botón oscuro)
        # Resetear hover primero
        self.boton_personal.hover = False
        self.boton_global.hover = False
        
        # Luego activar el hover del tab actual
        if self.tab_actual == "personal":
            self.boton_personal.hover = True
        else:
            self.boton_global.hover = True
        
        # Dibujar botones
        self.boton_personal.draw(surface)
        self.boton_global.draw(surface)
        self.boton_volver.draw(surface)
        
        # Dibujar ranking según tab activo
        if self.tab_actual == "personal":
            self.draw_ranking_personal(surface)
        else:
            self.draw_ranking_global(surface)
    
    def draw_ranking_personal(self, surface: pygame.Surface):
        """
        Dibuja el ranking personal del jugador.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Subtítulo
        subtitulo = f"Ranking Personal - {self.nombre_jugador}"
        subtitulo_render = self.fuente_subtitulo.render(subtitulo, True, self.color_subtitulo)
        subtitulo_rect = subtitulo_render.get_rect(center=(self.screen_rect.centerx, 170))
        surface.blit(subtitulo_render, subtitulo_rect)
        
        if not self.ranking_personal:
            # No hay datos
            mensaje = "Aún no has jugado ninguna partida"
            mensaje_render = self.fuente_texto.render(mensaje, True, self.color_texto)
            mensaje_rect = mensaje_render.get_rect(center=(self.screen_rect.centerx, 300))
            surface.blit(mensaje_render, mensaje_rect)
            return
        
        # Headers de la tabla
        y_start = 220
        headers = ["#", "Partida", "Puntaje", "Aciertos", "Porcentaje"]
        x_positions = [100, 200, 350, 500, 640]
        
        for i, header in enumerate(headers):
            header_render = self.fuente_texto.render(header, True, self.color_header)
            surface.blit(header_render, (x_positions[i], y_start))
        
        # Línea separadora
        pygame.draw.line(surface, self.color_header, (80, y_start + 30), (720, y_start + 30), 2)
        
        # Mostrar top 10 partidas
        y_offset = y_start + 45
        max_mostrar = min(10, len(self.ranking_personal))
        
        for i in range(max_mostrar):
            partida = self.ranking_personal[i]
            
            # Determinar color (destacar top 3)
            if i < 3:
                color = self.color_texto_destacado
            else:
                color = self.color_texto
            
            # Renderizar datos
            datos = [
                str(i + 1),
                f"#{partida['numero']}",
                str(partida['puntaje']),
                f"{partida['aciertos']}/{partida['total_preguntas']}",
                f"{partida['porcentaje']:.1f}%"
            ]
            
            for j, dato in enumerate(datos):
                dato_render = self.fuente_texto.render(dato, True, color)
                surface.blit(dato_render, (x_positions[j], y_offset))
            
            y_offset += 30
    
    def draw_ranking_global(self, surface: pygame.Surface):
        """
        Dibuja el ranking global de jugadores.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Subtítulo
        subtitulo = "Ranking Global - Mejores Jugadores"
        subtitulo_render = self.fuente_subtitulo.render(subtitulo, True, self.color_subtitulo)
        subtitulo_rect = subtitulo_render.get_rect(center=(self.screen_rect.centerx, 170))
        surface.blit(subtitulo_render, subtitulo_rect)
        
        if not self.ranking_global:
            # No hay datos
            mensaje = "No hay datos de jugadores aún"
            mensaje_render = self.fuente_texto.render(mensaje, True, self.color_texto)
            mensaje_rect = mensaje_render.get_rect(center=(self.screen_rect.centerx, 300))
            surface.blit(mensaje_render, mensaje_rect)
            return
        
        # Headers de la tabla
        y_start = 220
        headers = ["#", "Jugador", "Mejor Puntaje", "Aciertos", "Partidas"]
        x_positions = [100, 200, 380, 530, 660]
        
        for i, header in enumerate(headers):
            header_render = self.fuente_texto.render(header, True, self.color_header)
            surface.blit(header_render, (x_positions[i], y_start))
        
        # Línea separadora
        pygame.draw.line(surface, self.color_header, (80, y_start + 30), (720, y_start + 30), 2)
        
        # Mostrar top 10 jugadores
        y_offset = y_start + 45
        max_mostrar = min(10, len(self.ranking_global))
        
        for i in range(max_mostrar):
            jugador = self.ranking_global[i]
            
            # Determinar color (destacar top 3 y jugador actual)
            if jugador["nombre"] == self.nombre_jugador:
                color = (255, 255, 100)  # Amarillo para jugador actual
            elif i < 3:
                color = self.color_texto_destacado
            else:
                color = self.color_texto
            
            # Renderizar datos
            nombre_truncado = jugador["nombre"][:15] if len(jugador["nombre"]) > 15 else jugador["nombre"]
            
            datos = [
                str(i + 1),
                nombre_truncado,
                str(jugador["mejor_puntaje"]),
                str(jugador["mejor_aciertos"]),
                str(jugador["total_partidas"])
            ]
            
            for j, dato in enumerate(datos):
                dato_render = self.fuente_texto.render(dato, True, color)
                surface.blit(dato_render, (x_positions[j], y_offset))
            
            y_offset += 30