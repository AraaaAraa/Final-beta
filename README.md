**-ESPAÑOL-**

# 📜 Juego de Trivia Mitológica

Este proyecto simula un juego de trivia interactivo con temáticas de mitología griega, egipcia y hebrea. Incluye un sistema de buffs, objetos especiales, minijuegos y estadísticas avanzadas para los jugadores.

**🎯 ARQUITECTURA REORGANIZADA PARA PYGAME**: El código ha sido completamente reorganizado separando la lógica de negocio de la interfaz de usuario, facilitando la migración a Pygame. Ver [ARQUITECTURA.md](ARQUITECTURA.md) para detalles.

## 🛠️ Tecnologías Utilizadas

* Python 3.10+
* Arquitectura modular con separación de responsabilidades
* Estructuras de datos básicas (sin librerías externas)
* Algoritmos personalizados (ordenamiento, búsqueda, recorridos)
* Persistencia con archivos CSV y JSON
* Programación funcional
* Type hints para mejor documentación

## 📁 Estructura de Carpetas (Nueva Arquitectura)

```
SegundoParcial/
├── core/                          # Lógica de negocio (sin UI)
│   ├── logica_juego.py           # Orquestación del flujo del juego
│   ├── logica_buffeos.py         # Sistema de buffeos y objetos
│   ├── logica_preguntas.py       # Evaluación de preguntas
│   ├── logica_puntaje.py         # Cálculo de puntajes
│   └── logica_minijuego.py       # Lógica del minijuego
│
├── models/                        # Modelos de datos
│   ├── pregunta.py               # Estructura de preguntas
│   ├── usuario.py                # Estructura de usuarios
│   ├── partida.py                # Estado de partidas
│   └── objeto_buff.py            # Objetos especiales
│
├── data/                          # Capa de persistencia
│   ├── archivos_json.py          # Operaciones JSON
│   ├── repositorio_usuarios.py   # CRUD de usuarios
│   └── repositorio_preguntas.py  # Carga de preguntas
│
├── ui/                            # Interfaces de usuario
│   ├── interfaces.py             # Interfaces abstractas
│   └── consola/                  # Implementación consola
│       ├── menu_consola.py
│       ├── juego_consola.py
│       └── minijuego_consola.py
│
├── utils/                         # Utilidades
│   ├── validaciones.py
│   ├── algoritmos.py
│   └── formateadores.py
│
├── config/                        # Configuraciones
│   ├── constantes.py
│   └── mensajes.py
│
├── assets/                        # Archivos de datos
│   ├── preguntas.csv
│   ├── Usuarios.json
│   └── EstadoBuff.json
│
├── Main.py                        # Punto de entrada
├── ARQUITECTURA.md                # Documentación de arquitectura
└── README.md                      # Este archivo
```

## 📌 Características Principales

* ✅ **Separación UI/Lógica**: La lógica del juego está completamente independiente de la interfaz
* ✅ **Sistema de trivia** con 3 niveles de dificultad (10 preguntas por partida)
* ✅ **Bonificaciones por racha** de respuestas correctas
* ✅ **Objetos especiales**: Espada, Armadura, Raciones, Bolsa de Monedas
* ✅ **Estadísticas detalladas** por jugador
* ✅ **Ranking global** de mejores puntajes
* ✅ **Minijuego "Guardianes de Piedra"** con lógica recursiva
* ✅ **Comentarios descriptivos** en todas las funciones
* ✅ **Preparado para Pygame**: Fácil migración a interfaz gráfica

## 🧠 Principios de Programación Aplicados

* **Modularización**: Código organizado por responsabilidades
* **Separación de capas**: Core, Models, Data, UI, Utils, Config
* **Algoritmos manuales**: Implementación sin usar built-ins (sum, max, min, etc.)
* **Un solo return** por función
* **Validación exhaustiva** de entradas
* **Persistencia de datos** en JSON/CSV
* **Documentación completa** de cada función

## ▶️ ¿Cómo Ejecutarlo?

1. Asegurate de tener **Python 3.10 o superior** instalado.
2. Cloná o descargá el repositorio completo.
3. Abrí una terminal en la carpeta del proyecto.
4. Ejecutá el programa principal:

   ```bash
   python Main.py
   ```

5. Seguí las instrucciones del menú:
   - **Opción 1**: Juego principal
   - **Opción 2**: Ver estadísticas personales
   - **Opción 3**: Ver ranking global
   - **Opción 4**: Mini juego "Guardianes de Piedra"
   - **Opción 5**: Salir

## 🎮 Reglas del Juego

### Juego Principal
- Se presentan 10 preguntas divididas en 3 niveles
- Cada nivel tiene distinta cantidad de preguntas (5, 3, 2)
- Puntos según dificultad: 1, 2 o 3 puntos
- **Sistema de rachas**: Puntos extra por respuestas correctas consecutivas
  - Racha > 3: +1 punto
  - Racha > 5: +3 puntos
  - Racha > 7: +5 puntos
