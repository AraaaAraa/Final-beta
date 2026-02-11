# =============================================================================
# MÓDULO DE CAPA DE DATOS
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Inicializa el paquete de capa de datos (Data Layer).
#    Contiene repositorios para usuarios, preguntas y operaciones con archivos.
#
# 📥 IMPORTADO EN:
#    - Implícitamente cuando se importa el paquete data
#
# 🔗 DEPENDENCIAS:
#    Ninguna
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Implementa patrón Repository para abstracción de persistencia
#    - Separa lógica de datos de lógica de negocio (core)
#    - Facilita testing al poder mockear repositorios
#    - Permite cambiar fuente de datos sin afectar core
# =============================================================================
