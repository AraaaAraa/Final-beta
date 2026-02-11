# 🗺️ Mapa de Dependencias del Proyecto

## 📊 Visión General de Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                         UI Layer                         │
│  ┌──────────────┐              ┌──────────────┐         │
│  │   Consola    │              │   Pygame     │         │
│  │  (ui/consola)│              │ (ui/Pygame)  │         │
│  └──────┬───────┘              └──────┬───────┘         │
│         │                             │                  │
└─────────┼─────────────────────────────┼─────────────────┘
          │                             │
          └──────────┬──────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    Core Layer                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │ logica_juego.py (Orchestrator)                   │  │
│  │    ├─► logica_preguntas.py                       │  │
│  │    ├─► logica_buffeos.py                         │  │
│  │    ├─► logica_puntaje.py                         │  │
│  │    └─► logica_minijuego.py                       │  │
│  └──────────────────┬───────────────────────────────┘  │
└─────────────────────┼──────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────┐
│                   Data Layer                            │
│  ┌──────────────┐         ┌─────────────────┐          │
│  │ repositorio_ │         │ repositorio_    │          │
│  │ usuarios.py  │         │ preguntas.py    │          │
│  └──────┬───────┘         └────────┬────────┘          │
│         │                          │                    │
│         └──────────┬───────────────┘                    │
│                    │                                     │
│         ┌──────────▼───────────┐                        │
│         │  archivos_json.py    │                        │
│         └──────────────────────┘                        │
└────────────────────┬───────────────────────────────────┘
                     │
┌────────────────────▼───────────────────────────────────┐
│                 Models Layer                            │
│  usuario.py │ pregunta.py │ partida.py │ objeto_buff.py│
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│      Utils (usado por todas las capas)                  │
│  algoritmos.py │ validaciones.py │ formateadores.py    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│       Config (constantes globales)                      │
│       constantes.py │ mensajes.py                       │
└─────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Ejecución Principal

### Modo Consola
```
Main.py
  └─► ui/consola/menu_consola.py
       ├─► ui/consola/juego_consola.py
       │    └─► core/logica_juego.py
       │         ├─► core/logica_preguntas.py
       │         ├─► core/logica_buffeos.py
       │         ├─► core/logica_puntaje.py
       │         └─► data/repositorio_preguntas.py
       │
       └─► ui/consola/minijuego_consola.py
            └─► core/logica_minijuego.py
```

### Modo Pygame
```
ui/Pygame/main.py
  └─► ui/Pygame/Juego.py
       └─► ui/Pygame/Estados/Menu.py
            ├─► ui/Pygame/Estados/Gameplay.py
            │    └─► core/logica_juego.py (mismo que consola)
            │
            ├─► ui/Pygame/Estados/Minijuego.py
            │    └─► core/logica_minijuego.py (mismo que consola)
            │
            ├─► ui/Pygame/Estados/SeleccionObjeto.py
            │    └─► core/logica_buffeos.py
            │
            ├─► ui/Pygame/Estados/Game_Over.py
            │    └─► data/repositorio_usuarios.py
            │
            └─► ui/Pygame/Estados/Rankings.py
                 └─► data/repositorio_usuarios.py
```

## 📋 Matriz de Importaciones Detallada

### config/constantes.py
**Es importado por:**
- `core/logica_juego.py` (líneas 29-34)
- `core/logica_buffeos.py` (líneas 8-13)
- `core/logica_puntaje.py` (línea 7)
- `core/logica_minijuego.py` (línea 8)
- `data/repositorio_usuarios.py` (línea 10)
- `data/repositorio_preguntas.py` (línea 10)
- `utils/formateadores.py` (línea 7)
- `ui/Pygame/Estados/*.py` (múltiples)

### models/usuario.py
**Importa de:** Ninguno (modelo puro)

**Es importado por:**
- `data/repositorio_usuarios.py` (línea 8)

### models/pregunta.py
**Importa de:** Ninguno (modelo puro)

**Es importado por:**
- `data/repositorio_preguntas.py` (línea 9)

### models/partida.py
**Importa de:**
- `time` (biblioteca estándar)

**Es importado por:**
- `ui/Pygame/Estados/Gameplay.py`
- `ui/consola/juego_consola.py`

### data/archivos_json.py
**Importa de:**
- `os` (biblioteca estándar)
- `json` (biblioteca estándar)

**Es importado por:**
- `data/repositorio_usuarios.py` (línea 7)
- `data/repositorio_preguntas.py` (línea 8)
- `core/logica_buffeos.py` (línea 7)

