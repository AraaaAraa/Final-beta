# =============================================================================
# ALGORITMOS MANUALES
# =============================================================================
# Implementaciones manuales de algoritmos comunes
# (sin usar funciones built-in como sum, max, min, etc.)
# =============================================================================

# =============================================================================
# MI_SUM
# =============================================================================
# Descripción: Suma todos los elementos de una lista (implementación manual)
# 
# Uso en Pygame: Se usa igual para cálculos de estadísticas
#
# Parámetros:
#   - lista (list): Lista de números a sumar
#
# Retorna:
#   - int/float: Suma de todos los elementos
#
# Ejemplo de uso:
#   total = mi_sum([1, 2, 3, 4, 5])  # retorna 15
# =============================================================================
def mi_sum(lista) -> int:
    """Suma todos los elementos de una lista."""
    total = 0
    for valor in lista:
        total = total + valor
    return total


# =============================================================================
# MI_MIN
# =============================================================================
# Descripción: Encuentra el valor mínimo en una lista (implementación manual)
# 
# Uso en Pygame: Se usa igual para encontrar mejores tiempos
#
# Parámetros:
#   - lista (list): Lista de números
#
# Retorna:
#   - int/float: Valor mínimo o 0 si la lista está vacía
#
# Ejemplo de uso:
#   minimo = mi_min([5, 2, 8, 1])  # retorna 1
# =============================================================================
def mi_min(lista) -> int:
    """Encuentra el valor mínimo en una lista."""
    if not lista:
        return 0
    minimo = lista[0]
    i = 1
    while i < len(lista):
        if lista[i] < minimo:
            minimo = lista[i]
        i = i + 1
    return minimo


# =============================================================================
# MI_MAX
# =============================================================================
# Descripción: Encuentra el valor máximo en una lista (implementación manual)
# 
# Uso en Pygame: Se usa igual para encontrar mejores puntajes
#
# Parámetros:
#   - lista (list): Lista de números
#
# Retorna:
#   - int/float: Valor máximo o 0 si la lista está vacía
#
# Ejemplo de uso:
#   maximo = mi_max([5, 2, 8, 1])  # retorna 8
# =============================================================================
def mi_max(lista) -> int:
    """Encuentra el valor máximo en una lista."""
    if not lista:
        return 0
    maximo = lista[0]
    i = 1
    while i < len(lista):
        if lista[i] > maximo:
            maximo = lista[i]
        i = i + 1
    return maximo


# =============================================================================
# MI_ENUMERATE
# =============================================================================
# Descripción: Implementación manual de enumerate
# 
# Uso en Pygame: Se usa para iterar con índices
#
# Parámetros:
#   - lista (list): Lista a enumerar
#   - inicio (int): Índice inicial (default: 0)
#
# Retorna:
#   - list: Lista de tuplas (índice, elemento)
#
# Ejemplo de uso:
#   for i, val in mi_enumerate(["a", "b", "c"]):
#       print(i, val)
# =============================================================================
def mi_enumerate(lista, inicio=0) -> list:
    """Implementación manual de enumerate."""
    res = []
    for j in range(len(lista)):
        res.append((inicio + j, lista[j]))
    return res


# =============================================================================
# ENCONTRAR_INDICE
# =============================================================================
# Descripción: Encuentra el índice de un elemento en una lista
# 
# Uso en Pygame: Se usa para búsquedas en listas
#
# Parámetros:
#   - elemento: Elemento a buscar
#   - lista (list): Lista donde buscar
#
# Retorna:
#   - int: Índice del elemento o -1 si no se encuentra
#
# Ejemplo de uso:
#   indice = encontrar_indice("b", ["a", "b", "c"])  # retorna 1
# =============================================================================
def encontrar_indice(elemento, lista) -> int:
    """Encuentra el índice de un elemento en una lista."""
    i = 0
    while i < len(lista):
        if elemento == lista[i]:
            return i
        i = i + 1
    return -1


# =============================================================================
# CALCULAR_ESTADISTICAS_LISTA
# =============================================================================
# Descripción: Calcula estadísticas de una lista de números
# 
# Uso en Pygame: Se usa para mostrar estadísticas de jugadores
#
# Parámetros:
#   - lista (list): Lista de números
#
# Retorna:
#   - dict: Diccionario con promedio, mejor, peor y total
#
# Ejemplo de uso:
#   stats = calcular_estadisticas_lista([10, 20, 30])
#   # retorna {"promedio": 20, "mejor": 30, "peor": 10, "total": 60}
# =============================================================================
def calcular_estadisticas_lista(lista) -> dict:
    """Calcula estadísticas de una lista de números."""
    if not lista:
        return {
            "promedio": 0,
            "mejor": 0,
            "peor": 0,
            "total": 0
        }
    total = mi_sum(lista)
    promedio = total / len(lista)
    mejor = mi_max(lista)
    peor = mi_min(lista)
    return {
        "promedio": promedio,
        "mejor": mejor,
        "peor": peor,
        "total": total
    }
