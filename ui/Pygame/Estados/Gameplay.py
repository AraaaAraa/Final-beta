# =============================================================================
# ESTADO GAMEPLAY
# =============================================================================
# Pantalla principal del juego de trivia
# =============================================================================

import pygame
from .base import BaseEstado
from ..Botones import Boton
from ..efectos import dibujar_degradado_vertical, dibujar_sombra_texto
from data.repositorio_preguntas import cargar_preguntas_desde_csv
from core.logica_juego import (
    obtener_pregunta_para_nivel,
    preparar_datos_pregunta_para_ui,
    calcular_datos_buffeo_para_ui,
    procesar_pregunta_completa,
    verificar_condicion_fin_partida
)
from core.logica_preguntas import calcular_racha_actual, determinar_intentos_maximos
from config.constantes import RUTA_PREGUNTAS, PREGUNTAS_POR_NIVEL, MAX_ERRORES_PERMITIDOS


class gameplay(BaseEstado):
    """
    Estado principal del gameplay.
    
    Maneja la lógica del juego de trivia con integración completa
    de las funciones del módulo core.
    """
    
    def __init__(self):
        """Inicializa el estado de gameplay."""
        super(gameplay, self).__init__()
        self.sig_estado = "Gameover"
        
        # Colores
        self.color_fondo_1 = (20, 30, 50)
        self.color_fondo_2 = (50, 30, 80)
        self.color_texto = (255, 255, 255)
        self.color_pregunta = (255, 255, 200)
        self.color_correcto = (100, 255, 100)
        self.color_incorrecto = (255, 100, 100)
        self.color_buffeo = (255, 215, 0)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 40)
        self.fuente_pregunta = pygame.font.Font(None, 32)
        self.fuente_opcion = pygame.font.Font(None, 28)
        self.fuente_stats = pygame.font.Font(None, 30)
        
        # Estado del juego
        self.preguntas = {}
        self.preguntas_usadas = []
        self.respuestas_partida = []
        self.nivel_actual = 1
        self.numero_pregunta_nivel = 0
        self.pregunta_actual = None
        self.puntos_totales = 0
        self.racha_actual = 0
        self.errores = 0
        self.nombre_usuario = "Jugador"
        
        # Constante para conversión de índice a letra
        self.ASCII_A = 65
        
        # Estado de respuesta
        self.opcion_seleccionada = -1
        self.esperando_respuesta = False
        self.mostrar_resultado = False
        self.resultado_actual = None
        self.tiempo_resultado = 0
        
        # Botones de opciones (se crean dinámicamente)
        self.botones_opciones = []
    
    def startup(self, persist: dict):
        """
        Inicializa el estado al comenzar.
        
        Parámetros:
            persist (dict): Datos persistentes entre estados
        """
        self.persist = persist
        self.done = False
        
        # Resetear estado del juego
        self.preguntas = cargar_preguntas_desde_csv(RUTA_PREGUNTAS)
        self.preguntas_usadas = []
        self.respuestas_partida = []
        self.nivel_actual = 1
        self.numero_pregunta_nivel = 0
        self.puntos_totales = 0
        self.racha_actual = 0
        self.errores = 0
        self.opcion_seleccionada = -1
        self.esperando_respuesta = False
        self.mostrar_resultado = False
        self.resultado_actual = None
        
        # Cargar primera pregunta
        self.cargar_siguiente_pregunta()
    
    def cargar_siguiente_pregunta(self):
        """Carga la siguiente pregunta del nivel actual."""
        # Verificar si terminó el nivel
        if self.numero_pregunta_nivel >= PREGUNTAS_POR_NIVEL.get(self.nivel_actual, 0):
            # Pasar al siguiente nivel
            self.nivel_actual += 1
            self.numero_pregunta_nivel = 0
            
            # Verificar si terminó el juego
            if self.nivel_actual > 3:
                self.terminar_juego()
                return
        
        # Obtener pregunta
        self.pregunta_actual = obtener_pregunta_para_nivel(
            self.preguntas,
            self.nivel_actual,
            self.preguntas_usadas
        )
        
        if self.pregunta_actual is None or not self.pregunta_actual:
            # No hay más preguntas, terminar juego
            self.terminar_juego()
            return
        
        # Agregar a preguntas usadas
        self.preguntas_usadas.append(self.pregunta_actual.get("id", 0))
        self.numero_pregunta_nivel += 1
        
        # Crear botones de opciones
        self.crear_botones_opciones()
        
        # Resetear estado de respuesta
        self.opcion_seleccionada = -1
        self.esperando_respuesta = True
        self.mostrar_resultado = False
        self.resultado_actual = None
    
    def crear_botones_opciones(self):
        """Crea los botones para las opciones de respuesta."""
        self.botones_opciones = []
        opciones = self.pregunta_actual.get("opciones", [])
        
        y_start = 300
        for i, opcion in enumerate(opciones):
            boton = Boton(
                f"{chr(self.ASCII_A + i)}. {opcion}",
                100,
                y_start + (i * 60),
                600,
                50,
                self.fuente_opcion,
                (80, 80, 150)
            )
            self.botones_opciones.append(boton)
    
    def procesar_respuesta(self, indice_opcion: int):
        """
        Procesa la respuesta del usuario.
        
        Parámetros:
            indice_opcion (int): Índice de la opción seleccionada (0-3)
        """
        if not self.pregunta_actual or indice_opcion < 0:
            return
        
        opciones = self.pregunta_actual.get("opciones", [])
        if indice_opcion >= len(opciones):
            return
        
        # Convertir índice a letra (A, B, C, D)
        letra_respuesta = chr(self.ASCII_A + indice_opcion)
        
        # Procesar con la lógica del core
        self.resultado_actual = procesar_pregunta_completa(
            self.pregunta_actual,
            self.nombre_usuario,
            self.racha_actual,
            letra_respuesta,
            0,
            determinar_intentos_maximos(self.nombre_usuario)
        )
        
        # Actualizar estadísticas
        if self.resultado_actual.get("es_correcta", False):
            self.puntos_totales += self.resultado_actual.get("puntos", 0)
            self.racha_actual += 1
        else:
            self.racha_actual = 0
            self.errores += 1
        
        # Guardar respuesta
        self.respuestas_partida.append(self.resultado_actual)
        
        # Mostrar resultado
        self.mostrar_resultado = True
        self.esperando_respuesta = False
        self.tiempo_resultado = 0
        
        # Verificar condición de fin
        if verificar_condicion_fin_partida(self.respuestas_partida):
            self.terminar_juego()
    
    def terminar_juego(self):
        """Termina el juego y pasa al estado Game Over."""
        # Contar respuestas correctas
        respuestas_correctas = sum(
            1 for r in self.respuestas_partida 
            if r.get("es_correcta", False)
        )
        
        # Pasar estadísticas al siguiente estado
        self.persist["puntos_totales"] = self.puntos_totales
        self.persist["respuestas_correctas"] = respuestas_correctas
        self.persist["total_preguntas"] = len(self.respuestas_partida)
        
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
        elif event.type == pygame.MOUSEBUTTONDOWN and self.esperando_respuesta:
            pos = pygame.mouse.get_pos()
            for i, boton in enumerate(self.botones_opciones):
                if boton.verificar_click(pos):
                    self.opcion_seleccionada = i
                    self.procesar_respuesta(i)
                    break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.terminar_juego()
            elif self.esperando_respuesta:
                # Navegación con teclas
                if event.key == pygame.K_1:
                    self.opcion_seleccionada = 0
                    self.procesar_respuesta(0)
                elif event.key == pygame.K_2:
                    self.opcion_seleccionada = 1
                    self.procesar_respuesta(1)
                elif event.key == pygame.K_3:
                    self.opcion_seleccionada = 2
                    self.procesar_respuesta(2)
                elif event.key == pygame.K_4:
                    self.opcion_seleccionada = 3
                    self.procesar_respuesta(3)
            elif self.mostrar_resultado:
                # Presionar cualquier tecla para continuar
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.cargar_siguiente_pregunta()
    
    def update(self, dt: float):
        """
        Actualiza el estado del gameplay.
        
        Parámetros:
            dt (float): Delta time en milisegundos
        """
        if self.mostrar_resultado:
            self.tiempo_resultado += dt
            # Avanzar automáticamente después de 3 segundos
            if self.tiempo_resultado > 3000:
                self.cargar_siguiente_pregunta()
    
    def draw(self, surface: pygame.Surface):
        """
        Dibuja el gameplay en la superficie.
        
        Parámetros:
            surface (pygame.Surface): Superficie donde dibujar
        """
        # Fondo con degradado
        dibujar_degradado_vertical(surface, self.color_fondo_1, self.color_fondo_2)
        
        # Encabezado con estadísticas
        self.dibujar_stats(surface)
        
        # Pregunta
        if self.pregunta_actual:
            self.dibujar_pregunta(surface)
        
        # Opciones
        if self.esperando_respuesta:
            for boton in self.botones_opciones:
                boton.draw(surface)
        
        # Resultado
        if self.mostrar_resultado and self.resultado_actual:
            self.dibujar_resultado(surface)
    
    def dibujar_stats(self, surface: pygame.Surface):
        """Dibuja las estadísticas en la parte superior."""
        y = 20
        
        # Nivel
        nivel_text = f"Nivel {self.nivel_actual} - Pregunta {self.numero_pregunta_nivel}/{PREGUNTAS_POR_NIVEL.get(self.nivel_actual, 0)}"
        nivel_render = self.fuente_stats.render(nivel_text, True, self.color_texto)
        surface.blit(nivel_render, (20, y))
        
        # Puntos
        puntos_text = f"Puntos: {self.puntos_totales}"
        puntos_render = self.fuente_stats.render(puntos_text, True, (255, 215, 0))
        surface.blit(puntos_render, (400, y))
        
        y += 35
        
        # Racha
        racha_text = f"Racha: {self.racha_actual}"
        racha_render = self.fuente_stats.render(racha_text, True, self.color_buffeo)
        surface.blit(racha_render, (20, y))
        
        # Errores
        errores_text = f"Errores: {self.errores}/{MAX_ERRORES_PERMITIDOS}"
        color_error = self.color_incorrecto if self.errores > 0 else self.color_texto
        errores_render = self.fuente_stats.render(errores_text, True, color_error)
        surface.blit(errores_render, (400, y))
    
    def dibujar_pregunta(self, surface: pygame.Surface):
        """Dibuja la pregunta actual."""
        descripcion = self.pregunta_actual.get("descripcion", "")
        categoria = self.pregunta_actual.get("categoria", "")
        
        # Categoría
        cat_text = f"[{categoria}]"
        cat_render = self.fuente_opcion.render(cat_text, True, (150, 150, 255))
        cat_rect = cat_render.get_rect(center=(self.screen_rect.centerx, 120))
        surface.blit(cat_render, cat_rect)
        
        # Pregunta (dividir en líneas si es muy larga)
        palabras = descripcion.split()
        lineas = []
        linea_actual = ""
        
        for palabra in palabras:
            test_linea = linea_actual + palabra + " "
            if self.fuente_pregunta.size(test_linea)[0] < 700:
                linea_actual = test_linea
            else:
                if linea_actual:
                    lineas.append(linea_actual)
                linea_actual = palabra + " "
        
        if linea_actual:
            lineas.append(linea_actual)
        
        y_offset = 170
        for linea in lineas:
            pregunta_render = self.fuente_pregunta.render(linea.strip(), True, self.color_pregunta)
            pregunta_rect = pregunta_render.get_rect(center=(self.screen_rect.centerx, y_offset))
            surface.blit(pregunta_render, pregunta_rect)
            y_offset += 35
    
    def dibujar_resultado(self, surface: pygame.Surface):
        """Dibuja el resultado de la respuesta."""
        # Overlay semi-transparente
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Mensaje
        mensaje = self.resultado_actual.get("mensaje", "")
        color = self.color_correcto if self.resultado_actual.get("es_correcta", False) else self.color_incorrecto
        
        # Dividir mensaje en líneas
        lineas = mensaje.split("\n")
        y_offset = 200
        
        for linea in lineas:
            texto_render = self.fuente_titulo.render(linea, True, color)
            texto_rect = texto_render.get_rect(center=(self.screen_rect.centerx, y_offset))
            surface.blit(texto_render, texto_rect)
            y_offset += 50
        
        # Puntos obtenidos
        if self.resultado_actual.get("es_correcta", False):
            puntos = self.resultado_actual.get("puntos", 0)
            puntos_text = f"+{puntos} puntos"
            puntos_render = self.fuente_stats.render(puntos_text, True, (255, 215, 0))
            puntos_rect = puntos_render.get_rect(center=(self.screen_rect.centerx, y_offset + 20))
            surface.blit(puntos_render, puntos_rect)
        
        # Instrucción
        instruccion = "Presiona ESPACIO o espera 3 segundos..."
        instruccion_render = self.fuente_opcion.render(instruccion, True, (200, 200, 200))
        instruccion_rect = instruccion_render.get_rect(center=(self.screen_rect.centerx, 500))
        surface.blit(instruccion_render, instruccion_rect)
