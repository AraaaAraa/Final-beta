# =============================================================================
# MODELO: PREGUNTA
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Modelo de datos que representa una pregunta del juego de trivia.
#    Define la estructura y operaciones básicas para trabajar con preguntas.
#    Incluye funciones para crear, validar y acceder a datos de preguntas.
#
# 📥 IMPORTADO EN:
#    - data/repositorio_preguntas.py (línea ~8) - para crear_pregunta
#    - data/repositorio_preguntas.py - para validar preguntas cargadas desde CSV
#
# 🔗 DEPENDENCIAS:
#    Ninguna (modelo de datos puro)
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Implementación basada en diccionarios para flexibilidad
#    - Validación manual de campos requeridos sin usar built-ins prohibidos
#    - Separación clara entre estructura de datos y lógica de negocio
#    - Función obtener_campo_pregunta implementa acceso seguro sin .get()
# =============================================================================

# =============================================================================
# CREAR_PREGUNTA
# =============================================================================
# 📄 Descripción: 
#    Crea un objeto pregunta con todos sus datos estructurados
# 
# 📥 Parámetros:
#    - id_pregunta (int): Identificador único de la pregunta
#    - nivel (int): Nivel de la pregunta (1, 2 o 3)
#    - descripcion (str): Texto de la pregunta
#    - dificultad (int): Dificultad (1=fácil, 2=medio, 3=difícil)
#    - categoria (str): Categoría temática de la pregunta
#    - opciones (list): Lista de opciones de respuesta
#    - respuesta_correcta (str): Respuesta correcta
#
# 📤 Retorna:
#    - dict: Diccionario con toda la información de la pregunta
#
# 🔧 Importado en:
#    - data/repositorio_preguntas.py (línea ~45) - para construir preguntas desde CSV
#
# 💡 Algoritmo:
#    - Paso 1: Crear diccionario vacío
#    - Paso 2: Asignar cada campo manualmente
#    - Paso 3: Retornar diccionario completo (un solo return)
#
# 📝 Ejemplo de uso:
#    pregunta = crear_pregunta(1, 1, "¿Quién era Zeus?", 2, "Mitología", 
#                              ["Dios", "Mortal", "Titán", "Héroe"], "Dios")
# =============================================================================
def crear_pregunta(id_pregunta: int, nivel: int, descripcion: str, 
                   dificultad: int, categoria: str, opciones: list, 
                   respuesta_correcta: str) -> dict:
    """Crea un objeto pregunta con todos sus datos."""
    pregunta = {}
    pregunta["id"] = id_pregunta
    pregunta["nivel"] = nivel
    pregunta["descripcion"] = descripcion
    pregunta["dificultad"] = dificultad
    pregunta["categoria"] = categoria
    pregunta["opciones"] = opciones
    pregunta["correcta"] = respuesta_correcta
    
    return pregunta


# =============================================================================
# VALIDAR_PREGUNTA
# =============================================================================
# 📄 Descripción: 
#    Verifica que una pregunta tenga todos los campos requeridos
# 
# 📥 Parámetros:
#    - pregunta (dict): Diccionario con datos de la pregunta
#
# 📤 Retorna:
#    - bool: True si la pregunta es válida, False en caso contrario
#
# 🔧 Importado en:
#    - data/repositorio_preguntas.py (línea ~60) - para validar preguntas cargadas
#
# 💡 Algoritmo:
#    - Paso 1: Definir lista de campos requeridos
#    - Paso 2: Para cada campo, buscar con bucle manual si existe en pregunta
#    - Paso 3: Si falta algún campo, retornar False
#    - Paso 4: Si todos existen, retornar True (un solo return al final)
#
# 📝 Ejemplo de uso:
#    if validar_pregunta(pregunta):
#        # usar pregunta
# =============================================================================
def validar_pregunta(pregunta: dict) -> bool:
    """Verifica que una pregunta tenga todos los campos requeridos."""
    campos_requeridos = ["id", "nivel", "descripcion", "dificultad", 
                        "categoria", "opciones", "correcta"]
    
    for campo in campos_requeridos:
        campo_existe = False
        for clave in pregunta:
            if clave == campo:
                campo_existe = True
                break
        if not campo_existe:
            return False
    
    return True


# =============================================================================
# OBTENER_CAMPO_PREGUNTA
# =============================================================================
# 📄 Descripción: 
#    Obtiene un campo específico de una pregunta de forma segura
# 
# 📥 Parámetros:
#    - pregunta (dict): Diccionario con datos de la pregunta
#    - campo (str): Nombre del campo a obtener
#    - default: Valor por defecto si el campo no existe
#
# 📤 Retorna:
#    - any: Valor del campo o default si no existe
#
# 🔧 Importado en:
#    - (Función auxiliar, puede ser usada en cualquier módulo que trabaje con preguntas)
#
# 💡 Algoritmo:
#    - Paso 1: Iterar manualmente sobre claves del diccionario
#    - Paso 2: Comparar cada clave con el campo buscado
#    - Paso 3: Si se encuentra, retornar valor; si no, retornar default (un solo return)
#
# 📝 Ejemplo de uso:
#    nivel = obtener_campo_pregunta(pregunta, "nivel", 1)
# =============================================================================
def obtener_campo_pregunta(pregunta: dict, campo: str, default=None):
    """Obtiene un campo específico de una pregunta de forma segura."""
    for clave in pregunta:
        if clave == campo:
            return pregunta[clave]
    return default
