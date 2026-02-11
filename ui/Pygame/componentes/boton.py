# =============================================================================
# COMPONENTE: BOTÓN REUTILIZABLE
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Componente de botón para reutilizar en todos los estados.
#    Maneja renderizado, detección de clicks y estados visuales.
#
# 📥 USADO EN:
#    - Estados/Menu.py
#    - Estados/Gameplay/gestor_respuestas.py
#    - Estados/Rankings.py
#    - Estados/Game_Over.py
#    - Estados/SeleccionObjeto.py
#    - Estados/Historia.py
#
# 💡 BENEFICIO:
#    Evita duplicar código de botones en cada estado. Proporciona una
#    interfaz consistente para manejar interacciones del usuario.
#
# 🔗 DEPENDENCIAS:
#    - pygame: Para renderizado y geometría
#    - ui.Pygame.recursos: cargar_imagen para imágenes de botón
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Implementa patrón de componente reutilizable
#    - Encapsula lógica de hover y detección de clicks
#    - Usa imágenes para dar estilo visual a los botones
#    - Mantiene un solo return por función (principio del proyecto)
# =============================================================================

import pygame
from ..recursos import cargar_imagen


class Boton:
    """Componente reutilizable de botón con soporte para imágenes y hover."""
    
    def __init__(self, x: int, y: int, ancho: int, alto: int, texto: str, 
                 fuente: pygame.font.Font, color_texto: tuple = (255, 255, 255)):
        """
        Inicializa un botón.
        
        Args:
            x (int): Posición X del botón
            y (int): Posición Y del botón
            ancho (int): Ancho del botón en píxeles
            alto (int): Alto del botón en píxeles
            texto (str): Texto a mostrar en el botón
            fuente (pygame.font.Font): Fuente para el texto
            color_texto (tuple): Color RGB del texto (por defecto blanco)
        
        Returns:
            None
        
        Usado en:
            - Menu.py - Crear botones de menú principal
            - Gameplay/gestor_respuestas.py - Crear botones de opciones
            - Rankings.py - Crear botón de volver
            - Game_Over.py - Crear botones de reintentar/menú
        
        Ejemplo:
            fuente = pygame.font.Font(None, 32)
            boton = Boton(100, 200, 200, 60, "JUGAR", fuente)
        """
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.fuente = fuente
        self.color_texto = color_texto
        
        # Cargar imágenes de botón
        self.imagen_normal = cargar_imagen("BotonNormal.png", escalar=(ancho, alto))
        self.imagen_hover = cargar_imagen("BotonOscuro.png", escalar=(ancho, alto))
        
        # Estado del botón
        self.esta_hover = False
        self.activo = True
        
        return None
    
    def actualizar(self, pos_mouse: tuple) -> None:
        """
        Actualiza estado hover del botón.
        
        Args:
            pos_mouse (tuple): Posición (x, y) del mouse
        
        Returns:
            None
        
        Usado en:
            - Menu.py (línea ~100) - Actualizar hover en game loop
            - Gameplay/gestor_respuestas.py - Actualizar hover de opciones
        
        Ejemplo:
            pos = pygame.mouse.get_pos()
            boton.actualizar(pos)
        """
        if self.activo and self.rect.collidepoint(pos_mouse):
            self.esta_hover = True
        else:
            self.esta_hover = False
        
        return None
    
    def fue_clickeado(self, pos_click: tuple) -> bool:
        """
        Verifica si el botón fue clickeado.
        
        Args:
            pos_click (tuple): Posición (x, y) del click
        
        Returns:
            bool: True si fue clickeado, False si no
        
        Usado en:
            - Menu.py (línea ~75) - Detectar clicks en botones de menú
            - Gameplay/gestor_respuestas.py - Detectar respuesta seleccionada
            - Rankings.py - Detectar click en botón volver
        
        Ejemplo:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton.fue_clickeado(evento.pos):
                    print("Botón clickeado!")
        """
        if self.activo and self.rect.collidepoint(pos_click):
            resultado = True
        else:
            resultado = False
        
        return resultado
    
    def renderizar(self, pantalla: pygame.Surface) -> None:
        """
        Dibuja el botón en pantalla.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
        
        Returns:
            None
        
        Usado en:
            - Menu.py (línea ~120) - Renderizar botones en draw()
            - Gameplay/gestor_respuestas.py - Renderizar opciones
            - Rankings.py - Renderizar botón volver
        
        Ejemplo:
            boton.renderizar(screen)
        """
        # Elegir imagen según hover y estado activo
        if self.esta_hover or not self.activo:
            imagen_actual = self.imagen_hover
        else:
            imagen_actual = self.imagen_normal
        
        # Dibujar imagen del botón
        pantalla.blit(imagen_actual, self.rect.topleft)
        
        # Renderizar texto centrado
        superficie_texto = self.fuente.render(self.texto, True, self.color_texto)
        rect_texto = superficie_texto.get_rect(center=(self.rect.centerx, self.rect.centery - 10))
        
        # Si el botón está inactivo, hacer el texto más oscuro
        if not self.activo:
            # Crear superficie semi-transparente
            texto_surface = pygame.Surface(superficie_texto.get_size(), pygame.SRCALPHA)
            texto_surface.blit(superficie_texto, (0, 0))
            texto_surface.set_alpha(128)
            pantalla.blit(texto_surface, rect_texto)
        else:
            pantalla.blit(superficie_texto, rect_texto)
        
        return None
    
    def set_activo(self, activo: bool) -> None:
        """
        Establece si el botón está activo o no.
        
        Args:
            activo (bool): True si el botón debe estar activo
        
        Returns:
            None
        
        Usado en:
            - Gameplay.py - Desactivar botones durante animaciones
        
        Ejemplo:
            boton.set_activo(False)  # Desactivar
        """
        self.activo = activo
        return None
