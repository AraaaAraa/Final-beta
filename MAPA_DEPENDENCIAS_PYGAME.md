# 🗺️ Mapa de Dependencias: Pygame

## 📋 Índice
1. [Flujo de Ejecución General](#flujo-de-ejecución-general)
2. [Dependencias por Capa](#dependencias-por-capa)
3. [Importaciones Detalladas](#importaciones-detalladas)
4. [Diagrama Visual](#diagrama-visual)

---

## 🔄 Flujo de Ejecución General

```
Main.py
  ↓ pygame.init()
  ↓ crear pantalla
  ↓
Juego.py (máquina de estados)
  ↓ crear todos los estados
  ↓ estado_actual = "Menu"
  ↓
GAME LOOP:
  ↓
Estado actual (ej: Gameplay)
  ↓ get_event() → detecta click
  ↓ update() → actualiza lógica
  ↓
DELEGA A CORE:
  ↓ procesar_pregunta_completa()
  ↓ calcular_datos_buffeo_para_ui()
  ↓ obtener_pregunta_para_nivel()
  ↓
CORE devuelve resultado
  ↓
Estado actualiza UI
  ↓ draw() → renderiza
  ↓
pygame.display.flip()
```

---

## 📦 Dependencias por Capa

### Capa 1: Core (Lógica Pura)

**NO depende de Pygame**, solo de:
- `config/constantes.py`
- `data/` (para acceso a archivos)
- `models/` (estructuras de datos)
- `utils/` (validaciones, algoritmos)

**Archivos**:
- `core/logica_juego.py`
- `core/logica_preguntas.py`
- `core/logica_puntaje.py`
- `core/logica_buffeos.py`
- `core/logica_minijuego.py`

### Capa 2: Data (Persistencia)

**Depende de**:
- `config/constantes.py` (rutas de archivos)
- `models/` (Usuario, Pregunta, etc.)
- `utils/` (validaciones)

**NO depende de**: Pygame, core

**Archivos**:
- `data/repositorio_usuarios.py`
- `data/repositorio_preguntas.py`
- `data/archivos_json.py`

### Capa 3: UI Pygame (Interfaz)

**Depende de**:
- Pygame
- `core/` (llama a funciones de lógica)
- `data/` (a veces directamente)
- `config/constantes.py`

**Archivos**:
- `ui/Pygame/main.py`
- `ui/Pygame/Juego.py`
- `ui/Pygame/Estados/*.py`
- `ui/Pygame/componentes/*.py`
- `ui/Pygame/utils/*.py`

---

## 📝 Importaciones Detalladas

### ui/Pygame/main.py

**Importa**:
```python
import pygame
from ui.Pygame.Juego import Juego
from config.constantes import ANCHO, ALTO, FPS
```

**Propósito**: 
- Punto de entrada de Pygame
- Inicializa pygame
- Crea ventana y reloj
- Ejecuta máquina de estados

**Depende de**: Pygame, Juego.py, constantes.py

---

### ui/Pygame/Juego.py

**Importa**:
```python
import pygame
from ui.Pygame.Estados.Menu import menu
from ui.Pygame.Estados.Gameplay import gameplay
from ui.Pygame.Estados.Rankings import rankings
from ui.Pygame.Estados.Game_Over import gameOver
from ui.Pygame.Estados.Historia import historia
from ui.Pygame.Estados.Minijuego import minijuego
from ui.Pygame.Estados.SeleccionObjeto import seleccionObjeto
from config.constantes import ANCHO, ALTO, FPS
```

**Propósito**:
- Máquina de estados
- Game loop principal
- Gestión de transiciones entre estados

**Depende de**: Pygame, todos los estados, constantes.py

---

### ui/Pygame/Estados/Gameplay/gameplay.py

**Importa**:
```python
import pygame
from .base import BaseEstado
from config.constantes import ALTO, ANCHO, RUTA_PREGUNTAS, PREGUNTAS_POR_NIVEL, MAX_ERRORES_PERMITIDOS
from ..Botones import Boton, BOTON_ALTO_PEQUENO, BOTON_ANCHO_PEQUENO
from ..recursos import cargar_imagen, cargar_fuente_principal
from ..efectos import dibujar_degradado_vertical, dibujar_sombra_texto
from data.repositorio_preguntas import cargar_preguntas_desde_csv
from core.logica_juego import (
    obtener_pregunta_para_nivel,
    preparar_datos_pregunta_para_ui,
    calcular_datos_buffeo_para_ui,
    procesar_pregunta_completa,
    verificar_condicion_fin_partida
)
from core.logica_preguntas import calcular_racha_actual, determinar_intentos_maximos
from core.logica_buffeos import (
    verificar_objeto_equipado, 
    verificar_merecimiento_objeto,
    calcular_errores_permitidos_con_vidas,
    obtener_vidas_extra_usuario,
    consumir_vidas_extra_usuario,
    calcular_vidas_ganadas,
    guardar_vidas_extra_usuario,
    consumir_objeto_equipado
)
```

**Propósito**:
- Estado principal del juego
- Orquesta la pantalla de juego
- Delega lógica a core/

**Depende de**: Pygame, BaseEstado, Botones, recursos, efectos, data/, core/

**Llamado por**: Juego.py (máquina de estados)

---

### ui/Pygame/Estados/Gameplay/gestor_preguntas.py

**Importa**:
```python
import pygame
from data.repositorio_preguntas import cargar_preguntas_desde_csv
from core.logica_juego import obtener_pregunta_para_nivel
from config.constantes import RUTA_PREGUNTAS, PREGUNTAS_POR_NIVEL
from ..efectos import dibujar_sombra_texto
```

**Propósito**:
- Gestionar carga y selección de preguntas
- Renderizar preguntas en pantalla

**Depende de**: Pygame, data/, core/, constantes, efectos

**Usado por**: gameplay.py (futuro)

---

### ui/Pygame/Estados/Gameplay/gestor_respuestas.py

**Importa**:
```python
import pygame
from ..Botones import Boton, BOTON_ANCHO_PEQUENO, BOTON_ALTO_PEQUENO
from core.logica_juego import procesar_pregunta_completa
from core.logica_preguntas import determinar_intentos_maximos
from core.logica_buffeos import verificar_objeto_equipado
```

**Propósito**:
- Gestionar botones de opciones
- Detectar respuestas del usuario
- Procesar respuestas usando core/

**Depende de**: Pygame, Botones, core/

**Usado por**: gameplay.py (futuro)

---

### ui/Pygame/Estados/Gameplay/gestor_hud.py

**Importa**:
```python
import pygame
from core.logica_buffeos import verificar_objeto_equipado
from config.constantes import PREGUNTAS_POR_NIVEL, MAX_ERRORES_PERMITIDOS
```

**Propósito**:
- Mostrar puntos, nivel, racha, errores
- Visualizar objetos equipados
- Renderizar HUD (heads-up display)

**Depende de**: Pygame, core/, constantes

**Usado por**: gameplay.py (futuro)

---

### ui/Pygame/Estados/Menu.py

**Importa**:
```python
import pygame
from .base import BaseEstado
from ..Botones import Boton, crear_botones_centrados
from ..efectos import dibujar_degradado_vertical
from ..recursos import cargar_imagen, cargar_fuente_principal
```

**Propósito**:
- Menú principal
- Botones de navegación

**Depende de**: Pygame, BaseEstado, Botones, efectos, recursos

---

### ui/Pygame/Estados/Rankings.py

**Importa**:
```python
import pygame
from .base import BaseEstado
from ..Botones import Boton, crear_botones_centrados
from ..efectos import dibujar_degradado_vertical
from ..recursos import cargar_imagen, cargar_fuente_principal
from data.repositorio_usuarios import obtener_ranking
from config.constantes import RUTA_USUARIOS
```

**Propósito**:
- Mostrar tabla de clasificación
- Ordenar jugadores por puntaje

**Depende de**: Pygame, BaseEstado, Botones, efectos, recursos, data/

---

### ui/Pygame/componentes/boton.py

**Importa**:
```python
import pygame
from ..recursos import cargar_imagen
```

**Propósito**:
- Componente reutilizable de botón
- Detección de hover y clicks

**Depende de**: Pygame, recursos

**Usado por**: Todos los estados (futuro)

---

### ui/Pygame/utils/renderizado.py

**Importa**:
```python
import pygame
```

**Propósito**:
- Utilidades de renderizado
- Funciones para dibujar texto, rectángulos

**Depende de**: Solo Pygame

**Usado por**: Estados (futuro)

---

### ui/Pygame/utils/eventos.py

**Importa**:
```python
import pygame
```

**Propósito**:
- Utilidades de manejo de eventos
- Detección de clicks en botones

**Depende de**: Solo Pygame

**Usado por**: Estados (futuro)

---

### core/logica_juego.py

**Importa**:
```python
from data.repositorio_preguntas import filtrar_preguntas_por_nivel, seleccionar_pregunta_aleatoria
from core.logica_puntaje import calcular_puntos_pregunta
from core.logica_preguntas import determinar_intentos_maximos, calcular_racha_actual
from core.logica_buffeos import (
    calcular_puntos_buffeo,
    aplicar_buffeo_objeto,
    calcular_datos_buffeo_completo,
    verificar_objeto_equipado
)
from config.constantes import PREGUNTAS_POR_NIVEL, MAX_ERRORES_PERMITIDOS, RUTA_PREGUNTAS
```

**Propósito**:
- Orquestador principal de lógica de juego
- Procesa preguntas completas
- Coordina cálculos de puntos, racha, buffeo

**Depende de**: data/, otros módulos core/, constantes

**NO depende de**: Pygame

**Usado por**: ui/Pygame/Estados/Gameplay/gameplay.py

---

### core/logica_buffeos.py

**Importa**:
```python
from config.constantes import (
    RACHA_BUFFEO_MINIMA,
    PUNTOS_BUFFEO_POR_RACHA,
    OBJETOS_ESPECIALES,
    RUTA_ESTADO_BUFF,
    PUNTOS_POR_VIDA_EXTRA,
    MAX_VIDAS_EXTRA
)
from data.archivos_json import leer_json, escribir_json
```

**Propósito**:
- Sistema de buffeos (puntos extra)
- Gestión de objetos especiales
- Sistema de vidas extra

**Depende de**: constantes, data/archivos_json

**NO depende de**: Pygame

**Usado por**: core/logica_juego.py, ui/Pygame/Estados/Gameplay/

---

### data/repositorio_preguntas.py

**Importa**:
```python
import csv
from models.pregunta import Pregunta
from utils.validaciones import validar_dificultad, validar_respuesta
```

**Propósito**:
- Cargar preguntas desde CSV
- Filtrar por nivel
- Seleccionar preguntas aleatoriamente

**Depende de**: models/, utils/

**NO depende de**: Pygame, core

**Usado por**: core/logica_juego.py, ui/Pygame/Estados/Gameplay/

---

### config/constantes.py

**Importa**:
```python
import os
```

**Propósito**:
- Centralizar toda la configuración
- Rutas de archivos
- Parámetros del juego
- Configuración de Pygame (ANCHO, ALTO, FPS)

**NO depende de**: Ningún otro módulo del proyecto

**Usado por**: TODO el proyecto

---

## 📊 Diagrama Visual de Dependencias

```
┌─────────────────────────────────────────────────────────┐
│                     MAIN.PY                             │
│                 (Punto de Entrada)                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                    JUEGO.PY                             │
│              (Máquina de Estados)                       │
└───┬─────────┬─────────┬─────────┬─────────┬────────────┘
    │         │         │         │         │
    ↓         ↓         ↓         ↓         ↓
┌───────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
│ Menu  │ │Gameplay│ │Rankings│ │Gameover│ │ Historia │
└───┬───┘ └───┬────┘ └───┬────┘ └───┬────┘ └────┬─────┘
    │         │          │          │           │
    └─────────┴──────────┴──────────┴───────────┘
                     │
                     ↓
         ┌───────────────────────┐
         │   COMPONENTES PYGAME  │
         │  - Botones.py         │
         │  - recursos.py        │
         │  - efectos.py         │
         │  - componentes/       │
         │  - utils/             │
         └───────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         ↓                       ↓
┌─────────────────┐     ┌─────────────────┐
│   CORE (Lógica) │     │  DATA (Archivos)│
│ - logica_juego  │     │ - repo_preguntas│
│ - logica_buffeos│     │ - repo_usuarios │
│ - logica_puntaje│     │ - archivos_json │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         └───────────┬───────────┘
                     ↓
         ┌───────────────────────┐
         │  FUNDACIÓN            │
         │  - config/constantes  │
         │  - models/            │
         │  - utils/             │
         └───────────────────────┘
```

---

## 🔍 Análisis de Dependencias Circulares

**¿Hay dependencias circulares?** ❌ NO

El proyecto sigue una arquitectura en capas clara:

1. **Capa Base**: config, models, utils
2. **Capa Data**: usa Capa Base
3. **Capa Core**: usa Data y Base
4. **Capa UI**: usa todas las anteriores

**Flujo de dependencias**: UI → Core → Data → Base

✅ Sin ciclos, arquitectura limpia

---

## 🎯 Puntos Clave para la Defensa

1. **Separación Clara**: UI no sabe de lógica, Core no sabe de Pygame
2. **Flujo Unidireccional**: UI llama a Core, Core devuelve datos
3. **Capa Base Independiente**: constantes, models, utils son autocontenidos
4. **Máquina de Estados Centralizada**: Juego.py orquesta todo
5. **Componentes Reutilizables**: Evitan duplicación en UI

---

## 📚 Archivos por Propósito

### Punto de Entrada
- `Main.py` → Inicia todo

### Orquestación
- `Juego.py` → Máquina de estados

### Lógica de Negocio
- `core/logica_juego.py` → Procesamiento principal
- `core/logica_buffeos.py` → Sistema de buffeos
- `core/logica_puntaje.py` → Cálculo de puntos
- `core/logica_preguntas.py` → Gestión de preguntas
- `core/logica_minijuego.py` → Lógica del minijuego

### Persistencia
- `data/repositorio_usuarios.py` → CRUD usuarios
- `data/repositorio_preguntas.py` → Carga de preguntas
- `data/archivos_json.py` → Lectura/escritura JSON

### Interfaz Gráfica
- `ui/Pygame/Estados/*.py` → Estados visuales
- `ui/Pygame/componentes/*.py` → Componentes reutilizables
- `ui/Pygame/utils/*.py` → Utilidades de UI
- `ui/Pygame/Botones.py` → Clase Boton original
- `ui/Pygame/recursos.py` → Carga de assets
- `ui/Pygame/efectos.py` → Efectos visuales

### Configuración
- `config/constantes.py` → Toda la configuración

### Modelos
- `models/usuario.py` → Estructura de Usuario
- `models/pregunta.py` → Estructura de Pregunta
- `models/partida.py` → Estructura de Partida
- `models/objeto_buff.py` → Estructura de ObjetoBuff

### Utilidades
- `utils/validaciones.py` → Validaciones
- `utils/algoritmos.py` → Algoritmos manuales
- `utils/formateadores.py` → Formateo de datos

---

**Total de archivos Python**: ~35
**Líneas de código (estimado)**: ~5000

**Arquitectura**: Limpia, modular, mantenible ✅
