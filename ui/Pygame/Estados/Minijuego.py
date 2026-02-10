# =============================================================================
# ESTADO MINIJUEGO
# =============================================================================
# Minijuego "Guardianes de Piedra"
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton
from ..efectos import dibujar_degradado_vertical
from ..recursos import cargar_imagen
from core.logica_minijuego import (
    inicializar_estado_minijuego,
    obtener_movimientos_validos,
    validar_movimiento,
    procesar_movimiento_minijuego
)


class minijuego(BaseEstado):
    """
    Estado del minijuego "Guardianes de Piedra".
    
    El jugador debe navegar una matriz de números, moviéndose solo
    a celdas con valores mayores hasta llegar a la esquina inferior derecha.
    """
    
    def __init__(self):
        """Inicializa el estado del minijuego."""
        super(minijuego, self).__init__()
        self.sig_estado = "Menu"
        
        # Cargar fondo
        ancho, alto = self.screen_rect.size
        self.fondo = cargar_imagen("FondoDesertico.png", escalar=(ancho, alto))
        
        # Colores
        self.color_fondo_1 = (30, 40, 50)
        self.color_fondo_2 = (50, 60, 80)
        self.color_celda = (70, 70, 90)
        self.color_celda_jugador = (100, 200, 100)
        self.color_celda_objetivo = (255, 215, 0)
        self.color_celda_visitada = (90, 90, 110)
        self.color_celda_movimiento = (150, 150, 200)
        self.color_texto = (255, 255, 255)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 50)
        self.fuente_celda = pygame.font.Font(None, 28)
        self.fuente_instrucciones = pygame.font.Font(None, 24)
        self.fuente_boton = pygame.font.Font(None, 32)
        
        # Estado del juego
        self.estado_juego = None
        self.movimientos_validos = []
        self.tamano_celda = 80
        self.margen = 5
        
        # Botones para la pantalla de victoria
        centro_x = self.screen_rect.centerx
        self.boton_reintentar = Boton(
            "Reintentar",
            centro_x - 150,
            350,
            300,
            60,
            self.fuente_boton,
            (255, 255, 255)
        )
        self.boton_menu = Boton(
            "Menú Principal",
            centro_x - 150,
            430,
            300,
            60,
            self.fuente_boton,
            (255, 255, 255)
        )
        
        self.botones = [self.boton_reintentar, self.boton_menu]
    
    def startup(self, persist: dict):
        """
        Inicializa el estado al comenzar.
        
        Parámetros:
            persist (dict): Datos persistentes entre estados
        """
        self.persist = persist
        self.done = False
        
        # Inicializar juego
        self.estado_juego = inicializar_estado_minijuego()
        self.actualizar_movimientos_validos()
    
    def actualizar_movimientos_validos(self):
        """Actualiza la lista de movimientos válidos."""
        if self.estado_juego:
            self.movimientos_validos = obtener_movimientos_validos(
                self.estado_juego["matriz"],
                self.estado_juego["jugador_pos"],
                self.estado_juego["valor_actual"]
            )
            
            # Verificar si no hay movimientos válidos y el juego no ha terminado
            if len(self.movimientos_validos) == 0 and not self.estado_juego["terminado"]:
                # Marcar el juego como terminado y como derrota
                self.estado_juego["terminado"] = True
                self.estado_juego["victoria"] = False
    
    def procesar_click_celda(self, fila: int, col: int):
        """
        Procesa el click en una celda.
        
        Parámetros:
            fila (int): Fila de la celda
            col (int): Columna de la celda
        """
        # Verificar si la celda clickeada es un movimiento válido
        for i, mov in enumerate(self.movimientos_validos):
            if mov[0] == fila and mov[1] == col:
                # Movimiento válido
                nueva_pos = (fila, col)
                self.estado_juego = procesar_movimiento_minijuego(
                    self.estado_juego,
                    nueva_pos
                )
                
                if not self.estado_juego["terminado"]:
                    self.actualizar_movimientos_validos()
                else:
                    # Si el juego terminó, verificar si fue victoria o derrota
                    if not self.estado_juego["victoria"]:
                        # Ir a Game Over
                        self.ir_a_game_over()
                break
    
    def ir_a_game_over(self):
        """Cambia al estado de Game Over cuando se pierde el minijuego."""
        # Preparar datos para Game Over
        self.persist["puntos_totales"] = 0
        self.persist["respuestas_correctas"] = 0
        self.persist["total_preguntas"] = 1
        self.sig_estado = "Gameover"
        self.done = True
    
    def get_event(self, event: pygame.event.Event):
        """
        Procesa eventos de Pygame.
        
        Parámetros:
            event (pygame.event.Event): Evento a procesar
        """
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.done = True
            elif self.estado_juego and self.estado_juego["terminado"]:
                # Si ganó, mostrar opciones con teclas
                if self.estado_juego["victoria"]:
                    if event.key == pygame.K_r:
                        # Reintentar
                        self.estado_juego = inicializar_estado_minijuego()
                        self.actualizar_movimientos_validos()
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_m:
                        # Volver al menú
                        self.done = True
                # Si perdió, ya fue al Game Over automáticamente
            elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                # Navegación con números
                num = event.key - pygame.K_1 + 1
                if num <= len(self.movimientos_validos):
                    mov = self.movimientos_validos[num - 1]
                    self.procesar_click_celda(mov[0], mov[1])
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Si el juego terminó con victoria, verificar clics en botones
            if self.estado_juego and self.estado_juego["terminado"] and self.estado_juego["victoria"]:
                if self.boton_reintentar.verificar_click(pos):
                    # Reintentar
                    self.estado_juego = inicializar_estado_minijuego()
                    self.actualizar_movimientos_validos()
                elif self.boton_menu.verificar_click(pos):
                    # Volver al menú
                    self.done = True
            # Si el juego no ha terminado, procesar clics en celdas
            elif not self.estado_juego["terminado"]:
                # Calcular qué celda se clickeó
                offset_x = (self.screen_rect.width - (self.estado_juego["tamano"] * (self.tamano_celda + self.margen))) // 2
                offset_y = 150
                
                col = (pos[0] - offset_x) // (self.tamano_celda + self.margen)
                fila = (pos[1] - offset_y) // (self.tamano_celda + self.margen)
                
                if 0 <= fila < self.estado_juego["tamano"] and 0 <= col < self.estado_juego["tamano"]:
                    self.procesar_click_celda(fila, col)
    
    def update(self, dt: float):
        """
        Actualiza el estado del minijuego.
        
        Parámetros:
            dt (float): Delta time en milisegundos
        """
        # Actualizar hover de los botones si el juego terminó con victoria
        if self.estado_juego and self.estado_juego["terminado"] and self.estado_juego["victoria"]:
            mouse_pos = pygame.mouse.get_pos()
            for boton in self.botones:
                boton.actualizar_hover(mouse_pos)
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja el minijuego en la superficie.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Dibujar fondo de imagen
        surface.blit(self.fondo, (0, 0))
        
        # Overlay semi-transparente
        overlay = pygame.Surface(self.screen_rect.size)
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Título
        titulo_text = "Guardianes de Piedra"
        titulo_render = self.fuente_titulo.render(titulo_text, True, (255, 215, 0))
        titulo_rect = titulo_render.get_rect(center=(self.screen_rect.centerx, 40))
        surface.blit(titulo_render, titulo_rect)
        
        # Instrucciones
        if not self.estado_juego["terminado"]:
            inst_text = "Mueve a celdas con números mayores. Llega a la esquina dorada."
            inst_render = self.fuente_instrucciones.render(inst_text, True, self.color_texto)
            inst_rect = inst_render.get_rect(center=(self.screen_rect.centerx, 90))
            surface.blit(inst_render, inst_rect)
            
            # Mostrar cantidad de movimientos válidos
            mov_text = f"Movimientos disponibles: {len(self.movimientos_validos)}"
            mov_render = self.fuente_instrucciones.render(mov_text, True, (200, 200, 100))
            mov_rect = mov_render.get_rect(center=(self.screen_rect.centerx, 115))
            surface.blit(mov_render, mov_rect)
        
        # Matriz
        if self.estado_juego:
            self.dibujar_matriz(surface)
        
        # Resultado (solo si ganó)
        if self.estado_juego and self.estado_juego["terminado"] and self.estado_juego["victoria"]:
            self.dibujar_resultado(surface)
    
    def dibujar_matriz(self, surface: pygame.Surface):
        """Dibuja la matriz del juego."""
        tamano = self.estado_juego["tamano"]
        matriz = self.estado_juego["matriz"]
        jugador_pos = self.estado_juego["jugador_pos"]
        objetivo = self.estado_juego["objetivo"]
        visitadas = self.estado_juego["camino_recorrido"]
        
        # Calcular offset para centrar la matriz
        offset_x = (self.screen_rect.width - (tamano * (self.tamano_celda + self.margen))) // 2
        offset_y = 150
        
        for fila in range(tamano):
            for col in range(tamano):
                x = offset_x + col * (self.tamano_celda + self.margen)
                y = offset_y + fila * (self.tamano_celda + self.margen)
                
                # Determinar color de la celda
                if (fila, col) == jugador_pos:
                    color = self.color_celda_jugador
                elif (fila, col) == objetivo:
                    color = self.color_celda_objetivo
                elif (fila, col) in visitadas:
                    color = self.color_celda_visitada
                else:
                    # Verificar si es movimiento válido
                    es_movimiento_valido = False
                    for mov in self.movimientos_validos:
                        if mov[0] == fila and mov[1] == col:
                            es_movimiento_valido = True
                            break
                    
                    color = self.color_celda_movimiento if es_movimiento_valido else self.color_celda
                
                # Dibujar celda
                rect = pygame.Rect(x, y, self.tamano_celda, self.tamano_celda)
                pygame.draw.rect(surface, color, rect, 0, 5)
                pygame.draw.rect(surface, (100, 100, 100), rect, 2, 5)
                
                # Dibujar valor
                valor = matriz[fila][col]
                valor_text = str(valor)
                valor_render = self.fuente_celda.render(valor_text, True, self.color_texto)
                valor_rect = valor_render.get_rect(center=(x + self.tamano_celda // 2, y + self.tamano_celda // 2))
                surface.blit(valor_render, valor_rect)
    
    def dibujar_resultado(self, surface: pygame.Surface):
        """Dibuja el resultado del juego cuando se gana."""
        # Overlay semi-transparente
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Mensaje de victoria
        mensaje = "¡VICTORIA!"
        color = (100, 255, 100)
        
        mensaje_render = self.fuente_titulo.render(mensaje, True, color)
        mensaje_rect = mensaje_render.get_rect(center=(self.screen_rect.centerx, 200))
        surface.blit(mensaje_render, mensaje_rect)
        
        # Mensaje de felicitaciones
        felicitaciones = "¡Has completado el minijuego!"
        felicitaciones_render = self.fuente_instrucciones.render(felicitaciones, True, (200, 200, 200))
        felicitaciones_rect = felicitaciones_render.get_rect(center=(self.screen_rect.centerx, 270))
        surface.blit(felicitaciones_render, felicitaciones_rect)
        
        # Botones
        for boton in self.botones:
            boton.draw(surface)
        
        # Instrucciones de teclas
        inst_text = "R: Reintentar  |  M: Menú  |  ESC: Salir"
        inst_render = self.fuente_instrucciones.render(inst_text, True, (150, 150, 150))
        inst_rect = inst_render.get_rect(center=(self.screen_rect.centerx, 520))
        surface.blit(inst_render, inst_rect)