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
│   └── consola/                  # Implementación consola
│       ├── __init__.py
│       ├── menu_consola.py       # Menú principal consola
│       ├── juego_consola.py      # Flujo de juego consola
│       └── minijuego_consola.py  # Minijuego consola
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
