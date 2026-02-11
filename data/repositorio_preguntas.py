# =============================================================================
# REPOSITORIO DE PREGUNTAS
# =============================================================================
# 📄 DESCRIPCIÓN:
#    Módulo para cargar y gestionar las preguntas del juego desde archivo CSV.
#    Incluye filtrado por nivel, selección aleatoria y mezclado de opciones.
#
# 📥 IMPORTADO EN:
#    - core/logica_juego.py (líneas 7-10) - para cargar_preguntas_desde_csv, filtrar_preguntas_por_nivel, seleccionar_pregunta_aleatoria
#    - ui/Pygame/Estados/Gameplay.py (línea 13) - para cargar_preguntas_desde_csv
#    - ui/consola/juego_consola.py - para cargar preguntas en UI de consola
#
# 🔗 DEPENDENCIAS:
#    - random: para selección aleatoria y mezcla de opciones
#    - data/archivos_json: para verificar_y_obtener_ruta
#    - models/pregunta: para crear_pregunta
#    - config/constantes: para RUTA_PREGUNTAS
#
# 💡 NOTAS PARA LA DEFENSA:
#    - Carga de CSV implementada manualmente (sin pandas)
#    - Algoritmo Fisher-Yates manual para mezclar opciones
#    - Filtrado manual de preguntas sin usar filter()
#    - Selección aleatoria por categoría para variedad
#    - Búsqueda manual de preguntas usadas sin usar 'in'
# =============================================================================

import random
from data.archivos_json import verificar_y_obtener_ruta
from models.pregunta import crear_pregunta
from config.constantes import RUTA_PREGUNTAS

# =============================================================================
# CARGAR_PREGUNTAS_DESDE_CSV
# =============================================================================
# Descripción: Carga todas las preguntas desde el archivo CSV
# 
# Uso en Pygame: Se usa igual al iniciar el juego
#
# Parámetros:
#   - path (str): Ruta al archivo CSV de preguntas
#
# Retorna:
#   - dict: Diccionario de preguntas indexadas por ID
#
# Ejemplo de uso:
#   preguntas = cargar_preguntas_desde_csv("preguntas.csv")
# =============================================================================
def cargar_preguntas_desde_csv(path: str) -> dict:
    """Carga todas las preguntas desde el archivo CSV."""
    preguntas = {}
    abs_path = verificar_y_obtener_ruta(path)
    if abs_path != "":
        with open(abs_path, encoding="utf-8") as f:
            encabezado = f.readline()
            for linea in f:
                fila = linea.strip().split(",")
                if len(fila) >= 10:
                    pregunta = procesar_linea_csv(fila)
                    if "id" in pregunta:
                        preguntas[pregunta["id"]] = {
                            "nivel": pregunta["nivel"],
                            "descripcion": pregunta["descripcion"],
                            "dificultad": pregunta["dificultad"],
                            "categoria": pregunta["categoria"],
                            "opciones": pregunta["opciones"],
                            "correcta": pregunta["correcta"]
                        }
    return preguntas


# =============================================================================
# PROCESAR_LINEA_CSV
# =============================================================================
# Descripción: Procesa una línea del CSV y crea una pregunta
# 
# Uso en Pygame: Se usa internamente al cargar preguntas
#
# Parámetros:
#   - fila (list): Lista con los campos de la pregunta
#
# Retorna:
#   - dict: Pregunta procesada o dict vacío si hay error
#
# Ejemplo de uso:
#   pregunta = procesar_linea_csv(fila_csv)
# =============================================================================
def procesar_linea_csv(fila: list) -> dict:
    """Procesa una línea del CSV y crea una pregunta."""
    try:
        pid = int(fila[0])
        nivel = int(fila[1])
        descripcion = fila[2].strip('"')
        dificultad = int(fila[3])
        categoria = fila[4]
        opcion_correcta = int(fila[5])
        opciones = (fila[6], fila[7], fila[8], fila[9])
        if 1 <= opcion_correcta <= 4:
            respuesta_correcta = opciones[opcion_correcta - 1]
        else:
            respuesta_correcta = opciones[0]
        opciones_mezcladas = mezclar_opciones(list(opciones))
        pregunta = {
            "id": pid,
            "nivel": nivel,
            "descripcion": descripcion,
            "dificultad": dificultad,
            "categoria": categoria,
            "opciones": opciones_mezcladas,
            "correcta": respuesta_correcta
        }
        return pregunta
    except Exception:
        return {}


