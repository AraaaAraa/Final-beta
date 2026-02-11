# =============================================================================
# MÓDULO CORE - LÓGICA DE NEGOCIO
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Inicializa el paquete core que contiene toda la lógica de negocio del juego.
#    Completamente independiente de la interfaz de usuario (UI).
#
# 📥 IMPORTADO EN:
#    - Implícitamente cuando se importa el paquete core
#
# 🔗 DEPENDENCIAS:
#    Ninguna
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Separación estricta entre lógica (core) y presentación (ui)
#    - Sin imports de pygame en ningún módulo de core
#    - Permite reutilizar lógica en consola y pygame
#    - Facilita testing unitario sin necesidad de UI
#    - Arquitectura en capas: models -> data -> core -> ui
# =============================================================================
