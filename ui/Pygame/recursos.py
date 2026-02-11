# =============================================================================
# MÓDULO DE RECURSOS
# =============================================================================
# Maneja la carga de recursos (fuentes e imágenes) para Pygame
# =============================================================================

import pygame
import os

# Rutas base
BASE_DIR = os.path.dirname(__file__)
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
IMAGES_DIR = os.path.join(BASE_DIR, "imagenes")

# ⬅️ FUENTE PRINCIPAL DEL JUEGO
FUENTE_PRINCIPAL = "Jacquard12-Regular.ttf"  # ⬅️ Cambiar a .otf si es necesario

# Cache global de imágenes
_cache_imagenes = {}


def cargar_fuente(nombre: str, tamaño: int) -> pygame.font.Font:
    """
    Carga una fuente desde el directorio de fuentes.
    
    Parámetros:
        nombre (str): Nombre del archivo de fuente
        tamaño (int): Tamaño de la fuente
    
    Retorna:
        pygame.font.Font: Fuente cargada o fuente por defecto si no existe
    """
    ruta = os.path.join(FONTS_DIR, nombre)
    if os.path.exists(ruta):
        return pygame.font.Font(ruta, tamaño)
    else:
        print(f"⚠️ Fuente no encontrada: {ruta}, usando fuente por defecto")
        return pygame.font.Font(None, tamaño)


# ⬅️ FUNCIÓN HELPER PARA CARGAR LA FUENTE PRINCIPAL
def cargar_fuente_principal(tamaño: int) -> pygame.font.Font:
    """
    Carga la fuente principal del juego (Jacquard12-Regular).
    
    Parámetros:
        tamaño (int): Tamaño de la fuente
    
    Retorna:
        pygame.font.Font: Fuente principal cargada
    """
    return cargar_fuente(FUENTE_PRINCIPAL, tamaño)


def cargar_imagen(nombre: str, escalar: tuple = None) -> pygame.Surface:
    """
    Carga una imagen desde el directorio de imágenes con cache.
    
    Parámetros:
        nombre (str): Nombre del archivo de imagen
        escalar (tuple): Opcional, dimensiones (ancho, alto) para escalar
    
    Retorna:
        pygame.Surface: Imagen cargada o superficie magenta si no existe
    """
    # Crear clave de cache única
    cache_key = f"{nombre}_{escalar}" if escalar else nombre
    
    # Verificar si ya está en cache
    if cache_key in _cache_imagenes:
        return _cache_imagenes[cache_key].copy()
    
    ruta = os.path.join(IMAGES_DIR, nombre)
    if os.path.exists(ruta):
        imagen = pygame.image.load(ruta).convert_alpha()
        if escalar:
            imagen = pygame.transform.scale(imagen, escalar)
        
        # Guardar en cache
        _cache_imagenes[cache_key] = imagen
        return imagen.copy()
    else:
        # Crear superficie de placeholder magenta si no existe la imagen
        print(f"⚠️ Imagen no encontrada: {ruta}, usando placeholder")
        tamaño = escalar if escalar else (100, 100)
        img = pygame.Surface(tamaño)
        img.fill((255, 0, 255))
        
        # Guardar placeholder en cache
        _cache_imagenes[cache_key] = img
        return img.copy()


def limpiar_cache_imagenes():
    """Limpia el cache de imágenes para liberar memoria."""
    global _cache_imagenes
    _cache_imagenes.clear()