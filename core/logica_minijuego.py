# =============================================================================
# LÓGICA DEL MINIJUEGO
# =============================================================================
# Lógica del minijuego "Guardianes de Piedra" sin UI
# =============================================================================

import random
from config.constantes import TAMAÑO_MATRIZ_MINIJUEGO

# =============================================================================
# GENERAR_MATRIZ_RESOLUBLE
# =============================================================================
# Descripción: Genera una matriz con solución garantizada
# 
# Uso en Pygame: Se usa igual para generar el tablero del minijuego
#
# Parámetros:
#   - tamano (int): Tamaño de la matriz (NxN)
#
# Retorna:
#   - list: Matriz 2D con valores
#
# Ejemplo de uso:
#   matriz = generar_matriz_resoluble(5)
# =============================================================================
def generar_matriz_resoluble(tamano: int) -> list:
    """Genera una matriz con solución garantizada."""
    matriz = inicializar_matriz_vacia(tamano)
    camino = generar_camino_garantizado(tamano)
    asignar_valores_a_camino(matriz, camino)
    rellenar_matriz_con_valores_seguro(matriz, camino)
    matriz_final = matriz
    return matriz_final


# =============================================================================
# INICIALIZAR_MATRIZ_VACIA
# =============================================================================
# Descripción: Crea una matriz NxN llena de ceros
# 
# Uso en Pygame: Se usa internamente al generar matriz
#
# Parámetros:
#   - tamano (int): Tamaño de la matriz
#
# Retorna:
#   - list: Matriz 2D de ceros
#
# Ejemplo de uso:
#   matriz = inicializar_matriz_vacia(5)
# =============================================================================
def inicializar_matriz_vacia(tamano: int) -> list:
    """Crea una matriz NxN llena de ceros."""
    matriz = []
    fila_idx = 0
    while fila_idx < tamano:
        fila = []
        col_idx = 0
        while col_idx < tamano:
            fila.append(0)
            col_idx += 1
        matriz.append(fila)
        fila_idx += 1
    return matriz


# =============================================================================
# GENERAR_CAMINO_GARANTIZADO
# =============================================================================
# Descripción: Genera un camino garantizado desde (0,0) hasta la esquina final
# 
# Uso en Pygame: Se usa internamente para asegurar solución
#
# Parámetros:
#   - tamano (int): Tamaño de la matriz
#   - fila (int): Fila actual (default: 0)
#   - col (int): Columna actual (default: 0)
#   - camino (list): Camino acumulado (default: [])
#
# Retorna:
#   - list: Lista de tuplas (fila, col) que forman el camino
#
# Ejemplo de uso:
#   camino = generar_camino_garantizado(5)
# =============================================================================
def generar_camino_garantizado(tamano: int, fila=0, col=0, camino=[]) -> list:
    """Genera un camino garantizado recursivamente."""
    if not camino:  
        camino = []
    
    camino.append((fila, col))
    
    if (fila, col) == (tamano - 1, tamano - 1):
        return camino
    opciones = []
    if fila + 1 < tamano:
        opciones.append((fila + 1, col))
    if col + 1 < tamano:
        opciones.append((fila, col + 1))
    if fila + 1 < tamano and col + 1 < tamano:
        opciones.append((fila + 1, col + 1))
    
    nueva_fila, nueva_col = random.choice(opciones)
    return generar_camino_garantizado(tamano, nueva_fila, nueva_col, camino)


# =============================================================================
# ASIGNAR_VALORES_A_CAMINO
# =============================================================================
# Descripción: Asigna valores crecientes a las celdas del camino
# 
# Uso en Pygame: Se usa internamente al generar matriz
#
# Parámetros:
#   - matriz (list): Matriz a modificar
#   - camino (list): Camino garantizado
#
# Retorna:
#   - None (modifica la matriz in-place)
#
# Ejemplo de uso:
#   asignar_valores_a_camino(matriz, camino)
# =============================================================================
def asignar_valores_a_camino(matriz: list, camino: list):
    """Asigna valores crecientes a las celdas del camino."""
    valor = random.randint(10, 20)
    for fila, col in camino:
        matriz[fila][col] = valor
        valor += random.randint(1, 5)


