# =============================================================================
# UTILIDADES PYGAME - INIT
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Inicializa el módulo de utilidades de Pygame.
#
# 📥 IMPORTADO EN:
#    - ui/Pygame/Estados/Gameplay/gameplay.py
#    - ui/Pygame/Estados/Menu.py
#    - ui/Pygame/Estados/Rankings.py
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Facilita importaciones de utilidades
#    - Permite usar: from ui.Pygame.utils import renderizar_texto
# =============================================================================

from .renderizado import (
    renderizar_texto,
    renderizar_rectangulo_con_borde,
    limpiar_pantalla
)
from .eventos import (
    detectar_click_en_botones,
    obtener_posicion_mouse
)

__all__ = [
    "renderizar_texto",
    "renderizar_rectangulo_con_borde",
    "limpiar_pantalla",
    "detectar_click_en_botones",
    "obtener_posicion_mouse"
]
