# =============================================================================
# ESTADO HISTORIA
# =============================================================================
# Pantalla que muestra la historia del juego con transiciones
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton, crear_botones_centrados, BOTON_ALTO_PEQUENO, BOTON_ANCHO_PEQUENO
from ..efectos import dibujar_degradado_vertical, dibujar_sombra_texto
from ..recursos import cargar_imagen


class historia(BaseEstado):
    """
    Estado de la historia del juego.
    
    Muestra la narrativa en pantallas secuenciales y permite
    al jugador ingresar su nombre al finalizar.
    """
    
    def __init__(self):
        """Inicializa el estado de historia."""
        super(historia, self).__init__()
        self.sig_estado = "Menu"
        
        # Cargar fondo
        ancho, alto = self.screen_rect.size
        self.fondo = cargar_imagen("Fondo_sangre.jpg", escalar=(ancho, alto))
        
        # Colores
        self.color_fondo_1 = (30, 20, 40)
        self.color_fondo_2 = (50, 40, 60)
        self.color_texto = (255, 255, 255)
        self.color_input = (255, 215, 0)
        
        # Fuentes
        self.fuente_texto = pygame.font.Font(None, 30)
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
                "en medio del desierto egipcio",
            ],
            [
                "Tu misión: adentrarte en las pirámides antiguas",
                "y recuperar los tesoros perdidos",
            ],
            [
                "Pero cuidado... las pirámides están llenas de acertijos",
                "y guardianes que pondrán a prueba tu conocimiento",
            ],
            [
                "Solo los más sabios podrán sobrevivir...",
                "¿Estás listo para enfrentar el desafío?",
            ]
        ]
        
        # Estado de la historia
        self.pantalla_actual = 0
        self.total_pantallas = len(self.pantallas)
        self.en_input_nombre = False
        self.nombre_jugador = ""
        self.max_caracteres = 20
        
        # Efectos de transición
        self.alpha_fade = 0
        self.fade_in = True
        self.velocidad_fade = 3
        
        # Botón continuar (solo para la pantalla de input)
        centro_x = self.screen_rect.centerx
        botones_lista = crear_botones_centrados(
            ["Continuar"],
            centro_x,
            self.fuente_boton,
            tamano="pequeno",
            y_inicial=400
        )
        self.boton_continuar = botones_lista[0]
        
        # Botón saltar historia (visible durante las pantallas de historia)
        self.boton_saltar = Boton(
            "Saltar Historia",
            self.screen_rect.width - 400,  # Esquina superior derecha
            20,
            BOTON_ANCHO_PEQUENO,
            BOTON_ALTO_PEQUENO,
            pygame.font.Font(None, 28),
            (255, 255, 255)
        )
        
        # Input rect para el nombre
        self.input_rect = pygame.Rect(
            centro_x - 200,
            280,
            400,
            50
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
    
    def get_event(self, event: pygame.event.Event):
        """
        Procesa eventos de Pygame.
        
        Parámetros:
            event (pygame.event.Event): Evento a procesar
        """
        if event.type == pygame.QUIT:
            self.quit = True
        
        # Si está en la pantalla de input de nombre
        if self.en_input_nombre:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.nombre_jugador.strip():
                    # Enter: continuar si hay nombre
                    self.finalizar_historia()
                elif event.key == pygame.K_BACKSPACE:
                    # Borrar último carácter
                    self.nombre_jugador = self.nombre_jugador[:-1]
                elif event.key == pygame.K_ESCAPE:
                    # Escapar: saltar historia
                    self.saltar_a_input()
                elif len(self.nombre_jugador) < self.max_caracteres:
                    # Agregar carácter si es válido
                    if event.unicode.isprintable() and event.unicode not in ['|', '\\']:
                        self.nombre_jugador += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.boton_continuar.verificar_click(pos) and self.nombre_jugador.strip():
                    self.finalizar_historia()
        
        # Si está en las pantallas de historia
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Escapar: saltar a input
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
        Actualiza el estado de la historia.
        
        Parámetros:
            dt (float): Delta time en milisegundos
        """
        # Efecto de fade in/out
        if self.fade_in:
            self.alpha_fade = min(255, self.alpha_fade + self.velocidad_fade)
            if self.alpha_fade >= 255:
                self.fade_in = False
        
        # Actualizar hover del botón continuar si está en input
        if self.en_input_nombre:
            mouse_pos = pygame.mouse.get_pos()
            self.boton_continuar.actualizar_hover(mouse_pos)
        else:
            # Actualizar hover del botón saltar
            mouse_pos = pygame.mouse.get_pos()
            self.boton_saltar.actualizar_hover(mouse_pos)
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja la pantalla de historia.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Dibujar fondo de imagen
        surface.blit(self.fondo, (0, 0))
        
        # Overlay oscuro
        overlay = pygame.Surface(self.screen_rect.size)
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Superficie de contenido para aplicar fade
        contenido_surface = pygame.Surface(self.screen_rect.size, pygame.SRCALPHA)
        contenido_surface.set_alpha(self.alpha_fade)
        
        if self.en_input_nombre:
            # Pantalla de input de nombre
            self.dibujar_input_nombre(contenido_surface)
        else:
            # Pantalla de historia
            self.dibujar_pantalla_historia(contenido_surface)
            
            # Dibujar botón saltar (sin fade, siempre visible)
            # Lo dibujamos directamente en surface, no en contenido_surface
        
        # Dibujar superficie de contenido con fade
        surface.blit(contenido_surface, (0, 0))
        
        # Dibujar botón saltar DESPUÉS del fade (siempre visible)
        if not self.en_input_nombre:
            self.boton_saltar.draw(surface)
    
    def dibujar_pantalla_historia(self, surface: pygame.Surface):
        """Dibuja una pantalla de la historia."""
        lineas = self.pantallas[self.pantalla_actual]
        
        # Centrar el bloque de texto verticalmente
        total_height = len(lineas) * 60
        y_start = (self.screen_rect.height - total_height) // 2
        
        for i, linea in enumerate(lineas):
            texto_render = self.fuente_texto.render(linea, True, self.color_texto)
            texto_rect = texto_render.get_rect(center=(self.screen_rect.centerx, y_start + i * 60))
            surface.blit(texto_render, texto_rect)
        
        # Indicación de continuar
        indicacion = "Presiona cualquier tecla o haz clic para continuar..."
        indicacion_render = self.fuente_indicacion.render(indicacion, True, (150, 150, 150))
        indicacion_rect = indicacion_render.get_rect(center=(self.screen_rect.centerx, self.screen_rect.height - 50))
        surface.blit(indicacion_render, indicacion_rect)
        
        # Indicador de progreso
        progreso = f"{self.pantalla_actual + 1}/{self.total_pantallas}"
        progreso_render = self.fuente_indicacion.render(progreso, True, (100, 100, 100))
        progreso_rect = progreso_render.get_rect(bottomright=(self.screen_rect.width - 30, self.screen_rect.height - 30))
        surface.blit(progreso_render, progreso_rect)
    
    def dibujar_input_nombre(self, surface: pygame.Surface):
        """Dibuja la pantalla de input de nombre."""
        # Título
        titulo = "¿Cuál es tu nombre, soldado?"
        titulo_render = self.fuente_texto.render(titulo, True, self.color_texto)
        titulo_rect = titulo_render.get_rect(center=(self.screen_rect.centerx, 200))
        surface.blit(titulo_render, titulo_rect)
        
        # Input box
        pygame.draw.rect(surface, (50, 50, 70), self.input_rect, 0, 10)
        pygame.draw.rect(surface, self.color_input, self.input_rect, 3, 10)
        
        # Texto del input
        if self.nombre_jugador:
            texto_display = self.nombre_jugador
        else:
            texto_display = "Escribe tu nombre..."
        
        if self.nombre_jugador:
            texto_render = self.fuente_input.render(texto_display, True, self.color_input)
            texto_rect = texto_render.get_rect(center=self.input_rect.center)
            surface.blit(texto_render, texto_rect)
        else:
            texto_render = self.fuente_input.render(texto_display, True, (100, 100, 120))
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
                (150, 150, 150)
            )
            aviso_rect = aviso_render.get_rect(center=(self.screen_rect.centerx, 450))
            surface.blit(aviso_render, aviso_rect)