# =============================================================================
# MEZCLAR_OPCIONES
# =============================================================================
# Descripción: Mezcla las opciones de una pregunta (algoritmo Fisher-Yates manual)
# 
# Uso en Pygame: Se usa igual para randomizar opciones
#
# Parámetros:
#   - opciones (list): Lista de opciones a mezclar
#
# Retorna:
#   - list: Lista de opciones mezcladas
#
# Ejemplo de uso:
#   opciones_mezcladas = mezclar_opciones(["A", "B", "C", "D"])
# =============================================================================
def mezclar_opciones(opciones: list) -> list:
    """Mezcla las opciones de una pregunta usando Fisher-Yates."""
    mezcladas = opciones[:]
    i = len(mezcladas) - 1
    while i > 0:
        j = random.randint(0, i)
        temp = mezcladas[i]
        mezcladas[i] = mezcladas[j]
        mezcladas[j] = temp
        i = i - 1
    return mezcladas


# =============================================================================
# FILTRAR_PREGUNTAS_POR_NIVEL
# =============================================================================
# Descripción: Filtra preguntas que correspondan a un nivel específico
# 
# Uso en Pygame: Se usa igual para seleccionar preguntas del nivel
#
# Parámetros:
#   - preguntas (dict): Diccionario completo de preguntas
#   - nivel (int): Nivel a filtrar (1, 2, o 3)
#   - preguntas_usadas (list): IDs de preguntas ya usadas (opcional)
#
# Retorna:
#   - dict: Diccionario con solo las preguntas del nivel solicitado
#
# Ejemplo de uso:
#   preguntas_nivel_1 = filtrar_preguntas_por_nivel(preguntas, 1, [])
# =============================================================================
def filtrar_preguntas_por_nivel(preguntas: dict, nivel: int, preguntas_usadas: list = None) -> dict:
    """Filtra preguntas que correspondan a un nivel específico."""
    if preguntas_usadas is None:
        preguntas_usadas = []
    
    disponibles = {}
    for pid, pregunta in preguntas.items():
        esta_usada = False
        for usada in preguntas_usadas:
            if usada == pid:
                esta_usada = True
                break

        if pregunta['nivel'] == nivel and not esta_usada:
            disponibles[pid] = pregunta

    return disponibles


# =============================================================================
# SELECCIONAR_PREGUNTA_ALEATORIA
# =============================================================================
# Descripción: Selecciona una pregunta aleatoria de las disponibles
# 
# Uso en Pygame: Se usa igual para obtener pregunta siguiente
#
# Parámetros:
#   - preguntas_disponibles (dict): Preguntas disponibles para elegir
#
# Retorna:
#   - dict: Pregunta seleccionada con su ID, o dict vacío si no hay
#
# Ejemplo de uso:
#   pregunta = seleccionar_pregunta_aleatoria(preguntas_nivel_1)
# =============================================================================
def seleccionar_pregunta_aleatoria(preguntas_disponibles: dict) -> dict:
    """Selecciona una pregunta aleatoria de las disponibles."""
    if not preguntas_disponibles:
        return {}

    categorias = []
    for p in preguntas_disponibles.values():
        ya_esta = False
        for c in categorias:
            if c == p['categoria']:
                ya_esta = True
                break
        if not ya_esta:
            categorias.append(p['categoria'])

    categoria = random.choice(categorias)

    candidatas = []
    for pid, p in preguntas_disponibles.items():
        if p['categoria'] == categoria:
            candidatas.append(pid)

    id_pregunta = random.choice(candidatas)

    dicc = {"id": id_pregunta}
    for k in preguntas_disponibles[id_pregunta]:
        dicc[k] = preguntas_disponibles[id_pregunta][k]

    return dicc
