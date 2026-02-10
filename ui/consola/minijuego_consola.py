# =============================================================================
# MINIJUEGO CONSOLA
# =============================================================================
# Implementación del minijuego "Guardianes de Piedra" en consola
# =============================================================================

from core.logica_minijuego import (
    inicializar_estado_minijuego,
    obtener_movimientos_validos,
    validar_movimiento,
    procesar_movimiento_minijuego,
    verificar_victoria
)
from config.mensajes import *

# =============================================================================
# MOSTRAR_MATRIZ_CONSOLA
# =============================================================================
# Descripción: Muestra la matriz del minijuego en consola
# 
# Uso en Pygame: Mostraría una cuadrícula gráfica
#
# Parámetros:
#   - matriz (list): Matriz del juego
#   - jugador_pos (tuple): Posición del jugador
#   - camino_recorrido (set): Posiciones ya recorridas
#
# Retorna:
#   - None
#
# Ejemplo de uso:
#   mostrar_matriz_consola(matriz, (0,0), camino)
# =============================================================================
def mostrar_matriz_consola(matriz: list, jugador_pos: tuple, camino_recorrido: set) -> None:
    """Muestra la matriz del minijuego en consola."""
    i = 0
    while i < len(matriz):
        fila = matriz[i]
        linea = ""
        j = 0
        while j < len(fila):
            valor = fila[j]
            if jugador_pos[0] == i and jugador_pos[1] == j:
                linea = linea + f"[{valor:2}]"
            else:
                esta_en_camino = (i, j) in camino_recorrido
                if esta_en_camino:
                    linea = linea + f" {valor:2}*"
                else:
                    linea = linea + f" {valor:2} "
            linea = linea + " "
            j = j + 1
        print(linea)
        i = i + 1
    print()


# =============================================================================
# MOSTRAR_MOVIMIENTOS_CONSOLA
# =============================================================================
# Descripción: Muestra los movimientos válidos en consola
# 
# Uso en Pygame: Mostraría botones o celdas destacadas
#
# Parámetros:
#   - movimientos (list): Lista de movimientos válidos
#
# Retorna:
#   - None
#
# Ejemplo de uso:
#   mostrar_movimientos_consola(movimientos)
# =============================================================================
def mostrar_movimientos_consola(movimientos: list) -> None:
    """Muestra los movimientos válidos en consola."""
    print("Movimientos válidos:")
    for mov in movimientos:
        fila, col, indice, simbolo = mov
        valor = "desconocido"  # placeholder
        print(f"{indice}. {simbolo} -> ({fila},{col})")


# =============================================================================
# EJECUTAR_MINIJUEGO_CONSOLA
# =============================================================================
# Descripción: Ejecuta el minijuego en modo consola
# 
# Uso en Pygame: Interfaz gráfica con cuadrícula interactiva
#
# Parámetros:
#   Ninguno
#
# Retorna:
#   - bool: True si ganó, False si perdió o salió
#
# Ejemplo de uso:
#   resultado = ejecutar_minijuego_consola()
# =============================================================================
def ejecutar_minijuego_consola() -> bool:
    """Ejecuta el minijuego en modo consola."""
    print(MINIJUEGO_TITULO)
    print(MINIJUEGO_OBJETIVO)
    print(MINIJUEGO_REGLA)
    print(MINIJUEGO_LEYENDA)
    
    # Inicializar estado
    estado = inicializar_estado_minijuego()
    print(MINIJUEGO_MATRIZ_GENERADA)
    
    print("Matriz de guardianes:")
    mostrar_matriz_consola(estado["matriz"], estado["jugador_pos"], estado["camino_recorrido"])
    
    # Bucle principal
    while not estado["terminado"]:
        print(f"\nPosición actual: {estado['jugador_pos']} [valor: {estado['valor_actual']}]")
        print(f"Objetivo: {estado['objetivo']}")
        
        # Obtener movimientos válidos
        movimientos = obtener_movimientos_validos(
            estado["matriz"],
            estado["jugador_pos"],
            estado["valor_actual"]
        )
        
        if not movimientos:
            print(MINIJUEGO_DERROTA)
            return False
        
        # Mostrar movimientos
        for mov in movimientos:
            fila, col, indice, simbolo = mov
            valor_celda = estado["matriz"][fila][col]
            print(f"{indice}. {simbolo} -> ({fila},{col}) [valor: {valor_celda}]")
        
        # Pedir entrada
        print("\n¿Qué movimiento eliges? (número del 1-8, 'r' para reiniciar, 'q' para salir)")
        entrada = input("Tu elección: ").strip().lower()
        
        # Procesar entrada
        if entrada == 'q':
            print(MINIJUEGO_SALIENDO)
            return False
        
        if entrada == 'r':
            print(MINIJUEGO_REINICIANDO)
            return ejecutar_minijuego_consola()
        
        if not entrada.isdigit():
            print("Por favor ingresa un número válido.")
            continue
        
        opcion = int(entrada)
        nueva_pos = validar_movimiento(opcion, movimientos)
        
        if nueva_pos is None:
            print("Opción no válida. Intenta de nuevo.")
            continue
        
        # Procesar movimiento
        estado = procesar_movimiento_minijuego(estado, nueva_pos)
        
        print(f"\nTe mueves a {nueva_pos} con valor {estado['valor_actual']}")
        print("Estado actual:")
        mostrar_matriz_consola(estado["matriz"], estado["jugador_pos"], estado["camino_recorrido"])
    
    # Victoria
    if estado["victoria"]:
        print(MINIJUEGO_VICTORIA)
        print("\nCamino completo recorrido:")
        mostrar_matriz_consola(estado["matriz"], (-1, -1), estado["camino_recorrido"])
        return True
    
    return False