- **Objetos especiales** (se desbloquean con 8+ aciertos en 10 preguntas):
  - **Espada**: +2 puntos por respuesta correcta + 1 reintento
  - **Armadura**: Protección automática contra 1 error
  - **Raciones**: Recupera 3 puntos al fallar
  - **Bolsa de Monedas**: Duplica puntos de última respuesta correcta
- Fin de partida: 2 errores o completar todos los niveles

### Minijuego "Guardianes de Piedra"
- Matriz 5x5 con valores aleatorios
- Objetivo: Llegar de (0,0) a (4,4)
- Regla: Solo moverte a casillas con valores MAYORES
- Genera matriz con solución garantizada
- Opciones: Reiniciar o salir en cualquier momento

## 💡 Migración a Pygame

El código está **completamente preparado** para migrar a Pygame:

1. **Mantener sin cambios**: `core/`, `models/`, `data/`, `utils/`, `config/`
2. **Crear nueva UI**: Implementar `ui/pygame_ui/` con interfaz gráfica
3. **Actualizar Main.py**: Cambiar `ejecutar_menu_consola()` por `ejecutar_menu_pygame()`

**La lógica del juego NO necesita modificarse**. Solo se reemplaza la capa de presentación.

Ver [ARQUITECTURA.md](ARQUITECTURA.md) para detalles completos de migración.

## 📚 Documentación Adicional

- [ARQUITECTURA.md](ARQUITECTURA.md): Documentación completa de la arquitectura
- Cada archivo incluye comentarios descriptivos según especificación
- Cada función tiene bloque de comentarios con:
  - Descripción
  - Uso en Pygame
  - Parámetros
  - Retorno
  - Ejemplo de uso

## 🏆 Características Técnicas Destacadas

- ✅ Sin librerías externas (Python puro)
- ✅ Algoritmos implementados manualmente
- ✅ Type hints para mejor documentación
- ✅ Código modular y reutilizable
- ✅ Separación completa UI/Lógica
- ✅ Arquitectura escalable
- ✅ Preparado para testing

---

**-ENGLISH-**

# 📜 Mythological Trivia Game

This project simulates an interactive trivia game focused on Greek, Egyptian, and Hebrew mythology. It includes a buff system, unlockable special items, minigames, and detailed player statistics.

**🎯 REORGANIZED ARCHITECTURE FOR PYGAME**: The code has been completely reorganized to separate business logic from the user interface, facilitating migration to Pygame. See [ARQUITECTURA.md](ARQUITECTURA.md) for details.

## 🛠️ Technologies Used

* Python 3.10+
* Modular architecture with separation of concerns
* Basic data structures (no external libraries)
* Custom algorithms (sorting, searching, traversal)
* CSV and JSON file persistence
* Functional programming
* Type hints for better documentation

## 📁 New Folder Structure

See Spanish section above for complete structure. Key directories:
- **core/**: Business logic (no UI dependencies)
- **models/**: Data structures
- **data/**: Persistence layer
- **ui/consola/**: Console interface implementation
- **utils/**: Reusable utilities
- **config/**: Game configuration
- **assets/**: Data files

## 📌 Main Features

* ✅ **UI/Logic Separation**: Game logic completely independent from interface
* ✅ **Trivia system** with 3 difficulty levels (10 questions per game)
* ✅ **Streak bonuses** for consecutive correct answers
* ✅ **Special items**: Sword, Armor, Rations, Coin Bag
* ✅ **Detailed statistics** per player
* ✅ **Global ranking** of top scores
* ✅ **"Stone Guardians" minigame** with recursive logic
* ✅ **Descriptive comments** on all functions
* ✅ **Pygame-ready**: Easy migration to graphical interface

## ▶️ How to Run

1. Make sure you have **Python 3.10 or higher** installed.
2. Clone or download the complete repository.
3. Open a terminal in the project folder.
4. Run:

   ```bash
   python Main.py
   ```

5. Follow the menu to play, view stats, or access the minigame.

## 💡 Pygame Migration

The code is **completely ready** for Pygame migration:

1. **Keep unchanged**: `core/`, `models/`, `data/`, `utils/`, `config/`
2. **Create new UI**: Implement `ui/pygame_ui/` with graphical interface
3. **Update Main.py**: Change `ejecutar_menu_consola()` to `ejecutar_menu_pygame()`

See [ARQUITECTURA.md](ARQUITECTURA.md) for complete details.

## 🏆 Technical Highlights

- ✅ No external libraries (pure Python)
- ✅ Manually implemented algorithms
- ✅ Type hints for better documentation
- ✅ Modular and reusable code
- ✅ Complete UI/Logic separation
- ✅ Scalable architecture
- ✅ Test-ready
