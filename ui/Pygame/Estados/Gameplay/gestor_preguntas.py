# =============================================================================
# GESTOR DE PREGUNTAS
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Responsable de cargar, seleccionar y mostrar preguntas del juego.
#    Maneja el flujo de preguntas por nivel y tracking de preguntas usadas.
#
# 🔗 DEPENDENCIAS CORE:
#    - data/repositorio_preguntas.py: cargar_preguntas_desde_csv()
#    - core/logica_juego.py: obtener_pregunta_para_nivel()
#
# 🔗 DEPENDENCIAS PYGAME:
#    - ui/Pygame/efectos.py: dibujar_sombra_texto()
#
# 💡 RESPONSABILIDAD ÚNICA:
#    Solo maneja preguntas: carga, selección y renderizado.
#    NO maneja puntos, respuestas ni racha.
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Patrón de separación de responsabilidades (Single Responsibility)
#    - Delega lógica de negocio al módulo core/
#    - Solo renderiza, no procesa lógica del juego
#    - Un solo return por función
# =============================================================================

import pygame
from data.repositorio_preguntas import cargar_preguntas_desde_csv
from core.logica_juego import obtener_pregunta_para_nivel
from config.constantes import RUTA_PREGUNTAS, PREGUNTAS_POR_NIVEL
from ..efectos import dibujar_sombra_texto


class GestorPreguntas:
    """Gestiona carga, selección y visualización de preguntas."""
    
    def __init__(self, fuente_pregunta: pygame.font.Font, color_pregunta: tuple):
        """
        Inicializa el gestor de preguntas.
        
        Args:
            fuente_pregunta (pygame.font.Font): Fuente para renderizar pregunta
            color_pregunta (tuple): Color RGB para el texto de la pregunta
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py (línea ~40) - Crear gestor al inicializar
        
        Ejemplo:
            fuente = pygame.font.Font(None, 32)
            gestor = GestorPreguntas(fuente, (255, 255, 200))
        """
        self.preguntas = {}
        self.preguntas_usadas = []
        self.pregunta_actual = None
        self.nivel_actual = 1
        self.numero_pregunta_nivel = 0
        
        # Configuración de renderizado
        self.fuente_pregunta = fuente_pregunta
        self.color_pregunta = color_pregunta
        
        return None
    
    def cargar_preguntas(self) -> None:
        """
        Carga todas las preguntas desde el archivo CSV.
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py (línea ~120) - Al iniciar partida
        
        Ejemplo:
            gestor.cargar_preguntas()
        """
        self.preguntas = cargar_preguntas_desde_csv(RUTA_PREGUNTAS)
        return None
    
    def siguiente_pregunta(self) -> bool:
        """
        Carga la siguiente pregunta del nivel actual.
        Avanza de nivel automáticamente cuando se completan todas las preguntas.
        
        Returns:
            bool: True si hay pregunta disponible, False si terminó el juego
        
        Usado en:
            - Estados/Gameplay/gameplay.py (línea ~135) - Después de cada respuesta
        
        Ejemplo:
            if not gestor.siguiente_pregunta():
                print("Juego terminado - No hay más preguntas")
        """
        # Verificar si terminó el nivel
        if self.numero_pregunta_nivel >= PREGUNTAS_POR_NIVEL.get(self.nivel_actual, 0):
            # Pasar al siguiente nivel
            self.nivel_actual = self.nivel_actual + 1
            self.numero_pregunta_nivel = 0
            
            # Verificar si terminó el juego (nivel 4 no existe)
            if self.nivel_actual > 3:
                resultado = False
                return resultado
        
        # Obtener pregunta usando lógica del core
        self.pregunta_actual = obtener_pregunta_para_nivel(
            self.preguntas,
            self.nivel_actual,
            self.preguntas_usadas
        )
        
        # Verificar si se obtuvo una pregunta válida
        if self.pregunta_actual is None or not self.pregunta_actual:
            resultado = False
            return resultado
        
        # Agregar a preguntas usadas
        self.preguntas_usadas.append(self.pregunta_actual.get("id", 0))
        self.numero_pregunta_nivel = self.numero_pregunta_nivel + 1
        
        resultado = True
        return resultado
    
    def obtener_opciones(self) -> list:
        """
        Obtiene las opciones de la pregunta actual.
        
        Returns:
            list: Lista de opciones (strings) de la pregunta actual
        
        Usado en:
            - Estados/Gameplay/gestor_respuestas.py - Crear botones de opciones
        
        Ejemplo:
            opciones = gestor.obtener_opciones()
            # ['Opción A', 'Opción B', 'Opción C', 'Opción D']
        """
        if self.pregunta_actual:
            opciones = self.pregunta_actual.get("opciones", [])
        else:
            opciones = []
        
        return opciones
    
    def obtener_descripcion_pregunta(self) -> str:
        """
        Obtiene el texto/descripción de la pregunta actual.
        
        Returns:
            str: Texto de la pregunta actual
        
        Usado en:
            - Estados/Gameplay/gameplay.py - Para renderizado
        
        Ejemplo:
            pregunta = gestor.obtener_descripcion_pregunta()
        """
        if self.pregunta_actual:
            descripcion = self.pregunta_actual.get("descripcion", "")
        else:
            descripcion = ""
        
        return descripcion
    
    def renderizar(self, pantalla: pygame.Surface) -> None:
        """
        Renderiza la pregunta actual en pantalla.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py (línea ~423) - En el método draw()
        
        Ejemplo:
            gestor.renderizar(screen)
        """
        if not self.pregunta_actual:
            return None
        
        # Obtener descripción de la pregunta
        descripcion = self.pregunta_actual.get("descripcion", "")
        
        # Posición centrada superior
        x_centro = pantalla.get_width() // 2
        y_pregunta = 120
        
        # Renderizar pregunta con sombra para mejor legibilidad
        dibujar_sombra_texto(
            pantalla,
            descripcion,
            (x_centro, y_pregunta),
            self.fuente_pregunta,
            self.color_pregunta
        )
        
        return None
    
    def resetear(self) -> None:
        """
        Resetea el estado del gestor para una nueva partida.
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py - Al reiniciar partida
        
        Ejemplo:
            gestor.resetear()
        """
        self.preguntas_usadas = []
        self.pregunta_actual = None
        self.nivel_actual = 1
        self.numero_pregunta_nivel = 0
        return None
