# Pygame UI - Trivia Mitológica

## Descripción
Interfaz gráfica completa para el juego de trivia mitológica implementada con Pygame.

## Requisitos
- Python 3.x
- Pygame 2.x

## Instalación

```bash
pip install pygame
```

## Ejecución

Desde el directorio raíz del proyecto:

```bash
cd ui/Pygame
python3 main.py
```

O desde el directorio raíz:

```bash
python3 -m ui.Pygame.main
```

## Estructura de Estados

El juego utiliza un sistema de estados con las siguientes pantallas:

1. **Splash** - Pantalla de inicio con fade-in (3 segundos)
2. **Menu** - Menú principal con opciones:
   - Jugar
   - Historia
   - Salir
3. **Gameplay** - Juego principal de trivia con:
   - Visualización de preguntas por categoría
   - 4 opciones de respuesta
   - Sistema de puntos y rachas
   - Indicador de errores
   - Navegación con mouse y teclado (1-4)
4. **Game Over** - Pantalla de resultados con:
   - Estadísticas finales
   - Opción de reintentar
   - Volver al menú
5. **Historia** - Información sobre el juego
6. **Minijuego** - "Guardianes de Piedra" (navegación por matriz)

## Controles

### Menú Principal
- **Mouse**: Click en los botones
- **ESC**: Salir del juego

### Gameplay
- **Mouse**: Click en las opciones de respuesta
- **1-4**: Seleccionar opción directamente
- **ESPACIO/ENTER**: Continuar después de responder
- **ESC**: Volver al menú (termina partida)

### Historia
- **Mouse**: Click en "Volver"
- **ENTER/ESC**: Volver al menú

### Minijuego
- **Mouse**: Click en las celdas disponibles
- **1-9**: Seleccionar movimiento por número
- **ESC**: Volver al menú

## Características

### Integración con Core
- Usa `core/logica_juego.py` para la lógica del juego
- Usa `core/logica_preguntas.py` para evaluar respuestas
- Usa `core/logica_minijuego.py` para el minijuego
- Carga preguntas desde `assets/preguntas.csv`

### Efectos Visuales
- Degradados de color en fondos
- Sombras en texto
- Fade-in en splash screen
- Colores distintos para respuestas correctas/incorrectas

### Modularidad
- Separación clara entre UI y lógica
- Sistema de estados reutilizable
- Módulo de recursos para fuentes e imágenes
- Módulo de efectos visuales

## Archivos Principales

- `main.py` - Punto de entrada del juego
- `Juego.py` - Motor de estados
- `Estados/base.py` - Clase base para estados
- `Estados/Menu.py` - Menú principal
- `Estados/Gameplay.py` - Juego de trivia
- `Estados/Game_Over.py` - Pantalla de fin de juego
- `Estados/Historia.py` - Pantalla de historia
- `Estados/Splash.py` - Pantalla inicial
- `Estados/Minijuego.py` - Minijuego
- `Botones.py` - Clase de botones
- `recursos.py` - Carga de recursos
- `efectos.py` - Efectos visuales

## Notas

- El juego requiere que exista el archivo `assets/preguntas.csv`
- Las fuentes e imágenes son opcionales (usa recursos por defecto si no existen)
- El juego termina después de 2 errores
- Se pueden ganar buffs con rachas de respuestas correctas
