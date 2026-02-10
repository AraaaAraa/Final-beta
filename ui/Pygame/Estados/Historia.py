# =============================================================================
# ESTADO HISTORIA
# =============================================================================
# Pantalla que muestra la historia del juego con transiciones
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton
from ..efectos import dibujar_degradado_vertical, dibujar_sombra_texto
from ..recursos import cargar_imagen


class historia(BaseEstado):
    """
    Estado de la historia del juego.
    
    Muestra información sobre el juego con transiciones entre pantallas.
    Al finalizar solicita el nombre del jugador y pasa al menú.
    """
    
    def __init__(self):
        """Inicializa el estado de historia."""
        super(historia, self).__init__()
        self.sig_estado = "Menu"
        
        # Cargar fondo
        ancho, alto = self.screen_rect.size
        self.fondo = cargar_imagen("cueva.png", escalar=(ancho, alto))
        
        # Colores
        self.color_fondo_1 = (30, 20, 40)
        self.color_fondo_2 = (50, 30, 60)
        self.color_texto = (255, 255, 200)
        self.color_titulo = (255, 215, 0)
        self.color_input = (255, 255, 255)
        self.color_input_bg = (50, 50, 50)
        self.color_input_border = (200, 200, 100)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 60)
        self.fuente_texto = pygame.font.Font(None, 26)
        self.fuente_boton = pygame.font.Font(None, 32)
        self.fuente_indicacion = pygame.font.Font(None, 24)
        self.fuente_input = pygame.font.Font(None, 40)
        
        # Pantallas de la historia (separadas por bloques vacíos)
        self.pantallas = [
            [
                "Hace unos meses te capturaron cometiendo un crimen atroz",
            ],
            [
                "Como antiguo soldado pensabas que tendrían piedad...",
                "pero estabas errado",
            ],
            [
                "Tu antiguo comandante decretó que ahora debías pagar",
                "haciendo una última misión",
            ],
            [
                "Lo peor? Te dejaron a tu suerte con pocos suministros",
                "y un objetivo casi suicida",
            ],
            [
                "Ahora ya pasó una semana y el mapa que conseguiste",
                "te guió a una gran cueva",
            ],
            [
                "Fuiste con toda la tranquilidad a ingresar cuando",
                "una esfinge interrumpió tu paso",
            ],
            [
                "Te dio unas instrucciones simples...",
                "tenías que responder sus preguntas y si lo hacías bien",
                "te permitiría pasar y hasta te podría dar una recompensa",
            ],
            [
                "Solo tienes dos oportunidades para equivocarte",
                "y todas las preguntas son sobre mitología",
                "griega, egipcia y hebrea",
            ],
            [
                "¿Acaso estás listo para responder correctamente?",
                "",
                "Recuerda que es de vida o muerte!",
            ]
        ]
        
        # Estado de la historia
        self.pantalla_actual = 0
        self.total_pantallas = len(self.pantallas)
        self.en_input_nombre = False  # Flag para la pantalla de input
        
        # Input de nombre
        self.nombre_jugador = ""
        self.max_caracteres = 15
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 500  # Parpadeo cada 500ms
        
        # Efecto de fade
        self.alpha_fade = 0
        self.fade_in = True
        self.fade_speed = 3  # Velocidad del fade
        
        # Rectángulo del input
        centro_x = self.screen_rect.centerx
        self.input_rect = pygame.Rect(centro_x - 200, 300, 400, 60)
        
        # Botón continuar (solo visible cuando hay nombre)
        self.boton_continuar = Boton(
            "Continuar",
            centro_x - 100,
            400,
            200,
            50,
            self.fuente_boton,
            (255, 255, 255)
        )
        
        # Botón saltar historia (visible durante las pantallas de historia)
        self.boton_saltar = Boton(
            "Saltar Historia",
            self.screen_rect.width - 220,  # Esquina superior derecha
            20,
            200,
            45,
            pygame.font.Font(None, 28),
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
        self.pantalla_actual = 0
        self.en_input_nombre = False
        self.nombre_jugador = ""
        self.alpha_fade = 0
        self.fade_in = True
        self.cursor_visible = True
        self.cursor_timer = 0
    
    def get_event(self, event: pygame.event.Event):
        """
        Procesa eventos de Pygame.
        
        Parámetros:
            event (pygame.event.Event): Evento a procesar
        """
        if event.type == pygame.QUIT:
            self.quit = True
            
        # Si estamos en la pantalla de input de nombre
        elif self.en_input_nombre:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Continuar solo si hay nombre
                    if self.nombre_jugador.strip():
                        self.finalizar_historia()
                elif event.key == pygame.K_BACKSPACE:
                    # Borrar último carácter
                    self.nombre_jugador = self.nombre_jugador[:-1]
                elif event.key == pygame.K_ESCAPE:
                    # ESC vuelve a la última pantalla de historia
                    self.en_input_nombre = False
                    self.pantalla_actual = self.total_pantallas - 1
                    self.alpha_fade = 0
                    self.fade_in = True
                else:
                    # Agregar carácter si no excede el límite
                    if len(self.nombre_jugador) < self.max_caracteres:
                        # Solo permitir letras, números y algunos caracteres
                        if event.unicode.isprintable() and event.unicode not in ['|', '\\', '/', ':']:
                            self.nombre_jugador += event.unicode
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Solo permitir clic en continuar si hay nombre
                if self.nombre_jugador.strip() and self.boton_continuar.verificar_click(pos):
                    self.finalizar_historia()
        
        # Si estamos en las pantallas de historia
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC salta a input de nombre
                    self.saltar_a_input()
                elif event.key == pygame.K_s:
                    # Tecla S también salta
                    self.saltar_a_input()
                else:
                    # Cualquier otra tecla avanza
                    self.siguiente_pantalla()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Verificar clic en botón saltar
                if self.boton_saltar.verificar_click(pos):
                    self.saltar_a_input()
                else:
                    # Clic avanza
                    self.siguiente_pantalla()
    
    def siguiente_pantalla(self):
        """Avanza a la siguiente pantalla de la historia."""
        if self.pantalla_actual < self.total_pantallas - 1:
            self.pantalla_actual += 1
            self.alpha_fade = 0
            self.fade_in = True
        else:
            # Pasar a la pantalla de input de nombre
            self.saltar_a_input()
    
    def saltar_a_input(self):
        """Salta directamente a la pantalla de input de nombre."""
        self.en_input_nombre = True
        self.alpha_fade = 0
        self.fade_in = True
    
    def finalizar_historia(self):
        """Finaliza la historia y guarda el nombre del jugador."""
        # Guardar nombre en persist para usar en todo el juego
        self.persist["nombre_jugador"] = self.nombre_jugador.strip()
        self.done = True
        self.sig_estado = "Menu"
    
    def update(self, dt: float):
        """
        Actualiza el estado de historia.
        
        Parámetros:
            dt (float): Delta time en milisegundos
        """
        # Efecto fade in
        if self.fade_in:
            self.alpha_fade = min(255, self.alpha_fade + self.fade_speed)
            if self.alpha_fade >= 255:
                self.fade_in = False
        
        # Parpadeo del cursor en input de nombre
        if self.en_input_nombre:
            self.cursor_timer += dt
            if self.cursor_timer >= self.cursor_interval:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
            
            # Actualizar hover del botón continuar
            mouse_pos = pygame.mouse.get_pos()
            self.boton_continuar.actualizar_hover(mouse_pos)
        else:
            # Actualizar hover del botón saltar
            mouse_pos = pygame.mouse.get_pos()
            self.boton_saltar.actualizar_hover(mouse_pos)
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja la historia en la superficie.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Dibujar fondo de imagen
        surface.blit(self.fondo, (0, 0))
        
        # Overlay oscuro para mejorar legibilidad
        overlay = pygame.Surface(self.screen_rect.size)
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Crear superficie para el contenido con fade
        contenido_surface = pygame.Surface(self.screen_rect.size, pygame.SRCALPHA)
        contenido_surface.set_alpha(self.alpha_fade)
        
        if self.en_input_nombre:
            # Pantalla de input de nombre
            self.draw_input_nombre(contenido_surface)
        else:
            # Pantallas de historia
            self.draw_pantalla_historia(contenido_surface)
            
            # Dibujar botón saltar (sin fade, siempre visible)
            # Lo dibujamos directamente en surface, no en contenido_surface
        
        # Dibujar superficie de contenido con fade
        surface.blit(contenido_surface, (0, 0))
        
        # Dibujar botón saltar DESPUÉS del fade (siempre visible)
        if not self.en_input_nombre:
            self.boton_saltar.draw(surface)
    
    def draw_pantalla_historia(self, surface: pygame.Surface):
        """
        Dibuja una pantalla de historia.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Título
        titulo_render = self.fuente_titulo.render("Historia", True, self.color_titulo)
        titulo_rect = titulo_render.get_rect(center=(self.screen_rect.centerx, 80))
        surface.blit(titulo_render, titulo_rect)
        
        # Líneas de la pantalla actual
        lineas = self.pantallas[self.pantalla_actual]
        y_offset = self.screen_rect.centery - (len(lineas) * 20)
        
        for linea in lineas:
            if linea:  # Solo renderizar si no es línea vacía
                texto_render = self.fuente_texto.render(linea, True, self.color_texto)
                texto_rect = texto_render.get_rect(center=(self.screen_rect.centerx, y_offset))
                surface.blit(texto_render, texto_rect)
            y_offset += 40
        
        # Indicador de progreso
        progreso_texto = f"Pantalla {self.pantalla_actual + 1} de {self.total_pantallas}"
        progreso_render = self.fuente_indicacion.render(progreso_texto, True, (150, 150, 150))
        progreso_rect = progreso_render.get_rect(bottomleft=(20, self.screen_rect.height - 20))
        surface.blit(progreso_render, progreso_rect)
        
        # Instrucción
        instruccion = "Presiona cualquier tecla o clic para continuar..."
        if self.pantalla_actual == self.total_pantallas - 1:
            instruccion = "Presiona cualquier tecla o clic para ingresar tu nombre..."
        
        instruccion_render = self.fuente_indicacion.render(instruccion, True, (200, 200, 100))
        instruccion_rect = instruccion_render.get_rect(center=(self.screen_rect.centerx, self.screen_rect.height - 50))
        surface.blit(instruccion_render, instruccion_rect)
    
    def draw_input_nombre(self, surface: pygame.Surface):
        """
        Dibuja la pantalla de input de nombre.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Título
        titulo_texto = "Ingresa tu nombre, soldado"
        dibujar_sombra_texto(
            surface,
            titulo_texto,
            self.fuente_titulo,
            self.color_titulo,
            (50, 50, 50),
            (self.screen_rect.centerx, 120),
            offset=3
        )
        
        # Instrucción
        instruccion_lineas = [
            "Este nombre se usará para guardar tu progreso",
            "y comparar tus resultados con otros jugadores"
        ]
        y_offset = 200
        for linea in instruccion_lineas:
            texto_render = self.fuente_indicacion.render(linea, True, self.color_texto)
            texto_rect = texto_render.get_rect(center=(self.screen_rect.centerx, y_offset))
            surface.blit(texto_render, texto_rect)
            y_offset += 30
        
        # Fondo del input
        pygame.draw.rect(surface, self.color_input_bg, self.input_rect, border_radius=5)
        pygame.draw.rect(surface, self.color_input_border, self.input_rect, 3, border_radius=5)
        
        # Texto del input
        texto_display = self.nombre_jugador
        if self.cursor_visible and len(self.nombre_jugador) < self.max_caracteres:
            texto_display += "|"
        
        if not self.nombre_jugador and not self.cursor_visible:
            # Placeholder
            placeholder_render = self.fuente_input.render("Escribe aquí...", True, (100, 100, 100))
            placeholder_rect = placeholder_render.get_rect(center=self.input_rect.center)
            surface.blit(placeholder_render, placeholder_rect)
        else:
            texto_render = self.fuente_input.render(texto_display, True, self.color_input)
            texto_rect = texto_render.get_rect(center=self.input_rect.center)
            surface.blit(texto_render, texto_rect)
        
        # Contador de caracteres
        contador_texto = f"{len(self.nombre_jugador)}/{self.max_caracteres}"
        contador_render = self.fuente_indicacion.render(contador_texto, True, (150, 150, 150))
        contador_rect = contador_render.get_rect(topright=(self.input_rect.right, self.input_rect.bottom + 5))
        surface.blit(contador_render, contador_rect)
        
        # Botón continuar (solo si hay nombre)
        if self.nombre_jugador.strip():
            self.boton_continuar.draw(surface)
        else:
            # Mensaje indicando que debe escribir algo
            aviso_render = self.fuente_indicacion.render(
                "Escribe un nombre para continuar", 
                True, 
                (200, 100, 100)
            )
            aviso_rect = aviso_render.get_rect(center=(self.screen_rect.centerx, 420))
            surface.blit(aviso_render, aviso_rect)
        
        # Instrucción adicional
        hint_render = self.fuente_indicacion.render(
            "Presiona ENTER o haz clic en Continuar",
            True,
            (150, 150, 150)
        )
        hint_rect = hint_render.get_rect(center=(self.screen_rect.centerx, self.screen_rect.height - 50))
        surface.blit(hint_render, hint_rect)