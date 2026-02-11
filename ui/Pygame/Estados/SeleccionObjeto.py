# =============================================================================
# ESTADO SELECCIÓN DE OBJETO
# =============================================================================
# Pantalla para seleccionar objeto especial tras ganar
# =============================================================================

import pygame
from .base import BaseEstado
from ..recursos import cargar_imagen
from core.logica_buffeos import obtener_opciones_objetos, guardar_objeto_equipado
from config.constantes import ALTO, ANCHO, OBJETOS_ESPECIALES


class seleccionObjeto(BaseEstado):
    """
    Estado de selección de objeto especial.
    
    Permite al jugador elegir entre 4 objetos especiales tras
    completar la partida con éxito.
    """
    
    def __init__(self):
        """Inicializa el estado de selección de objeto."""
        super(seleccionObjeto, self).__init__()
        self.sig_estado = "Gameover"
        
        # Cargar fondo
        ancho, alto = self.screen_rect.size
        self.fondo = cargar_imagen("cueva.png", escalar=(ancho, alto))
        
        # Colores
        self.color_texto = (255, 255, 255)
        self.color_titulo = (255, 215, 0)
        self.color_hover = (255, 255, 150)
        self.color_borde_normal = (100, 100, 150)
        self.color_borde_hover = (255, 215, 0)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 60)
        self.fuente_subtitulo = pygame.font.Font(None, 36)
        self.fuente_objeto = pygame.font.Font(None, 32)
        self.fuente_descripcion = pygame.font.Font(None, 22)
        
        # Estado
        self.opciones = []
        self.opcion_hover = -1
        self.nombre_usuario = "Jugador"
        
        # ��reas de los 4 cuadrantes
        self.cuadrantes = []
        self.crear_cuadrantes()
        
        # Emojis para cada objeto
        self.emojis = {
            "espada": "⚔️",
            "armadura": "🛡️",
            "raciones": "🍖",
            "bolsa_monedas": "💰"
        }
    
    def crear_cuadrantes(self):
        """Crea las áreas de los 4 cuadrantes para selección."""
        # Dividir pantalla en 4 cuadrantes (2x2)
        mitad_ancho = ANCHO // 2
        mitad_alto = ALTO // 2
        margen = 20
        
        # Superior izquierda
        self.cuadrantes.append(pygame.Rect(
            margen, 
            120 + margen, 
            mitad_ancho - margen * 2, 
            mitad_alto - 70
        ))
        
        # Superior derecha
        self.cuadrantes.append(pygame.Rect(
            mitad_ancho + margen, 
            120 + margen, 
            mitad_ancho - margen * 2, 
            mitad_alto - 70
        ))
        
        # Inferior izquierda
        self.cuadrantes.append(pygame.Rect(
            margen, 
            mitad_alto + 50 + margen, 
            mitad_ancho - margen * 2, 
            mitad_alto - 70
        ))
        
        # Inferior derecha
        self.cuadrantes.append(pygame.Rect(
            mitad_ancho + margen, 
            mitad_alto + 50 + margen, 
            mitad_ancho - margen * 2, 
            mitad_alto - 70
        ))
    
    def startup(self, persist: dict):
        """
        Inicializa el estado al comenzar.
        
        Parámetros:
            persist (dict): Datos persistentes entre estados
        """
        self.persist = persist
        self.done = False
        
        # Obtener nombre del jugador
        self.nombre_usuario = self.persist.get("nombre_jugador", "Jugador")
        
        # Obtener opciones de objetos desde la lógica
        self.opciones = obtener_opciones_objetos()
        
        # Resetear hover
        self.opcion_hover = -1
    
    def seleccionar_objeto(self, indice: int):
        """
        Selecciona un objeto y lo guarda.
        
        Parámetros:
            indice (int): Índice del objeto seleccionado (0-3)
        """
        if 0 <= indice < len(self.opciones):
            objeto_tipo = self.opciones[indice]["tipo"]
            
            # Guardar objeto usando la lógica del core
            guardar_objeto_equipado(self.nombre_usuario, objeto_tipo)
            
            print(f"✅ Objeto '{objeto_tipo}' equipado para {self.nombre_usuario}")
            
            # Pasar al Game Over
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Verificar clic en cuadrantes
            for i, cuadrante in enumerate(self.cuadrantes):
                if cuadrante.collidepoint(pos) and i < len(self.opciones):
                    self.seleccionar_objeto(i)
                    break
                    
        elif event.type == pygame.KEYDOWN:
            # Selección con teclas numéricas
            if event.key == pygame.K_1:
                self.seleccionar_objeto(0)
            elif event.key == pygame.K_2:
                self.seleccionar_objeto(1)
            elif event.key == pygame.K_3:
                self.seleccionar_objeto(2)
            elif event.key == pygame.K_4:
                self.seleccionar_objeto(3)
    
    def update(self, dt: float):
        """
        Actualiza el estado de selección de objeto.
        
        Parámetros:
            dt (float): Delta time en milisegundos
        """
        # Actualizar hover
        mouse_pos = pygame.mouse.get_pos()
        self.opcion_hover = -1
        
        for i, cuadrante in enumerate(self.cuadrantes):
            if cuadrante.collidepoint(mouse_pos) and i < len(self.opciones):
                self.opcion_hover = i
                break
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja la pantalla de selección de objeto.
        
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
        
        # Título principal
        titulo = "🌟 ¡FELICIDADES! 🌟"
        titulo_render = self.fuente_titulo.render(titulo, True, self.color_titulo)
        titulo_rect = titulo_render.get_rect(center=(self.screen_rect.centerx, 40))
        surface.blit(titulo_render, titulo_rect)
        
        # Subtítulo
        subtitulo = "Elige tu Recompensa de la Esfinge"
        subtitulo_render = self.fuente_subtitulo.render(subtitulo, True, self.color_texto)
        subtitulo_rect = subtitulo_render.get_rect(center=(self.screen_rect.centerx, 90))
        surface.blit(subtitulo_render, subtitulo_rect)
        
        # Dibujar los 4 cuadrantes con objetos
        for i, cuadrante in enumerate(self.cuadrantes):
            if i < len(self.opciones):
                self.dibujar_opcion_objeto(surface, cuadrante, i)
    
    def dibujar_opcion_objeto(self, surface: pygame.Surface, rect: pygame.Rect, indice: int):
        """
        Dibuja un cuadrante con información de un objeto.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
            rect (pygame.Rect): Rectángulo del cuadrante
            indice (int): Índice de la opción
        """
        opcion = self.opciones[indice]
        tipo = opcion["tipo"]
        nombre = opcion["nombre"]
        
        # Determinar si está en hover
        es_hover = (indice == self.opcion_hover)
        
        # Fondo del cuadrante
        fondo_cuadrante = pygame.Surface((rect.width, rect.height))
        fondo_cuadrante.set_alpha(120 if not es_hover else 180)
        fondo_cuadrante.fill((30, 30, 50) if not es_hover else (50, 40, 30))
        surface.blit(fondo_cuadrante, rect.topleft)
        
        # Borde del cuadrante
        color_borde = self.color_borde_hover if es_hover else self.color_borde_normal
        grosor_borde = 4 if es_hover else 2
        pygame.draw.rect(surface, color_borde, rect, grosor_borde, 10)
        
        # Emoji del objeto
        emoji = self.emojis.get(tipo, "⭐")
        emoji_render = self.fuente_titulo.render(emoji, True, self.color_texto)
        emoji_rect = emoji_render.get_rect(center=(rect.centerx, rect.top + 60))
        surface.blit(emoji_render, emoji_rect)
        
        # Nombre del objeto
        color_nombre = self.color_hover if es_hover else self.color_titulo
        nombre_render = self.fuente_objeto.render(nombre, True, color_nombre)
        nombre_rect = nombre_render.get_rect(center=(rect.centerx, rect.top + 120))
        surface.blit(nombre_render, nombre_rect)
        
        # Descripción del objeto (dividida en líneas)
        descripcion = OBJETOS_ESPECIALES[tipo].get("descripcion", "")
        self.dibujar_descripcion(surface, descripcion, rect)
        
        # Número de tecla
        numero = f"[{indice + 1}]"
        numero_render = self.fuente_descripcion.render(numero, True, (150, 150, 150))
        numero_rect = numero_render.get_rect(bottomright=(rect.right - 10, rect.bottom - 10))
        surface.blit(numero_render, numero_rect)
    
    def dibujar_descripcion(self, surface: pygame.Surface, descripcion: str, rect: pygame.Rect):
        """
        Dibuja la descripción del objeto dividida en líneas.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
            descripcion (str): Texto de descripción
            rect (pygame.Rect): Rectángulo del cuadrante
        """
        # Dividir descripción en palabras
        palabras = descripcion.split()
        lineas = []
        linea_actual = ""
        ancho_max = rect.width - 40  # Margen interno
        
        for palabra in palabras:
            test_linea = linea_actual + palabra + " "
            if self.fuente_descripcion.size(test_linea)[0] < ancho_max:
                linea_actual = test_linea
            else:
                if linea_actual:
                    lineas.append(linea_actual.strip())
                linea_actual = palabra + " "
        
        if linea_actual:
            lineas.append(linea_actual.strip())
        
        # Dibujar líneas centradas
        y_offset = rect.top + 160
        for linea in lineas:
            linea_render = self.fuente_descripcion.render(linea, True, (200, 200, 200))
            linea_rect = linea_render.get_rect(center=(rect.centerx, y_offset))
            surface.blit(linea_render, linea_rect)
            y_offset += 25