import sys
import os
from pathlib import Path

# ============================================
# CONFIGURACIÓN DE PATHS PARA IMPORTS
# ============================================
ruta_actual = Path(__file__).resolve()
ruta_proyecto = ruta_actual.parent.parent.parent

if str(ruta_proyecto) not in sys.path:
    sys.path.insert(0, str(ruta_proyecto))

# ============================================
# IMPORTS DEL JUEGO
# ============================================
import pygame
from ui.Pygame.Estados.Game_Over import gameOver
from ui.Pygame.Estados.Menu import menu
from ui.Pygame.Estados.Gameplay import gameplay
from ui.Pygame.Estados.Historia import historia
from ui.Pygame.Estados.Splash import splash
from ui.Pygame.Estados.Minijuego import minijuego
from ui.Pygame.Estados.Rankings import rankings
from ui.Pygame.Estados.SeleccionObjeto import seleccionObjeto  # ⬅️ NUEVO IMPORT
from config.constantes import ANCHO, ALTO, FPS
from ui.Pygame.Juego import juego

# ============================================
# INICIALIZACIÓN Y EJECUCIÓN
# ============================================
pygame.init()

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Trivia Mitológica")

estados = {
    "Menu": menu(),
    "Gameplay": gameplay(),
    "Historia": historia(),
    "Gameover": gameOver(),
    "Splash": splash(),
    "Minijuego": minijuego(),
    "Rankings": rankings(),
    "SeleccionObjeto": seleccionObjeto()  # ⬅️ NUEVO ESTADO
}

# Inicia con Historia
Juego = juego(pantalla, estados, "Historia", FPS)
Juego.run()

pygame.quit()
sys.exit()