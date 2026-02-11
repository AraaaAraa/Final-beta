# =============================================================================
# ESTADO MINIJUEGO
# =============================================================================
# Minijuego "Guardianes de Piedra"
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton, crear_botones_centrados
from ..recursos import cargar_imagen, cargar_fuente_principal
from core.logica_minijuego import (
    generar_matriz_resoluble,  # ⬅️ CAMBIADO
    obtener_movimientos_validos,
    verificar_victoria  # ⬅️ ESTE SÍ EXISTE
)
from config.constantes import ANCHO, ALTO, TAMAÑO_MATRIZ_MINIJUEGO


class minijuego(BaseEstado):
    """
    Estado del minijuego "Guardianes de Piedra".
    
    El jugador debe moverse por una matriz desde (0,0) hasta
    la esquina inferior derecha, solo pudiendo moverse a casillas
    con valores mayores.
    """
    
    def __init__(self):
        """Inicializa el estado del minijuego."""
        super(minijuego, self).__init__()
        self.sig_estado = "Menu"
        
        # Cargar fondo
        ancho, alto = self.screen_rect.size
        self.fondo = cargar_imagen("cueva.png", escalar=(ancho, alto))
        
        # Colores
        self.color_fondo = (20, 30, 50)
        self.color_celda = (100, 100, 150)
        self.color_celda_actual = (255, 215, 0)
        self.color_celda_visitada = (150, 150, 200)
        self.color_celda_valida = (100, 255, 100)
        self.color_texto = (255, 255, 255)
        self.color_texto_celda = (0, 0, 0)
        
        # Fuentes con Jacquard12
        self.fuente_titulo = cargar_fuente_principal(50)
        self.fuente_celda = cargar_fuente_principal(28)
        self.fuente_instrucciones = cargar_fuente_principal(24)
        self.fuente_boton = cargar_fuente_principal(32)
        
        # Estado del juego
        self.matriz = None
        self.pos_actual = (0, 0)
        self.camino_recorrido = [(0, 0)]
        self.movimientos_validos = []
        self.terminado = False
        self.victoria = False
        self.tamano_celda = 80
        self.margen = 5
        
        # Bandera para mostrar pantalla de derrota
        self.mostrar_derrota = False
        
        # Botones para las pantallas de resultado usando helper
        centro_x = self.screen_rect.centerx
        botones_lista = crear_botones_centrados(
            ["Reintentar", "Menu Principal"],
            centro_x,
            self.fuente_boton,
            tamano="pequeno",
            y_inicial=500
        )
        
        self.boton_reintentar = botones_lista[0]
        self.boton_menu = botones_lista[1]
        self.botones_resultado = botones_lista
    
    def startup(self, persist: dict):
        """
        Inicializa el estado al comenzar.
        
        Parámetros:
            persist (dict): Datos persistentes entre estados
        """
        self.persist = persist
        self.done = False
        
        # Iniciar nuevo juego
        self.iniciar_nuevo_juego()
    
    def iniciar_nuevo_juego(self):
        """Inicia un nuevo juego del minijuego."""
        # ⬅️ GENERAR MATRIZ
        self.matriz = generar_matriz_resoluble(TAMAÑO_MATRIZ_MINIJUEGO)
        self.pos_actual = (0, 0)
        self.camino_recorrido = [(0, 0)]
        self.terminado = False
        self.victoria = False
        self.mostrar_derrota = False
        
        # ⬅️ OBTENER MOVIMIENTOS VÁLIDOS (necesita matriz, pos, valor)
        valor_actual = self.matriz[0][0]
        self.movimientos_validos = obtener_movimientos_validos(
            self.matriz, 
            self.pos_actual, 
            valor_actual
        )
        
        print("🎮 Minijuego iniciado")
        print(f"📍 Posición inicial: {self.pos_actual}")
    
    def get_event(self, event: pygame.event.Event):
        """
        Procesa eventos de Pygame.
        
        Parámetros:
            event (pygame.event.Event): Evento a procesar
        """
        if event.type == pygame.QUIT:
            self.quit = True
        
        # Si está en pantalla de victoria o derrota
        if self.terminado or self.mostrar_derrota:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for boton in reversed(self.botones_resultado):
                    if boton == self.boton_menu and boton.verificar_click(pos):
                        self.sig_estado = "Menu"
                        self.done = True
                        break
                    elif boton == self.boton_reintentar and boton.verificar_click(pos):
                        self.iniciar_nuevo_juego()
                        break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.sig_estado = "Menu"
                    self.done = True
                elif event.key == pygame.K_RETURN:
                    self.iniciar_nuevo_juego()
        else:
            # Juego en curso
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.procesar_click(pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.sig_estado = "Menu"
                    self.done = True
    
    def procesar_click(self, pos: tuple):
        """
        Procesa un clic en la matriz.
        
        Parámetros:
            pos (tuple): Posición (x, y) del clic
        """
        if self.terminado:
            return
        
        # Calcular posición de la matriz según el clic
        inicio_x = (ANCHO - (self.tamano_celda * TAMAÑO_MATRIZ_MINIJUEGO + self.margen * (TAMAÑO_MATRIZ_MINIJUEGO - 1))) // 2
        inicio_y = 150
        
        x_rel = pos[0] - inicio_x
        y_rel = pos[1] - inicio_y
        
        if x_rel < 0 or y_rel < 0:
            return
        
        col = x_rel // (self.tamano_celda + self.margen)
        fila = y_rel // (self.tamano_celda + self.margen)
        
        if col >= TAMAÑO_MATRIZ_MINIJUEGO or fila >= TAMAÑO_MATRIZ_MINIJUEGO:
            return
        
        nueva_pos = (fila, col)
        
        # Verificar si es un movimiento válido (buscar en la lista)
        es_valido = False
        for mov in self.movimientos_validos:
            if (mov[0], mov[1]) == nueva_pos:
                es_valido = True
                break
        
        if es_valido:
            # Realizar movimiento
            self.pos_actual = nueva_pos
            self.camino_recorrido.append(nueva_pos)
            
            # ⬅️ VERIFICAR VICTORIA (recibe pos y tamaño)
            if verificar_victoria(self.pos_actual, TAMAÑO_MATRIZ_MINIJUEGO):
                print("🎉 ¡Victoria!")
                self.terminado = True
                self.victoria = True
            else:
                # Actualizar movimientos válidos
                valor_actual = self.matriz[self.pos_actual[0]][self.pos_actual[1]]
                self.movimientos_validos = obtener_movimientos_validos(
                    self.matriz,
                    self.pos_actual,
                    valor_actual
                )
                
                # Verificar si no hay movimientos (derrota)
                if not self.movimientos_validos:
                    print("😢 Derrota - No hay movimientos válidos")
                    self.mostrar_derrota = True
    
    def update(self, dt: float):
        """
        Actualiza el estado del minijuego.
        
        Parámetros:
            dt (float): Delta time en milisegundos
        """
        # Actualizar hover de botones de resultado
        if self.terminado or self.mostrar_derrota:
            mouse_pos = pygame.mouse.get_pos()
            for boton in self.botones_resultado:
                boton.hover = False
            
            for boton in reversed(self.botones_resultado):
                if boton.rect.collidepoint(mouse_pos):
                    boton.hover = True
                    break
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja el minijuego en la superficie.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Dibujar fondo
        surface.blit(self.fondo, (0, 0))
        
        # Overlay semi-transparente
        overlay = pygame.Surface(self.screen_rect.size)
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Título
        titulo = "GUARDIANES DE PIEDRA"
        titulo_render = self.fuente_titulo.render(titulo, True, (255, 215, 0))
        titulo_rect = titulo_render.get_rect(center=(self.screen_rect.centerx, 50))
        surface.blit(titulo_render, titulo_rect)
        
        # Instrucciones
        if not self.terminado:
            instruccion = "Muevete solo a casillas con valores MAYORES"
            inst_render = self.fuente_instrucciones.render(instruccion, True, self.color_texto)
            inst_rect = inst_render.get_rect(center=(self.screen_rect.centerx, 100))
            surface.blit(inst_render, inst_rect)
        
        # Dibujar matriz
        if self.matriz:
            self.dibujar_matriz(surface)
        
        # Pantalla de victoria
        if self.terminado and self.victoria:
            self.dibujar_resultado_victoria(surface)
        
        # Pantalla de derrota
        if self.mostrar_derrota:
            self.dibujar_resultado_derrota(surface)
    
    def dibujar_matriz(self, surface: pygame.Surface):
        """Dibuja la matriz del juego."""
        if not self.matriz:
            return
        
        # Centrar la matriz
        inicio_x = (ANCHO - (self.tamano_celda * TAMAÑO_MATRIZ_MINIJUEGO + self.margen * (TAMAÑO_MATRIZ_MINIJUEGO - 1))) // 2
        inicio_y = 150
        
        for fila in range(TAMAÑO_MATRIZ_MINIJUEGO):
            for col in range(TAMAÑO_MATRIZ_MINIJUEGO):
                x = inicio_x + col * (self.tamano_celda + self.margen)
                y = inicio_y + fila * (self.tamano_celda + self.margen)
                
                pos = (fila, col)
                
                # Determinar color de la celda
                if pos == self.pos_actual:
                    color = self.color_celda_actual
                elif pos in self.camino_recorrido:
                    color = self.color_celda_visitada
                else:
                    # Verificar si es movimiento válido
                    es_valido = False
                    for mov in self.movimientos_validos:
                        if (mov[0], mov[1]) == pos:
                            es_valido = True
                            break
                    color = self.color_celda_valida if es_valido else self.color_celda
                
                # Dibujar celda
                pygame.draw.rect(surface, color, (x, y, self.tamano_celda, self.tamano_celda))
                pygame.draw.rect(surface, (255, 255, 255), (x, y, self.tamano_celda, self.tamano_celda), 2)
                
                # Dibujar valor
                valor = str(self.matriz[fila][col])
                valor_render = self.fuente_celda.render(valor, True, self.color_texto_celda)
                valor_rect = valor_render.get_rect(center=(x + self.tamano_celda // 2, y + self.tamano_celda // 2))
                surface.blit(valor_render, valor_rect)
    
    def dibujar_resultado_victoria(self, surface: pygame.Surface):
        """Dibuja la pantalla de victoria."""
        # Overlay semi-transparente oscuro
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Mensaje de victoria
        mensaje = "VICTORIA!"
        color = (100, 255, 100)
        
        mensaje_render = self.fuente_titulo.render(mensaje, True, color)
        mensaje_rect = mensaje_render.get_rect(center=(self.screen_rect.centerx, 200))
        surface.blit(mensaje_render, mensaje_rect)
        
        # Mensaje de felicitaciones
        felicitaciones = "Has completado el minijuego!"
        felicitaciones_render = self.fuente_instrucciones.render(felicitaciones, True, (200, 200, 200))
        felicitaciones_rect = felicitaciones_render.get_rect(center=(self.screen_rect.centerx, 280))
        surface.blit(felicitaciones_render, felicitaciones_rect)
        
        # Botones
        for boton in self.botones_resultado:
            boton.draw(surface)
    
    def dibujar_resultado_derrota(self, surface: pygame.Surface):
        """Dibuja la pantalla de derrota."""
        # Overlay semi-transparente oscuro (igual que victoria)
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Mensaje de derrota (en rojo)
        mensaje = "DERROTA!"
        color = (255, 100, 100)
        
        mensaje_render = self.fuente_titulo.render(mensaje, True, color)
        mensaje_rect = mensaje_render.get_rect(center=(self.screen_rect.centerx, 200))
        surface.blit(mensaje_render, mensaje_rect)
        
        # Mensaje de ánimo
        mensaje_animo = "No hay movimientos validos. Intentalo de nuevo!"
        animo_render = self.fuente_instrucciones.render(mensaje_animo, True, (200, 200, 200))
        animo_rect = animo_render.get_rect(center=(self.screen_rect.centerx, 280))
        surface.blit(animo_render, animo_rect)
        
        # Botones
        for boton in self.botones_resultado:
            boton.draw(surface)