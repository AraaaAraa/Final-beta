# =============================================================================
# COMPONENTES REUTILIZABLES - INIT
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Inicializa el módulo de componentes reutilizables de Pygame.
#
# 📥 IMPORTADO EN:
#    - ui/Pygame/Estados/Menu.py
#    - ui/Pygame/Estados/Gameplay/gameplay.py
#    - ui/Pygame/Estados/Rankings.py
#    - ui/Pygame/Estados/Game_Over.py
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Facilita importaciones de componentes
#    - Permite usar: from ui.Pygame.componentes import Boton
# =============================================================================

from .boton import Boton

__all__ = ["Boton"]
