# =============================================================================
# GESTOR DE RESPUESTAS
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Responsable de mostrar opciones, detectar clicks/teclado y procesar 
#    respuestas del usuario. Coordina con el módulo core para la lógica.
#
# 🔗 DEPENDENCIAS CORE:
#    - core/logica_juego.py: procesar_pregunta_completa()
#    - core/logica_preguntas.py: determinar_intentos_maximos()
#    - core/logica_buffeos.py: verificar_objeto_equipado()
#
# 🔗 DEPENDENCIAS PYGAME:
#    - ui/Pygame/Botones.py: Boton (clase existente)
#
# 💡 RESPONSABILIDAD ÚNICA:
#    Solo maneja interacción del usuario con opciones de respuesta.
#    Delega procesamiento de lógica al módulo core/.
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Patrón de separación UI/Lógica
#    - UI solo detecta eventos y muestra, core procesa
#    - Reutiliza clase Boton existente del proyecto
#    - Un solo return por función
# =============================================================================

import pygame
from ..Botones import Boton, BOTON_ANCHO_PEQUENO, BOTON_ALTO_PEQUENO
from core.logica_juego import procesar_pregunta_completa
from core.logica_preguntas import determinar_intentos_maximos
from core.logica_buffeos import verificar_objeto_equipado


