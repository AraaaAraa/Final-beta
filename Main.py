# =============================================================================
# MAIN - PUNTO DE ENTRADA
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Punto de entrada mínimo del programa. Delega toda la lógica a los
#    módulos correspondientes manteniendo este archivo simple y limpio.
#
# 📥 IMPORTADO EN:
#    - Ejecutado directamente como script principal
#
# 🔗 DEPENDENCIAS:
#    - ui/consola/menu_consola: para ejecutar_menu_consola
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Punto de entrada simple que delega responsabilidades
#    - Facilita cambiar entre UI de consola y pygame
#    - Toda la lógica está en módulos especializados
#    - Patrón común en aplicaciones bien estructuradas
# =============================================================================

from ui.consola.menu_consola import ejecutar_menu_consola

def main():
    """Punto de entrada del programa."""
    ejecutar_menu_consola()

if __name__ == "__main__":
    main()