# =============================================================================
# RELLENAR_MATRIZ_CON_VALORES_SEGURO
# =============================================================================
# Descripción: Rellena el resto de la matriz con valores seguros
# 
# Uso en Pygame: Se usa internamente al generar matriz
#
# Parámetros:
#   - matriz (list): Matriz a rellenar
#   - camino (list): Camino garantizado (no modificar)
#
# Retorna:
#   - None (modifica la matriz in-place)
#
# Ejemplo de uso:
#   rellenar_matriz_con_valores_seguro(matriz, camino)
# =============================================================================
def rellenar_matriz_con_valores_seguro(matriz: list, camino: list):
    """Rellena el resto de la matriz con valores seguros."""
    tamano = len(matriz)
    for i in range(tamano):
        for j in range(tamano):
            if (i, j) not in camino:
                vecinos = obtener_valores_vecinos_no_nulos(matriz, i, j)
                if vecinos:
                    min_vecino = min(vecinos)
                    matriz[i][j] = random.randint(10, min_vecino + 10)
                else:
                    matriz[i][j] = random.randint(10, 50)


# =============================================================================
# OBTENER_VALORES_VECINOS_NO_NULOS
# =============================================================================
# Descripción: Obtiene los valores de los vecinos no nulos de una celda
# 
# Uso en Pygame: Se usa internamente para rellenar matriz
#
# Parámetros:
#   - matriz (list): Matriz
#   - fila (int): Fila de la celda
#   - col (int): Columna de la celda
#
# Retorna:
#   - list: Lista de valores vecinos no nulos
#
# Ejemplo de uso:
#   vecinos = obtener_valores_vecinos_no_nulos(matriz, 2, 3)
# =============================================================================
def obtener_valores_vecinos_no_nulos(matriz: list, fila: int, col: int) -> list:
    """Obtiene los valores de los vecinos no nulos de una celda."""
    tamano = len(matriz)
    vecinos = [
        (fila - 1, col), (fila + 1, col),
        (fila, col - 1), (fila, col + 1),
        (fila - 1, col - 1), (fila - 1, col + 1),
        (fila + 1, col - 1), (fila + 1, col + 1)
    ]

    vecinos_validos = [
        matriz[x][y]
        for x, y in vecinos
        if 0 <= x < tamano and 0 <= y < tamano and matriz[x][y] != 0
    ]
    return vecinos_validos


# =============================================================================
# OBTENER_MOVIMIENTOS_VALIDOS
# =============================================================================
# Descripción: Obtiene los movimientos válidos desde una posición
# 
# Uso en Pygame: Se usa para mostrar opciones disponibles al jugador
#
# Parámetros:
#   - matriz (list): Matriz del juego
#   - pos_actual (tuple): Posición actual (fila, col)
#   - valor_actual (int): Valor de la posición actual
#
# Retorna:
#   - list: Lista de tuplas (fila, col, indice, simbolo) con movimientos válidos
#
# Ejemplo de uso:
#   movimientos = obtener_movimientos_validos(matriz, (0, 0), 15)
# =============================================================================
def obtener_movimientos_validos(matriz, pos_actual, valor_actual):
    """Obtiene los movimientos válidos desde una posición."""
    fila, col = pos_actual
    movimientos = []
    direcciones = [
        (-1, -1, "↖"), (-1, 0, "↑"), (-1, 1, "↗"),
        (0, -1, "←"),                  (0, 1, "→"),
        (1, -1, "↙"),  (1, 0, "↓"),  (1, 1, "↘")
    ]
    
    indice_movimiento = 1
    for direccion_fila, direccion_columna, simbolo in direcciones:
        nueva_fila, nueva_col = fila + direccion_fila, col + direccion_columna
        if (0 <= nueva_fila < len(matriz) and 
            0 <= nueva_col < len(matriz[0])):
            nuevo_valor = matriz[nueva_fila][nueva_col]
            if nuevo_valor > valor_actual:
                movimientos.append((nueva_fila, nueva_col, indice_movimiento, simbolo))
                indice_movimiento += 1
    
    return movimientos


