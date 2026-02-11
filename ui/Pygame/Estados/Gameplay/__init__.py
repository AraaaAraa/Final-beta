# =============================================================================
# GAMEPLAY MODULE - INIT
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Módulo que contiene el estado principal del gameplay modularizado.
#
# 📥 IMPORTADO EN:
#    - ui/Pygame/Juego.py - Para crear estado de gameplay
#    - ui/Pygame/main.py - Para inicializar estados
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Estructura modular facilita mantenimiento
#    - Separación de responsabilidades (gestores especializados)
# =============================================================================

from .gameplay import gameplay

__all__ = ["gameplay"]
