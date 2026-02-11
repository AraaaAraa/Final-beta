# Arquitectura del Proyecto - Juego de Mitología

## 📋 Tabla de Contenidos
- [Visión General](#visión-general)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Principios de Diseño](#principios-de-diseño)
- [Módulos Principales](#módulos-principales)
- [Migración a Pygame](#migración-a-pygame)
- [Flujo de Ejecución](#flujo-de-ejecución)

## Visión General

Este proyecto implementa un juego de preguntas de mitología con sistema de buffeos, objetos especiales y minijuegos. La arquitectura está diseñada para **separar completamente la lógica de negocio de la interfaz de usuario**, facilitando la migración de consola a Pygame sin modificar la lógica del juego.

## Estructura del Proyecto

```
SegundoParcial/
├── core/                          # 🎯 Lógica de negocio (sin UI)
│   ├── __init__.py
│   ├── logica_juego.py           # Orquestación del flujo del juego
│   ├── logica_buffeos.py         # Sistema de buffeos y objetos especiales
│   ├── logica_preguntas.py       # Evaluación y manejo de preguntas
│   ├── logica_puntaje.py         # Cálculo de puntajes
│   └── logica_minijuego.py       # Lógica del minijuego "Guardianes de Piedra"
│
├── models/                        # 📦 Modelos de datos
│   ├── __init__.py
│   ├── pregunta.py               # Estructura de preguntas
│   ├── usuario.py                # Estructura de usuarios
│   ├── partida.py                # Estado de partidas
│   └── objeto_buff.py            # Objetos especiales/buffs
│
├── data/                          # 💾 Capa de persistencia
│   ├── __init__.py
│   ├── archivos_json.py          # Operaciones JSON genéricas
│   ├── repositorio_usuarios.py   # CRUD de usuarios
│   └── repositorio_preguntas.py  # Carga y filtrado de preguntas
│
├── ui/                            # 🖥️ Capa de presentación
│   ├── __init__.py
│   ├── interfaces.py             # Interfaces abstractas para UI
│   ├── consola/                  # Implementación consola
│   │   ├── __init__.py
│   │   ├── menu_consola.py       # Menú principal consola
│   │   ├── juego_consola.py      # Flujo de juego consola
│   │   └── minijuego_consola.py  # Minijuego consola
│   └── Pygame/                   # ⭐ Implementación Pygame
│       ├── __init__.py
│       ├── main.py               # Punto de entrada Pygame
│       ├── Juego.py              # Máquina de estados
│       ├── Botones.py            # Clase Boton original
│       ├── recursos.py           # Carga de fuentes e imágenes
│       ├── efectos.py            # Efectos visuales
│       ├── componentes/          # ⭐ Componentes reutilizables
│       │   ├── __init__.py
│       │   └── boton.py          # Botón reutilizable con hover
│       ├── utils/                # ⭐ Utilidades Pygame
│       │   ├── __init__.py
│       │   ├── renderizado.py    # Utilidades de renderizado
│       │   └── eventos.py        # Utilidades de eventos
│       └── Estados/              # Estados de la máquina
│           ├── __init__.py
│           ├── base.py           # Clase BaseEstado
│           ├── Menu.py           # Estado de menú
│           ├── Historia.py       # Estado de historia
│           ├── Rankings.py       # Estado de rankings
│           ├── Game_Over.py      # Estado de game over
│           ├── Minijuego.py      # Estado de minijuego
│           ├── SeleccionObjeto.py # Estado de selección
│           └── Gameplay/         # ⭐ Gameplay modularizado
│               ├── __init__.py
│               ├── gameplay.py   # Orquestador principal
│               ├── gestor_preguntas.py  # ⭐ Gestión de preguntas
│               ├── gestor_respuestas.py # ⭐ Gestión de respuestas
│               └── gestor_hud.py        # ⭐ Gestión de HUD
│
├── utils/                         # 🛠️ Utilidades generales
│   ├── __init__.py
│   ├── validaciones.py           # Validaciones reutilizables
│   ├── algoritmos.py             # Algoritmos manuales (sum, min, max, etc.)
│   └── formateadores.py          # Formateo y conversión de texto
│
├── config/                        # ⚙️ Configuraciones
│   ├── __init__.py
│   ├── constantes.py             # Constantes del juego
│   └── mensajes.py               # Mensajes y textos
│
├── assets/                        # 📁 Archivos de datos
│   ├── preguntas.csv             # Base de datos de preguntas
│   ├── Usuarios.json             # Datos de usuarios
│   └── EstadoBuff.json           # Estado de objetos especiales
│
├── Main.py                        # 🚀 Punto de entrada
├── ARQUITECTURA.md                # 📘 Este archivo
└── README.md                      # 📖 Documentación general
```

## Principios de Diseño

### 1. Separación de Responsabilidades

Cada módulo tiene una responsabilidad clara y única:

- **core/**: Contiene SOLO lógica de negocio, sin prints ni inputs
- **ui/**: Contiene SOLO código de interfaz de usuario
- **data/**: Contiene SOLO operaciones de persistencia
- **models/**: Define SOLO estructuras de datos
- **utils/**: Provee SOLO funciones auxiliares reutilizables
- **config/**: Centraliza SOLO configuraciones y constantes

### 2. Independencia de UI

**Regla de Oro**: La lógica de negocio NUNCA debe hacer `print()` ni `input()`.

Las funciones de `core/` retornan datos, y la UI decide cómo mostrarlos:

```python
# ✅ CORRECTO - core/logica_buffeos.py
def calcular_puntos_buffeo(racha: int, objeto: str) -> dict:
    """Calcula puntos sin mostrar nada."""
    puntos = calcular_puntos_por_racha(racha)
    return {
        "puntos": puntos,
        "por_racha": puntos,
        "objeto": objeto
    }

# ✅ CORRECTO - ui/consola/juego_consola.py
def mostrar_buffeo(buffeo_data: dict):
    """Muestra el buffeo en consola."""
    print(f"🔥 ¡BUFFEO! +{buffeo_data['puntos']} puntos")
```

### 3. Configuración Centralizada

Todas las constantes están en `config/constantes.py`:
- Rutas de archivos
- Configuración de niveles
- Puntos por dificultad
- Objetos especiales
- Etc.

Esto facilita ajustar parámetros sin tocar la lógica.

### 4. Algoritmos Manuales

El proyecto implementa manualmente algoritmos comunes (sin usar built-ins):
- `mi_sum()` en lugar de `sum()`
- `mi_max()` en lugar de `max()`
- `mi_min()` en lugar de `min()`
- Ordenamiento manual
- Búsqueda manual

Esto cumple con los requisitos académicos del proyecto.

## Módulos Principales

### core/logica_juego.py

**Responsabilidad**: Orquestar el flujo completo del juego

**Funciones clave**:
- `procesar_pregunta_completa()`: Procesa una pregunta con intentos
- `obtener_pregunta_para_nivel()`: Obtiene pregunta disponible
- `construir_estadisticas_partida()`: Construye stats finales
- `verificar_condicion_fin_partida()`: Verifica game over

**No hace**: Prints, inputs, o manejo de UI

### core/logica_buffeos.py

**Responsabilidad**: Sistema de buffeos y objetos especiales

**Funciones clave**:
- `calcular_puntos_buffeo()`: Calcula puntos extra
- `puede_usar_reintento()`: Verifica disponibilidad de reintento
- `usar_armadura()`, `usar_raciones()`, `usar_bolsa_monedas()`: Activan objetos
- `verificar_merecimiento_objeto()`: Determina si merece objeto

**No hace**: Mostrar mensajes de buffeo (eso es responsabilidad de la UI)

### core/logica_preguntas.py

**Responsabilidad**: Evaluación y manejo de preguntas

**Funciones clave**:
- `evaluar_respuesta()`: Evalúa respuesta del usuario
- `construir_mensaje_resultado()`: Prepara mensaje para UI
- `calcular_racha_actual()`: Calcula racha de aciertos
- `contar_errores_totales()`: Cuenta errores acumulados

**No hace**: Mostrar preguntas ni resultados

### data/repositorio_usuarios.py

**Responsabilidad**: Persistencia de datos de usuarios

**Funciones clave**:
- `obtener_usuario()`: Carga datos de usuario
- `guardar_estadisticas_usuario()`: Guarda stats de partida
- `obtener_ranking()`: Obtiene ranking ordenado

### ui/consola/juego_consola.py

**Responsabilidad**: Implementación de la UI del juego en consola

**Funciones clave**:
- `mostrar_pregunta_consola()`: Muestra pregunta y obtiene respuesta
- `mostrar_resultado_consola()`: Muestra resultado
- `procesar_pregunta_con_ui()`: Combina lógica + UI para una pregunta
- `jugar_partida_completa_consola()`: Flujo completo del juego

**Características**:
- Usa funciones de `core/` para la lógica
- Solo se encarga de prints e inputs
- Fácilmente reemplazable por versión Pygame

## Migración a Pygame

### Arquitectura Preparada

La arquitectura actual está **lista para Pygame**. Los pasos serían:

1. **Mantener sin cambios**:
   - `core/` - Lógica de negocio
   - `models/` - Estructuras de datos
   - `data/` - Persistencia
   - `utils/` - Utilidades
   - `config/` - Configuraciones

2. **Crear nueva UI**:
   ```
   ui/pygame_ui/
   ├── __init__.py
   ├── menu_pygame.py          # Menú con botones gráficos
   ├── juego_pygame.py         # Interfaz de juego gráfica
   ├── minijuego_pygame.py     # Minijuego con cuadrícula gráfica
   └── componentes/            # Widgets reutilizables
       ├── boton.py
       ├── panel_pregunta.py
       └── indicador_racha.py
   ```

3. **Actualizar Main.py**:
   ```python
   from ui.pygame_ui.menu_pygame import ejecutar_menu_pygame
   
   def main():
       ejecutar_menu_pygame()
   ```

### Ejemplo de Migración

**Versión Consola**:
```python
# ui/consola/juego_consola.py
def mostrar_pregunta_consola(pregunta: dict) -> str:
    print(f"📝 {pregunta['descripcion']}")
    for i, opcion in enumerate(pregunta['opciones']):
        print(f"{i+1}. {opcion}")
    return input("Tu respuesta: ")
```

**Versión Pygame** (futura):
```python
# ui/pygame_ui/juego_pygame.py
def mostrar_pregunta_pygame(pregunta: dict) -> str:
    panel = PanelPregunta(pregunta)
    panel.draw(screen)
    
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                respuesta = panel.get_clicked_option(event.pos)
                if respuesta:
                    return respuesta
```

**La lógica es la misma**:
```python
# core/logica_preguntas.py (sin cambios)
def evaluar_respuesta(respuesta: str, opciones: list, correcta: str, usuario: str) -> dict:
    # Esta función se usa igual en consola y pygame
    indice = obtener_indice_letra(respuesta)
    es_valido = validar_indice_opcion(indice, opciones)
    # ... resto de la lógica
```

## Arquitectura Pygame Implementada

### 🎮 Estructura Pygame

La implementación de Pygame sigue el **patrón State Machine** (Máquina de Estados) con componentes reutilizables:

```
ui/Pygame/
├── main.py                   # Punto de entrada, game loop
├── Juego.py                  # Máquina de estados
├── componentes/              # ⭐ Componentes reutilizables
│   ├── boton.py             # Botón con hover y detección de clicks
│   └── __init__.py
├── utils/                    # ⭐ Utilidades de Pygame
│   ├── renderizado.py       # Funciones de renderizado (texto, rectángulos)
│   ├── eventos.py           # Funciones de manejo de eventos
│   └── __init__.py
└── Estados/                  # Estados del juego
    ├── base.py              # BaseEstado (interfaz común)
    ├── Menu.py              # Menú principal
    ├── Historia.py          # Introducción narrativa
    ├── Rankings.py          # Tabla de clasificación
    ├── Game_Over.py         # Pantalla final
    ├── Minijuego.py         # Minijuego de matriz
    ├── SeleccionObjeto.py   # Selección de objeto especial
    └── Gameplay/            # ⭐ Gameplay modularizado
        ├── gameplay.py      # Orquestador principal
        ├── gestor_preguntas.py   # Gestión de preguntas
        ├── gestor_respuestas.py  # Gestión de respuestas
        └── gestor_hud.py         # Gestión de HUD (puntos, racha)
```

### 🔄 Patrón State Machine

**Concepto**: El juego está en uno de varios estados a la vez, cada uno con su propia lógica y renderizado.

**Estados disponibles**:
- `Menu`: Menú principal con opciones
- `Historia`: Introducción narrativa del juego
- `Gameplay`: Pantalla principal de juego (preguntas y respuestas)
- `Minijuego`: Minijuego "Guardianes de Piedra"
- `SeleccionObjeto`: Selección de objeto especial
- `Rankings`: Tabla de puntajes
- `Gameover`: Pantalla de fin de juego

**Flujo de estados**:
```
Menu → Historia → Gameplay → [SeleccionObjeto | Gameover]
  ↓                   ↓
Rankings         Minijuego
```

### 🎯 Game Loop

**Archivo**: `ui/Pygame/main.py`

El game loop se ejecuta a 60 FPS y sigue el patrón clásico de juegos:

```python
while juego.corriendo:
    # 1. PROCESAR EVENTOS (clicks, teclado, cerrar ventana)
    for evento in pygame.event.get():
        estado_actual.get_event(evento)
    
    # 2. ACTUALIZAR LÓGICA (mover objetos, calcular estado)
    dt = reloj.tick(FPS)  # Delta time
    estado_actual.update(dt)
    
    # 3. RENDERIZAR (dibujar todo en pantalla)
    estado_actual.draw(pantalla)
    pygame.display.flip()
    
    # 4. CAMBIAR ESTADO (si el actual terminó)
    if estado_actual.done:
        estado_actual = estados[estado_actual.sig_estado]
```

### 🧩 Componentes Reutilizables

#### Boton (`ui/Pygame/componentes/boton.py`)

**Propósito**: Componente reutilizable de botón con hover y detección de clicks.

**Características**:
- Imágenes de estado (normal/hover)
- Detección automática de hover
- Método `fue_clickeado()` para detección de clicks
- Método `renderizar()` para dibujado

**Uso**:
```python
from ui.Pygame.componentes import Boton

boton = Boton(x=300, y=200, ancho=200, alto=60, 
              texto="JUGAR", fuente=mi_fuente)

# En game loop:
boton.actualizar(pygame.mouse.get_pos())  # Actualizar hover
boton.renderizar(pantalla)                # Dibujar

# En eventos:
if evento.type == pygame.MOUSEBUTTONDOWN:
    if boton.fue_clickeado(evento.pos):
        # Botón clickeado!
```

**Beneficio**: Evita duplicar código de botones en cada estado.

#### Utilidades de Renderizado (`ui/Pygame/utils/renderizado.py`)

Funciones reutilizables:
- `renderizar_texto()`: Renderiza texto centrado en una posición
- `renderizar_rectangulo_con_borde()`: Dibuja rectángulo con borde
- `limpiar_pantalla()`: Limpia pantalla con color sólido

**Beneficio**: Centraliza lógica de renderizado, evita repetición.

#### Utilidades de Eventos (`ui/Pygame/utils/eventos.py`)

Funciones reutilizables:
- `detectar_click_en_botones()`: Detecta qué botón fue clickeado
- `obtener_posicion_mouse()`: Wrapper de pygame.mouse.get_pos()

**Beneficio**: Simplifica manejo de eventos.

### 🎮 Gameplay Modularizado

**Problema anterior**: `Gameplay.py` tenía ~612 líneas manejando todo.

**Solución**: Separar responsabilidades en gestores especializados:

#### GestorPreguntas (`gestor_preguntas.py`)

**Responsabilidad**: Cargar, seleccionar y renderizar preguntas.

**Funciones**:
- `cargar_preguntas()`: Carga preguntas desde CSV
- `siguiente_pregunta()`: Selecciona siguiente pregunta del nivel
- `obtener_opciones()`: Devuelve opciones de la pregunta actual
- `renderizar()`: Dibuja pregunta en pantalla

**Delega a**: `core/logica_juego.py`, `data/repositorio_preguntas.py`

#### GestorRespuestas (`gestor_respuestas.py`)

**Responsabilidad**: Mostrar opciones, detectar clicks/teclado, procesar respuestas.

**Funciones**:
- `crear_botones_opciones()`: Crea botones para A, B, C, D
- `actualizar_hover()`: Actualiza estado hover de botones
- `detectar_click()`: Detecta qué opción fue clickeada
- `procesar_respuesta()`: **Delega a core/** para calcular resultado
- `renderizar()`: Dibuja botones en pantalla

**Delega a**: `core/logica_juego.procesar_pregunta_completa()`

#### GestorHUD (`gestor_hud.py`)

**Responsabilidad**: Mostrar puntos, nivel, racha, errores, objetos equipados.

**Funciones**:
- `inicializar()`: Resetea estadísticas para nueva partida
- `actualizar_puntos()`: Actualiza puntos totales
- `actualizar_racha()`: Actualiza racha de aciertos
- `incrementar_errores()`: Incrementa contador de errores
- `renderizar()`: Dibuja HUD en pantalla

**NO delega**: Solo renderiza, no calcula lógica.

### 🔀 Separación UI/Lógica en Pygame

**Regla de Oro**: Pygame SOLO muestra y detecta eventos. Core SOLO procesa lógica.

**Ejemplo en Gameplay**:

```python
# ❌ MAL: Pygame calcula puntos
puntos = pregunta.dificultad * 2 + racha

# ✅ BIEN: Pygame delega a core
resultado = procesar_pregunta_completa(
    pregunta,
    nombre_usuario,
    racha_actual,
    letra_respuesta,
    intento_actual,
    intentos_maximos
)
puntos = resultado.get("puntos", 0)
racha_nueva = racha_actual + 1 if resultado["es_correcta"] else 0
```

**Beneficios**:
1. **Testabilidad**: Core se puede probar sin Pygame
2. **Reutilización**: Misma lógica para consola y Pygame
3. **Mantenibilidad**: Cambiar cálculos sin tocar UI
4. **Portabilidad**: Fácil migrar a otra librería gráfica

### 📚 Guías de Defensa Creadas

Para facilitar el estudio y defensa del código Pygame, se crearon 3 guías completas:

1. **GUIA_DEFENSA_PYGAME.md** (~13KB)
   - Conceptos fundamentales (máquina de estados, game loop)
   - Patrones de diseño aplicados
   - 10 preguntas frecuentes con respuestas preparadas
   - Frases clave para impresionar
   - Checklist de defensa

2. **MAPA_DEPENDENCIAS_PYGAME.md** (~13KB)
   - Flujo de ejecución completo
   - Dependencias por capa
   - Importaciones detalladas de cada archivo
   - Diagrama visual de dependencias
   - Análisis de dependencias circulares

3. **ESTUDIO_RAPIDO_PYGAME.md** (~14KB)
   - Cronograma de estudio de 1 hora
   - Top 5 archivos críticos a conocer
   - 10 frases clave memorizables
   - Estrategia de defensa
   - Checklist pre-defensa
   - Planes de emergencia (30 min, 15 min)

**Objetivo**: Estudiar y defender Pygame en 1 hora.

## Flujo de Ejecución

### 1. Inicio del Programa

```
Main.py
  ↓
ui/consola/menu_consola.py::ejecutar_menu_consola()
  ↓
Pide nombre de usuario
  ↓
Muestra menú principal
```

### 2. Inicio de Partida

```
Usuario selecciona "Juego principal"
  ↓
ui/consola/juego_consola.py::jugar_partida_completa_consola()
  ↓
data/repositorio_preguntas.py::cargar_preguntas_desde_csv()
  ↓
Para cada nivel (1, 2, 3):
  ↓
  ui/consola/juego_consola.py::jugar_nivel_consola()
```

### 3. Procesar Pregunta

```
Para cada pregunta del nivel:
  ↓
core/logica_juego.py::obtener_pregunta_para_nivel()
  ↓
ui/consola/juego_consola.py::mostrar_pregunta_consola() [UI]
  ↓
Usuario ingresa respuesta
  ↓
core/logica_juego.py::procesar_pregunta_completa() [LÓGICA]
  ├─→ core/logica_preguntas.py::evaluar_respuesta()
  ├─→ core/logica_puntaje.py::calcular_puntos_base()
  ├─→ core/logica_buffeos.py::calcular_puntos_buffeo()
  └─→ core/logica_buffeos.py::usar_raciones/bolsa_monedas()
  ↓
ui/consola/juego_consola.py::mostrar_resultado_consola() [UI]
```

### 4. Fin de Partida

```
Todos los niveles completados o 2 errores
  ↓
core/logica_buffeos.py::verificar_merecimiento_objeto()
  ↓
Si merece objeto:
  ui/consola/juego_consola.py::seleccionar_objeto_especial() [UI]
  core/logica_buffeos.py::guardar_objeto_equipado() [LÓGICA]
  ↓
core/logica_juego.py::construir_estadisticas_partida()
  ↓
data/repositorio_usuarios.py::guardar_estadisticas_usuario()
  ↓
ui/consola/juego_consola.py::mostrar_resumen_final() [UI]
```

## Ventajas de esta Arquitectura

✅ **Mantenibilidad**: Cada módulo tiene una responsabilidad clara  
✅ **Testabilidad**: La lógica puede probarse sin UI  
✅ **Escalabilidad**: Fácil agregar nuevas características  
✅ **Portabilidad**: Cambiar de consola a Pygame es trivial  
✅ **Reusabilidad**: Componentes reutilizables entre diferentes UIs  
✅ **Claridad**: Código bien organizado y documentado  

## Convenciones de Código

1. **Nombres de archivos**: snake_case (ej: `logica_buffeos.py`)
2. **Nombres de funciones**: snake_case (ej: `calcular_puntos()`)
3. **Nombres de clases**: PascalCase (ej: `InterfazJuego`)
4. **Constantes**: UPPER_SNAKE_CASE (ej: `RUTA_USUARIOS`)
5. **Comentarios**: Cada función tiene bloque de comentarios descriptivo
6. **Type hints**: Se usan cuando es posible para claridad
7. **Retornos**: Una sola sentencia `return` por función

## Documentación de Funciones

Cada función sigue este formato:

```python
# =============================================================================
# NOMBRE_FUNCION
# =============================================================================
# Descripción: Qué hace esta función en el contexto del juego
# 
# Uso en Pygame: Cómo se adaptaría esta función para pygame (si aplica)
#
# Parámetros:
#   - param1 (tipo): descripción
#   - param2 (tipo): descripción
#
# Retorna:
#   - tipo: descripción de qué retorna
#
# Ejemplo de uso:
#   resultado = nombre_funcion(param1, param2)
# =============================================================================
def nombre_funcion(param1: tipo, param2: tipo) -> tipo_retorno:
    """Docstring breve."""
    # Implementación...
    return resultado
```

## Conclusión

Esta arquitectura facilita:
- Desarrollo colaborativo
- Migración a Pygame
- Mantenimiento a largo plazo
- Extensión de funcionalidades
- Testing y debugging

El proyecto está **listo para migrar a Pygame** simplemente creando `ui/pygame_ui/` y reutilizando toda la lógica existente.