# =============================================================================
# VALIDAR_MOVIMIENTO
# =============================================================================
# Descripción: Valida si un movimiento es válido
# 
# Uso en Pygame: Se usa para validar clics/selecciones del jugador
#
# Parámetros:
#   - opcion (int): Número de opción seleccionada
#   - movimientos_validos (list): Lista de movimientos válidos
#
# Retorna:
#   - tuple: (fila, col) del movimiento o None si es inválido
#
# Ejemplo de uso:
#   movimiento = validar_movimiento(2, movimientos_validos)
# =============================================================================
def validar_movimiento(opcion: int, movimientos_validos: list):
    """Valida si un movimiento es válido."""
    for mov in movimientos_validos:
        if mov[2] == opcion:
            return (mov[0], mov[1])
    return None


# =============================================================================
# VERIFICAR_VICTORIA
# =============================================================================
# Descripción: Verifica si el jugador llegó al objetivo
# 
# Uso en Pygame: Se usa para detectar condición de victoria
#
# Parámetros:
#   - pos_actual (tuple): Posición actual del jugador
#   - tamano (int): Tamaño de la matriz
#
# Retorna:
#   - bool: True si llegó al objetivo
#
# Ejemplo de uso:
#   if verificar_victoria((4, 4), 5):
#       # ¡Victoria!
# =============================================================================
def verificar_victoria(pos_actual: tuple, tamano: int) -> bool:
    """Verifica si el jugador llegó al objetivo."""
    objetivo = (tamano - 1, tamano - 1)
    return pos_actual == objetivo


# =============================================================================
# INICIALIZAR_ESTADO_MINIJUEGO
# =============================================================================
# Descripción: Inicializa el estado del minijuego
# 
# Uso en Pygame: Se usa al comenzar una partida del minijuego
#
# Parámetros:
#   - tamano (int): Tamaño de la matriz (default: constante)
#
# Retorna:
#   - dict: Estado inicial del minijuego
#
# Ejemplo de uso:
#   estado = inicializar_estado_minijuego()
# =============================================================================
def inicializar_estado_minijuego(tamano: int = None) -> dict:
    """Inicializa el estado del minijuego."""
    if tamano is None:
        tamano = TAMAÑO_MATRIZ_MINIJUEGO
    
    matriz = generar_matriz_resoluble(tamano)
    
    estado = {
        "matriz": matriz,
        "jugador_pos": (0, 0),
        "objetivo": (tamano - 1, tamano - 1),
        "camino_recorrido": set(),
        "valor_actual": matriz[0][0],
        "tamano": tamano,
        "terminado": False,
        "victoria": False
    }
    
    return estado


# =============================================================================
# PROCESAR_MOVIMIENTO_MINIJUEGO
# =============================================================================
# Descripción: Procesa un movimiento en el minijuego
# 
# Uso en Pygame: Se usa cuando el jugador hace un movimiento
#
# Parámetros:
#   - estado (dict): Estado actual del minijuego
#   - nueva_pos (tuple): Nueva posición (fila, col)
#
# Retorna:
#   - dict: Estado actualizado
#
# Ejemplo de uso:
#   estado = procesar_movimiento_minijuego(estado, (1, 0))
# =============================================================================
def procesar_movimiento_minijuego(estado: dict, nueva_pos: tuple) -> dict:
    """Procesa un movimiento en el minijuego."""
    # Agregar posición actual al camino recorrido
    estado["camino_recorrido"].add(estado["jugador_pos"])
    
    # Actualizar posición y valor
    estado["jugador_pos"] = nueva_pos
    nuevo_valor = estado["matriz"][nueva_pos[0]][nueva_pos[1]]
    estado["valor_actual"] = nuevo_valor
    
    # Verificar victoria
    if verificar_victoria(nueva_pos, estado["tamano"]):
        estado["terminado"] = True
        estado["victoria"] = True
        estado["camino_recorrido"].add(nueva_pos)
    
    return estado
