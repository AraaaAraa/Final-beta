# =============================================================================
# GESTOR DE HUD (Heads-Up Display)
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Responsable de mostrar y actualizar información del juego en pantalla:
#    puntos, nivel, racha, errores, objetos equipados y vidas extra.
#
# 🔗 DEPENDENCIAS CORE:
#    - core/logica_buffeos.py: verificar_objeto_equipado()
#
# 🔗 DEPENDENCIAS PYGAME:
#    - pygame: Para renderizado de texto
#
# 💡 RESPONSABILIDAD ÚNICA:
#    Solo maneja visualización de estadísticas en pantalla.
#    NO procesa lógica del juego, solo muestra información.
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Patrón de separación de responsabilidades
#    - Vista pura: solo renderiza, no modifica estado
#    - Recibe datos, no los calcula
#    - Un solo return por función
# =============================================================================

import pygame
from core.logica_buffeos import verificar_objeto_equipado
from config.constantes import PREGUNTAS_POR_NIVEL, MAX_ERRORES_PERMITIDOS


class GestorHUD:
    """Gestiona visualización de puntos, nivel, racha, errores y objetos."""
    
    def __init__(self, fuente_stats: pygame.font.Font, fuente_buffeo: pygame.font.Font):
        """
        Inicializa el HUD.
        
        Args:
            fuente_stats (pygame.font.Font): Fuente para estadísticas principales
            fuente_buffeo (pygame.font.Font): Fuente para información de buffeo
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py (línea ~42) - Crear gestor al inicializar
        
        Ejemplo:
            fuente_stats = pygame.font.Font(None, 30)
            fuente_buffeo = pygame.font.Font(None, 24)
            hud = GestorHUD(fuente_stats, fuente_buffeo)
        """
        self.nombre_usuario = ""
        self.puntos_totales = 0
        self.nivel_actual = 1
        self.numero_pregunta_nivel = 0
        self.racha_actual = 0
        self.errores = 0
        self.vidas_extra_iniciales = 0
        self.max_errores_con_vidas = MAX_ERRORES_PERMITIDOS
        self.buffeo_activo = False
        
        # Configuración de renderizado
        self.fuente_stats = fuente_stats
        self.fuente_buffeo = fuente_buffeo
        
        # Colores
        self.color_texto = (255, 255, 255)
        self.color_puntos = (255, 215, 0)
        self.color_buffeo = (255, 215, 0)
        self.color_incorrecto = (255, 100, 100)
        self.color_objeto = (150, 255, 150)
        
        return None
    
    def inicializar(self, nombre_usuario: str, vidas_extra: int, max_errores: int) -> None:
        """
        Inicializa HUD para nueva partida.
        
        Args:
            nombre_usuario (str): Nombre del jugador
            vidas_extra (int): Vidas extra iniciales del jugador
            max_errores (int): Máximo de errores permitidos (base + vidas extra)
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py (línea ~101) - Al iniciar partida
        
        Ejemplo:
            hud.inicializar("Jugador1", 2, 4)
        """
        self.nombre_usuario = nombre_usuario
        self.puntos_totales = 0
        self.nivel_actual = 1
        self.numero_pregunta_nivel = 0
        self.racha_actual = 0
        self.errores = 0
        self.vidas_extra_iniciales = vidas_extra
        self.max_errores_con_vidas = max_errores
        self.buffeo_activo = False
        return None
    
    def actualizar_puntos(self, puntos: int) -> None:
        """
        Actualiza puntos totales.
        
        Args:
            puntos (int): Puntos a agregar
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gestor_respuestas.py - Al procesar respuesta correcta
        
        Ejemplo:
            hud.actualizar_puntos(5)
        """
        self.puntos_totales = self.puntos_totales + puntos
        return None
    
    def actualizar_racha(self, es_correcta: bool) -> None:
        """
        Actualiza racha según si la respuesta fue correcta.
        
        Args:
            es_correcta (bool): True si la respuesta fue correcta
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gestor_respuestas.py - Al procesar respuesta
        
        Ejemplo:
            hud.actualizar_racha(True)  # Incrementa racha
            hud.actualizar_racha(False)  # Resetea racha
        """
        if es_correcta:
            self.racha_actual = self.racha_actual + 1
        else:
            self.racha_actual = 0
        
        return None
    
    def incrementar_errores(self) -> None:
        """
        Incrementa contador de errores.
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gestor_respuestas.py - Al procesar respuesta incorrecta
        
        Ejemplo:
            hud.incrementar_errores()
        """
        self.errores = self.errores + 1
        return None
    
    def actualizar_nivel_y_pregunta(self, nivel: int, numero_pregunta: int) -> None:
        """
        Actualiza nivel y número de pregunta actual.
        
        Args:
            nivel (int): Nivel actual (1, 2, 3)
            numero_pregunta (int): Número de pregunta en el nivel actual
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py - Al cambiar de pregunta
        
        Ejemplo:
            hud.actualizar_nivel_y_pregunta(2, 1)
        """
        self.nivel_actual = nivel
        self.numero_pregunta_nivel = numero_pregunta
        return None
    
    def set_buffeo_activo(self, activo: bool) -> None:
        """
        Establece si hay buffeo activo (para cambiar color de racha).
        
        Args:
            activo (bool): True si hay buffeo activo
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py - Al actualizar buffeo
        
        Ejemplo:
            hud.set_buffeo_activo(True)
        """
        self.buffeo_activo = activo
        return None
    
    def juego_terminado(self) -> bool:
        """
        Verifica si el juego debe terminar por errores.
        
        Returns:
            bool: True si se alcanzó el máximo de errores
        
        Usado en:
            - Estados/Gameplay/gameplay.py - Al verificar condición de fin
        
        Ejemplo:
            if hud.juego_terminado():
                print("Game Over")
        """
        if self.errores >= self.max_errores_con_vidas:
            terminado = True
        else:
            terminado = False
        
        return terminado
    
    def renderizar(self, pantalla: pygame.Surface) -> None:
        """
        Renderiza HUD en pantalla.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
        
        Returns:
            None
        
        Usado en:
            - Estados/Gameplay/gameplay.py (línea ~415) - En el método draw()
        
        Ejemplo:
            hud.renderizar(screen)
        """
        y = 20
        
        # Nivel y progreso
        nivel_text = f"Nivel {self.nivel_actual} - Pregunta {self.numero_pregunta_nivel}/{PREGUNTAS_POR_NIVEL.get(self.nivel_actual, 0)}"
        nivel_render = self.fuente_stats.render(nivel_text, True, self.color_texto)
        pantalla.blit(nivel_render, (20, y))
        
        # Puntos
        puntos_text = f"Puntos: {self.puntos_totales}"
        puntos_render = self.fuente_stats.render(puntos_text, True, self.color_puntos)
        pantalla.blit(puntos_render, (400, y))
        
        y = y + 35
        
        # Racha (con color especial si hay buffeo)
        racha_text = f"Racha: {self.racha_actual}"
        if self.buffeo_activo:
            color_racha = self.color_buffeo
        else:
            color_racha = self.color_texto
        
        racha_render = self.fuente_stats.render(racha_text, True, color_racha)
        pantalla.blit(racha_render, (20, y))
        
        # Errores con vidas extra
        errores_text = f"Errores: {self.errores}/{self.max_errores_con_vidas}"
        
        # Si tiene vidas extra, mostrar desglose
        if self.vidas_extra_iniciales > 0:
            vidas_usadas = max(0, self.errores - MAX_ERRORES_PERMITIDOS)
            vidas_restantes = self.vidas_extra_iniciales - vidas_usadas
            errores_text = errores_text + f" (+{vidas_restantes} vidas)"
        
        if self.errores > 0:
            color_error = self.color_incorrecto
        else:
            color_error = self.color_texto
        
        errores_render = self.fuente_stats.render(errores_text, True, color_error)
        pantalla.blit(errores_render, (400, y))
        
        # Mostrar objeto equipado si existe
        objeto = verificar_objeto_equipado(self.nombre_usuario)
        if objeto:
            y = y + 35
            
            # Mapeo de nombres de objetos para display
            if objeto == "espada":
                nombre_display = "Espada"
            elif objeto == "armadura":
                nombre_display = "Armadura"
            elif objeto == "raciones":
                nombre_display = "Raciones"
            elif objeto == "bolsa_monedas":
                nombre_display = "Bolsa"
            else:
                nombre_display = objeto.capitalize()
            
            objeto_text = f"Objeto: {nombre_display}"
            objeto_render = self.fuente_buffeo.render(objeto_text, True, self.color_objeto)
            pantalla.blit(objeto_render, (20, y))
        
        return None
