# =============================================================================
# ESTADO GAMEPLAY
# =============================================================================
# Pantalla principal del juego de trivia
# =============================================================================

import pygame
from .base import BaseEstado
from config.constantes import ALTO, ANCHO
from ..Botones import Boton, BOTON_ALTO_PEQUENO, BOTON_ANCHO_PEQUENO
from ..recursos import cargar_imagen, cargar_fuente_principal
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
from core.logica_buffeos import verificar_objeto_equipado, verificar_merecimiento_objeto
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
        
        # Cargar fondo
        ancho, alto = self.screen_rect.size
        self.fondo = cargar_imagen("cueva.png", escalar=(ancho, alto))
        
        # Colores
        self.color_texto = (255, 255, 255)
        self.color_pregunta = (255, 255, 200)
        self.color_correcto = (100, 255, 100)
        self.color_incorrecto = (255, 100, 100)
        self.color_buffeo = (255, 215, 0)
        
        # Fuentes con Jacquard12
        self.fuente_titulo = cargar_fuente_principal(40)
        self.fuente_pregunta = cargar_fuente_principal(32)
        self.fuente_opcion = cargar_fuente_principal(28)
        self.fuente_stats = cargar_fuente_principal(30)
        self.fuente_buffeo = cargar_fuente_principal(24)
        
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
        
        # ⬅️ VIDAS EXTRA
        self.vidas_extra_iniciales = 0
        self.max_errores_con_vidas = MAX_ERRORES_PERMITIDOS
        
        # Constante para conversión de índice a letra
        self.ASCII_A = 65
        
        # Estado de respuesta
        self.opcion_seleccionada = -1
        self.esperando_respuesta = False
        self.mostrar_resultado = False
        self.resultado_actual = None
        self.tiempo_resultado = 0
        
        # Estado de buffeo
        self.buffeo_activo = False
        self.datos_buffeo = None
        
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
        
        # Obtener nombre del jugador
        self.nombre_usuario = self.persist.get("nombre_jugador", "Jugador")
        
        # ⬅️ CALCULAR ERRORES PERMITIDOS CON VIDAS EXTRA
        from core.logica_buffeos import calcular_errores_permitidos_con_vidas, obtener_vidas_extra_usuario
        
        self.vidas_extra_iniciales = obtener_vidas_extra_usuario(self.nombre_usuario)
        self.max_errores_con_vidas = calcular_errores_permitidos_con_vidas(self.nombre_usuario)
        
        print(f"🎮 Iniciando partida - Errores permitidos: {self.max_errores_con_vidas} (Base: {MAX_ERRORES_PERMITIDOS} + Extra: {self.vidas_extra_iniciales})")
        
        # Verificar objeto equipado al inicio
        objeto_equipado = verificar_objeto_equipado(self.nombre_usuario)
        if objeto_equipado:
            print(f"🎮 Iniciando partida con objeto: {objeto_equipado}")
        else:
            print(f"🎮 Iniciando partida sin objetos especiales")
        
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
        self.buffeo_activo = False
        self.datos_buffeo = None
        
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
        
        # Actualizar buffeo antes de mostrar la pregunta
        self.actualizar_buffeo()
        
        # Crear botones de opciones
        self.crear_botones_opciones()
        
        # Resetear estado de respuesta
        self.opcion_seleccionada = -1
        self.esperando_respuesta = True
        self.mostrar_resultado = False
        self.resultado_actual = None
    
    def actualizar_buffeo(self):
        """Actualiza los datos del buffeo según la racha actual."""
        self.datos_buffeo = calcular_datos_buffeo_para_ui(self.racha_actual, self.nombre_usuario)
        self.buffeo_activo = self.datos_buffeo.get("tiene_buffeo", False)
        
        # DEBUG: Mostrar información del buffeo
        if self.buffeo_activo:
            print(f"🔥 Buffeo activo - Racha: {self.racha_actual}, Puntos extra: {self.datos_buffeo.get('puntos_totales', 0)}")
    
    def crear_botones_opciones(self):
        """Crea los botones para las opciones de respuesta."""
        self.botones_opciones = []
        opciones = self.pregunta_actual.get("opciones", [])
        
        # TUS VALORES PERSONALIZADOS (NO MODIFICADOS)
        y_start = 200
        espaciado = 100
        x_centrado = (self.screen_rect.width - BOTON_ANCHO_PEQUENO) // 2
        
        for i, opcion in enumerate(opciones):
            boton = Boton(
                f"{chr(self.ASCII_A + i)}. {opcion}",
                x_centrado,
                y_start + (i * espaciado),
                BOTON_ANCHO_PEQUENO,
                BOTON_ALTO_PEQUENO,
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
        
        # Verificar objeto antes de procesar
        objeto_equipado = verificar_objeto_equipado(self.nombre_usuario)
        print(f"📝 Procesando respuesta '{letra_respuesta}' - Objeto: {objeto_equipado}, Racha: {self.racha_actual}")
        
        # Procesar con la lógica del core
        self.resultado_actual = procesar_pregunta_completa(
            self.pregunta_actual,
            self.nombre_usuario,
            self.racha_actual,
            letra_respuesta,
            0,
            determinar_intentos_maximos(self.nombre_usuario)
        )
        
        # DEBUG: Mostrar puntos obtenidos
        puntos_obtenidos = self.resultado_actual.get("puntos", 0)
        es_correcta = self.resultado_actual.get("es_correcta", False)
        print(f"✅ Resultado: {'Correcta' if es_correcta else 'Incorrecta'} - Puntos: {puntos_obtenidos}")
        
        # Actualizar estadísticas
        if es_correcta:
            self.puntos_totales += puntos_obtenidos
            self.racha_actual += 1
        else:
            self.racha_actual = 0
            self.errores += 1
        
        # Actualizar buffeo después de responder
        self.actualizar_buffeo()
        
        # Guardar respuesta
        self.respuestas_partida.append(self.resultado_actual)
        
        # Mostrar resultado
        self.mostrar_resultado = True
        self.esperando_respuesta = False
        self.tiempo_resultado = 0
        
        # ⬅️ VERIFICAR CONDICIÓN DE FIN CON VIDAS EXTRA
        if self.errores >= self.max_errores_con_vidas:
            print(f"💀 Game Over - Errores: {self.errores}/{self.max_errores_con_vidas}")
            self.terminar_juego()
    
    def terminar_juego(self):
        """Termina el juego y pasa al estado Game Over o Selección de Objeto."""
        from core.logica_buffeos import consumir_vidas_extra_usuario, calcular_vidas_ganadas, guardar_vidas_extra_usuario
        
        # Contar respuestas correctas
        respuestas_correctas = sum(
            1 for r in self.respuestas_partida 
            if r.get("es_correcta", False)
        )
        
        # ⬅️ CONSUMIR VIDAS EXTRA USADAS
        vidas_usadas = max(0, self.errores - MAX_ERRORES_PERMITIDOS)
        if vidas_usadas > 0:
            consumir_vidas_extra_usuario(self.nombre_usuario, vidas_usadas)
            print(f"💔 Vidas extra consumidas: {vidas_usadas}")
        
        # ⬅️ CALCULAR VIDAS GANADAS
        vidas_ganadas = calcular_vidas_ganadas(self.puntos_totales)
        if vidas_ganadas > 0:
            guardar_vidas_extra_usuario(self.nombre_usuario, vidas_ganadas)
            print(f"💚 Vidas extra ganadas: {vidas_ganadas} (por {self.puntos_totales} puntos)")
        
        # Verificar si merece objeto especial
        total_preguntas = len(self.respuestas_partida)
        merece_objeto = verificar_merecimiento_objeto(
            self.nombre_usuario, 
            respuestas_correctas, 
            total_preguntas
        )
        
        # Pasar estadísticas al siguiente estado
        self.persist["puntos_totales"] = self.puntos_totales
        self.persist["respuestas_correctas"] = respuestas_correctas
        self.persist["total_preguntas"] = total_preguntas
        self.persist["vidas_ganadas"] = vidas_ganadas  # ⬅️ NUEVO
        self.persist["vidas_usadas"] = vidas_usadas    # ⬅️ NUEVO
        
        # Si merece objeto, ir a pantalla de selección
        if merece_objeto:
            print(f"🌟 ¡{self.nombre_usuario} merece un objeto especial! ({respuestas_correctas}/{total_preguntas} correctas)")
            self.sig_estado = "SeleccionObjeto"
        else:
            print(f"📊 Fin de partida: {respuestas_correctas}/{total_preguntas} correctas - No merece objeto")
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
            
            # Verificar en orden inverso (del último al primero)
            for i in range(len(self.botones_opciones) - 1, -1, -1):
                boton = self.botones_opciones[i]
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
        # Actualizar hover de botones
        if self.esperando_respuesta:
            mouse_pos = pygame.mouse.get_pos()
            
            # Resetear todos los hovers
            for boton in self.botones_opciones:
                boton.hover = False
            
            # Verificar hover en orden inverso
            for i in range(len(self.botones_opciones) - 1, -1, -1):
                boton = self.botones_opciones[i]
                if boton.rect.collidepoint(mouse_pos):
                    boton.hover = True
                    break
        
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
        # Dibujar fondo de imagen
        surface.blit(self.fondo, (0, 0))
        
        # Overlay semi-transparente
        overlay = pygame.Surface(self.screen_rect.size)
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Encabezado con estadísticas
        self.dibujar_stats(surface)
        
        # Mostrar buffeo si está activo
        if self.buffeo_activo and self.datos_buffeo and self.esperando_respuesta:
            self.dibujar_buffeo(surface)
        
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
        
        # Racha (con indicador de buffeo)
        racha_text = f"Racha: {self.racha_actual}"
        if self.buffeo_activo:
            racha_text += " (Fuego)"
        racha_render = self.fuente_stats.render(racha_text, True, self.color_buffeo if self.buffeo_activo else self.color_texto)
        surface.blit(racha_render, (20, y))
        
        # ⬅️ ERRORES CON VIDAS EXTRA
        errores_text = f"Errores: {self.errores}/{self.max_errores_con_vidas}"
        
        # Si tiene vidas extra, mostrar desglose
        if self.vidas_extra_iniciales > 0:
            vidas_usadas = max(0, self.errores - MAX_ERRORES_PERMITIDOS)
            vidas_restantes = self.vidas_extra_iniciales - vidas_usadas
            errores_text += f" (+{vidas_restantes} vidas)"
        
        color_error = self.color_incorrecto if self.errores > 0 else self.color_texto
        errores_render = self.fuente_stats.render(errores_text, True, color_error)
        surface.blit(errores_render, (400, y))
        
        # Mostrar objeto equipado
        objeto = verificar_objeto_equipado(self.nombre_usuario)
        if objeto:
            y += 35
            # Mapeo de nombres de objetos para display
            nombres_objetos = {
                "espada": "Espada",
                "armadura": "Armadura",
                "raciones": "Raciones",
                "bolsa_monedas": "Bolsa"
            }
            nombre_display = nombres_objetos.get(objeto, objeto.capitalize())
            objeto_text = f"Objeto: {nombre_display}"
            objeto_render = self.fuente_buffeo.render(objeto_text, True, (150, 255, 150))
            surface.blit(objeto_render, (20, y))
    
    def dibujar_buffeo(self, surface: pygame.Surface):
        """Dibuja el indicador de buffeo activo."""
        if not self.datos_buffeo:
            return
        
        # Posición en la esquina superior derecha
        x = ANCHO - 250
        y = 100
        
        # Fondo semi-transparente para el buffeo
        buffeo_bg = pygame.Surface((230, 80))
        buffeo_bg.set_alpha(180)
        buffeo_bg.fill((50, 30, 10))
        surface.blit(buffeo_bg, (x, y))
        
        # Borde dorado
        pygame.draw.rect(surface, self.color_buffeo, (x, y, 230, 80), 2)
        
        # Título
        titulo_text = "BUFFEO ACTIVO!"
        titulo_render = self.fuente_buffeo.render(titulo_text, True, self.color_buffeo)
        surface.blit(titulo_render, (x + 10, y + 10))
        
        # Detalles del buffeo
        puntos_racha = self.datos_buffeo.get("puntos_racha", 0)
        puntos_objeto = self.datos_buffeo.get("puntos_objeto", 0)
        
        y_offset = y + 35
        
        if puntos_racha > 0:
            racha_text = f"  Racha: +{puntos_racha} pts"
            racha_render = self.fuente_buffeo.render(racha_text, True, (255, 200, 100))
            surface.blit(racha_render, (x + 10, y_offset))
            y_offset += 20
        
        if puntos_objeto > 0:
            objeto_text = f"  Objeto: +{puntos_objeto} pts"
            objeto_render = self.fuente_buffeo.render(objeto_text, True, (150, 255, 150))
            surface.blit(objeto_render, (x + 10, y_offset))
    
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
        overlay = pygame.Surface((ANCHO, ALTO))
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
        
        # Desglose de puntos (incluyendo buffeo)
        if self.resultado_actual.get("es_correcta", False):
            puntos_totales = self.resultado_actual.get("puntos", 0)
            puntos_base = self.resultado_actual.get("puntos_base", puntos_totales)
            puntos_buffeo = self.resultado_actual.get("puntos_buffeo", 0)
            puntos_objeto = self.resultado_actual.get("puntos_objetos", 0)
            
            # Puntos totales
            puntos_text = f"+{puntos_totales} puntos"
            puntos_render = self.fuente_stats.render(puntos_text, True, (255, 215, 0))
            puntos_rect = puntos_render.get_rect(center=(self.screen_rect.centerx, y_offset + 20))
            surface.blit(puntos_render, puntos_rect)
            
            # Desglose si hay buffeo
            if puntos_buffeo > 0 or puntos_objeto > 0:
                y_offset += 55
                desglose_text = f"(Base: {puntos_base}"
                if puntos_buffeo > 0:
                    desglose_text += f" + Buffeo: {puntos_buffeo}"
                if puntos_objeto > 0:
                    desglose_text += f" + Objeto: {puntos_objeto}"
                desglose_text += ")"
                
                desglose_render = self.fuente_buffeo.render(desglose_text, True, (200, 200, 200))
                desglose_rect = desglose_render.get_rect(center=(self.screen_rect.centerx, y_offset))
                surface.blit(desglose_render, desglose_rect)
        
        # Instrucción
        instruccion = "Presiona ESPACIO o espera 3 segundos..."
        instruccion_render = self.fuente_opcion.render(instruccion, True, (200, 200, 200))
        instruccion_rect = instruccion_render.get_rect(center=(self.screen_rect.centerx, 500))
        surface.blit(instruccion_render, instruccion_rect)