### data/repositorio_usuarios.py
**Importa de:**
- `data/archivos_json` (línea 7)
- `models/usuario` (línea 8)
- `utils/algoritmos` (línea 9)
- `config/constantes` (línea 10)

**Es importado por:**
- `core/logica_juego.py` (línea 12)
- `ui/consola/menu_consola.py`
- `ui/Pygame/Estados/Game_Over.py`
- `ui/Pygame/Estados/Rankings.py`

### data/repositorio_preguntas.py
**Importa de:**
- `random` (biblioteca estándar)
- `data/archivos_json` (línea 8)
- `models/pregunta` (línea 9)
- `config/constantes` (línea 10)

**Es importado por:**
- `core/logica_juego.py` (líneas 7-10)
- `ui/Pygame/Estados/Gameplay.py` (línea 13)
- `ui/consola/juego_consola.py`

### utils/algoritmos.py
**Importa de:** Ninguno (algoritmos puros)

**Es importado por:**
- `data/repositorio_usuarios.py` (línea 9)

### utils/validaciones.py
**Importa de:** Ninguno (validaciones puras)

**Es importado por:**
- `core/logica_preguntas.py` (línea 8)

### utils/formateadores.py
**Importa de:**
- `config/constantes` (línea 7)

**Es importado por:**
- `core/logica_preguntas.py` (línea 7)
- `ui/consola/juego_consola.py`

### core/logica_puntaje.py
**Importa de:**
- `config/constantes` (línea 7)

**Es importado por:**
- `core/logica_juego.py` (línea 28)

### core/logica_buffeos.py
**Importa de:**
- `data/archivos_json` (línea 7)
- `config/constantes` (líneas 8-13)

**Es importado por:**
- `core/logica_juego.py` (líneas 20-26)
- `core/logica_preguntas.py` (línea 9)
- `ui/Pygame/Estados/Gameplay.py` (línea 22)
- `ui/Pygame/Estados/SeleccionObjeto.py`

### core/logica_minijuego.py
**Importa de:**
- `random` (biblioteca estándar)
- `config/constantes` (línea 8)

**Es importado por:**
- `ui/consola/minijuego_consola.py`
- `ui/Pygame/Estados/Minijuego.py`

### core/logica_preguntas.py
**Importa de:**
- `utils/formateadores` (línea 7)
- `utils/validaciones` (línea 8)
- `core/logica_buffeos` (línea 9)

**Es importado por:**
- `core/logica_juego.py` (líneas 13-18)
- `ui/Pygame/Estados/Gameplay.py` (línea 21)

### core/logica_juego.py (ORCHESTRATOR PRINCIPAL)
**Importa de:**
- `data/repositorio_preguntas` (líneas 7-10)
- `data/repositorio_usuarios` (línea 12)
- `core/logica_preguntas` (líneas 13-18)
- `core/logica_buffeos` (líneas 20-26)
- `core/logica_puntaje` (línea 28)
- `config/constantes` (líneas 29-34)

**Es importado por:**
- `ui/consola/juego_consola.py`
- `ui/Pygame/Estados/Gameplay.py` (líneas 14-19)

## 🔒 Verificación de Principios

### ✅ Separación Core/UI
**NINGÚN archivo en `core/` importa pygame** ✓
- Verificado manualmente en todos los archivos de core/
- Toda la UI está encapsulada en `ui/`

### ✅ Arquitectura en Capas
```
UI (consola, pygame) 
  ↓ (solo puede importar de core, data, models, utils, config)
Core (lógica de negocio)
  ↓ (solo puede importar de data, models, utils, config)
Data (persistencia)
  ↓ (solo puede importar de models, utils, config)
Models (estructuras de datos)
  ↓ (no importa nada del proyecto)
Utils (algoritmos genéricos)
  ↓ (puede importar solo de config)
Config (constantes)
  ↓ (no importa nada del proyecto)
```

### ✅ Sin Dependencias Circulares
- Todas las importaciones fluyen en una sola dirección
- No hay ciclos en el grafo de dependencias

## 📝 Notas para la Defensa

1. **Patrón Repository**: `data/` encapsula toda la persistencia
2. **Patrón Facade**: `core/logica_juego.py` simplifica acceso a múltiples subsistemas
3. **Separation of Concerns**: Cada módulo tiene una responsabilidad clara
4. **Dependency Injection**: Las funciones reciben datos, no consultan directamente archivos
5. **Testabilidad**: La lógica core puede ser testeada sin UI
6. **Reutilización**: La misma lógica sirve para consola y pygame