class GestorRespuestas:
    """Gestiona botones de respuesta, detección de clicks y procesamiento."""
    
    def __init__(self, fuente_opcion: pygame.font.Font, screen_rect: pygame.Rect):
        """
        Inicializa el gestor de respuestas.
        
        Args:
            fuente_opcion (pygame.font.Font): Fuente para texto de opciones
            screen_rect (pygame.Rect): Rectángulo de la pantalla (para centrado)
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py (línea ~41) - Crear gestor al inicializar
        
        Ejemplo:
            fuente = pygame.font.Font(None, 28)
            rect = pygame.display.get_surface().get_rect()
            gestor = GestorRespuestas(fuente, rect)
        """
        self.botones_opciones = []
        self.fuente_opcion = fuente_opcion
        self.screen_rect = screen_rect
        self.opcion_seleccionada = -1
        self.esperando_respuesta = False
        
        # Constante para conversión índice -> letra
        self.ASCII_A = 65
        
        return None
    
    def crear_botones_opciones(self, opciones: list) -> None:
        """
        Crea botones para las opciones de respuesta.
        
        Args:
            opciones (list): Lista de strings con las opciones
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py (línea ~170) - Al cargar nueva pregunta
        
        Ejemplo:
            opciones = ["Zeus", "Poseidón", "Hades", "Ares"]
            gestor.crear_botones_opciones(opciones)
        """
        self.botones_opciones = []
        
        # Configuración de posicionamiento
        y_start = 200
        espaciado = 100
        x_centrado = (self.screen_rect.width - BOTON_ANCHO_PEQUENO) // 2
        
        # Crear un botón por cada opción
        i = 0
        while i < len(opciones):
            # Agregar letra (A, B, C, D) al texto de la opción
            texto_boton = f"{chr(self.ASCII_A + i)}. {opciones[i]}"
            
            boton = Boton(
                texto_boton,
                x_centrado,
                y_start + (i * espaciado),
                BOTON_ANCHO_PEQUENO,
                BOTON_ALTO_PEQUENO,
                self.fuente_opcion,
                (80, 80, 150)
            )
            self.botones_opciones.append(boton)
            i = i + 1
        
        self.esperando_respuesta = True
        self.opcion_seleccionada = -1
        
        return None
    
    def actualizar_hover(self, pos_mouse: tuple) -> None:
        """
        Actualiza estado hover de todos los botones.
        
        Args:
            pos_mouse (tuple): Posición (x, y) del mouse
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py (línea ~379) - En update()
        
        Ejemplo:
            pos = pygame.mouse.get_pos()
            gestor.actualizar_hover(pos)
        """
        # Primero resetear todos
        for boton in self.botones_opciones:
            boton.hover = False
        
        # Activar hover del botón bajo el mouse (en orden inverso)
        i = len(self.botones_opciones) - 1
        while i >= 0:
            if self.botones_opciones[i].rect.collidepoint(pos_mouse):
                self.botones_opciones[i].hover = True
                break
            i = i - 1
        
        return None
    
    def detectar_click(self, pos_click: tuple) -> int:
        """
        Detecta qué botón fue clickeado.
        
        Args:
            pos_click (tuple): Posición (x, y) del click
        
        Returns:
            int: Índice del botón clickeado, -1 si ninguno
        
        Usado en:
            - Estados/Gameplay/gameplay.py (línea ~341) - En get_event()
        
        Ejemplo:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                indice = gestor.detectar_click(evento.pos)
        """
        indice_clickeado = -1
        
        # Verificar en orden inverso
        i = len(self.botones_opciones) - 1
        while i >= 0:
            if self.botones_opciones[i].verificar_click(pos_click):
                indice_clickeado = i
                break
            i = i - 1
        
        return indice_clickeado
    
    def procesar_respuesta(self, indice_opcion: int, pregunta_actual: dict, 
                          nombre_usuario: str, racha_actual: int) -> dict:
        """
        Procesa la respuesta usando la lógica del core.
        
        Args:
            indice_opcion (int): Índice de la opción seleccionada (0-3)
            pregunta_actual (dict): Diccionario con datos de la pregunta
            nombre_usuario (str): Nombre del jugador
            racha_actual (int): Racha actual del jugador
        
        Returns:
            dict: Resultado del procesamiento (puntos, es_correcta, etc.)
        
        Usado en:
            - Estados/Gameplay/gameplay.py (línea ~209) - Al procesar respuesta
        
        Ejemplo:
            resultado = gestor.procesar_respuesta(0, pregunta, "Jugador1", 3)
            puntos = resultado.get("puntos", 0)
        """
        # Validar entrada
        if not pregunta_actual or indice_opcion < 0:
            resultado = {
                "es_correcta": False,
                "puntos": 0,
                "puntos_totales": 0
            }
            return resultado
        
        opciones = pregunta_actual.get("opciones", [])
        if indice_opcion >= len(opciones):
            resultado = {
                "es_correcta": False,
                "puntos": 0,
                "puntos_totales": 0
            }
            return resultado
        
        # Convertir índice a letra (A, B, C, D)
        letra_respuesta = chr(self.ASCII_A + indice_opcion)
        
        # Verificar objeto equipado antes de procesar
        objeto_equipado = verificar_objeto_equipado(nombre_usuario)
        print(f"📝 Procesando respuesta '{letra_respuesta}' - Objeto: {objeto_equipado}, Racha: {racha_actual}")
        
        # DELEGAR PROCESAMIENTO AL CORE
        resultado_core = procesar_pregunta_completa(
            pregunta_actual,
            nombre_usuario,
            racha_actual,
            letra_respuesta,
            0,  # Intento actual (primer intento)
            determinar_intentos_maximos(nombre_usuario)
        )
        
        # DEBUG: Mostrar resultado
        puntos_obtenidos = resultado_core.get("puntos", 0)
        es_correcta = resultado_core.get("es_correcta", False)
        print(f"✅ Resultado: {'Correcta' if es_correcta else 'Incorrecta'} - Puntos: {puntos_obtenidos}")
        
        # Marcar que ya no se espera respuesta
        self.esperando_respuesta = False
        self.opcion_seleccionada = indice_opcion
        
        return resultado_core
    
    def renderizar(self, pantalla: pygame.Surface) -> None:
        """
        Renderiza botones de opciones si se está esperando respuesta.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py (línea ~427) - En draw()
        
        Ejemplo:
            if gestor.esperando_respuesta:
                gestor.renderizar(screen)
        """
        if self.esperando_respuesta:
            for boton in self.botones_opciones:
                boton.draw(pantalla)
        
        return None
    
    def resetear(self) -> None:
        """
        Resetea el estado del gestor.
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py - Al cargar nueva pregunta
        
        Ejemplo:
            gestor.resetear()
        """
        self.opcion_seleccionada = -1
        self.esperando_respuesta = False
        return None
