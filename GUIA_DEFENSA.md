# 📖 Guía para Defensa del Proyecto Final-beta

## 🎯 Objetivo del Proyecto

Juego de trivia de mitología griega con:
- **Sistema de niveles progresivos** (3 niveles de dificultad)
- **Sistema de buffeos y objetos especiales** (espada, armadura, raciones, bolsa de monedas)
- **Minijuego** "Guardianes de Piedra" para obtener objetos
- **Dos interfaces**: Consola y Pygame
- **Persistencia de datos**: Usuarios, preguntas (CSV), estado de buffs (JSON)

---

## 📐 Estructura del Proyecto

### Capas de Arquitectura

```
┌─────────────────────────────────────────────┐
│  UI Layer (Presentación)                    │
│  - ui/consola/: Interfaz de texto           │
│  - ui/Pygame/: Interfaz gráfica             │
└─────────────┬───────────────────────────────┘
              │ (usa)
┌─────────────▼───────────────────────────────┐
│  Core Layer (Lógica de Negocio)             │
│  - logica_juego.py: Orquestador principal   │
│  - logica_preguntas.py: Evaluación          │
│  - logica_buffeos.py: Sistema de objetos    │
│  - logica_puntaje.py: Cálculo de puntos     │
│  - logica_minijuego.py: Minijuego           │
└─────────────┬───────────────────────────────┘
              │ (usa)
┌─────────────▼───────────────────────────────┐
│  Data Layer (Persistencia)                  │
│  - repositorio_usuarios.py: CRUD usuarios   │
│  - repositorio_preguntas.py: Carga CSV      │
│  - archivos_json.py: Operaciones JSON       │
└─────────────┬───────────────────────────────┘
              │ (usa)
┌─────────────▼───────────────────────────────┐
│  Models Layer (Estructuras de Datos)        │
│  - usuario.py: Modelo de usuario            │
│  - pregunta.py: Modelo de pregunta          │
│  - partida.py: Estado de partida            │
│  - objeto_buff.py: Objetos especiales       │
└─────────────────────────────────────────────┘

Módulos auxiliares (usados por todas las capas):
- utils/: Algoritmos manuales, validaciones, formateadores
- config/: Constantes y mensajes centralizados
```

---

## 🏗️ Principios de Programación Aplicados

### 1. Separación de Responsabilidades (Separation of Concerns)

**¿Qué es?**
Cada módulo tiene una única responsabilidad bien definida.

**¿Cómo se aplica en el proyecto?**
- **Core**: Solo lógica, NO maneja UI
- **Data**: Solo persistencia, NO lógica de negocio
- **Models**: Solo estructuras de datos, NO operaciones
- **UI**: Solo presentación, NO cálculos

**Ejemplo para explicar:**
```python
# ❌ ANTES (malo): Todo mezclado
def procesar_pregunta(pregunta):
    print("Pregunta:", pregunta)  # UI mezclada con lógica
    puntos = calcular_puntos()    # Lógica
    guardar_en_archivo(puntos)    # Persistencia
    
# ✅ DESPUÉS (bueno): Separado
# En core/logica_juego.py (solo lógica)
def procesar_pregunta(pregunta):
    return calcular_resultado(pregunta)
    
# En ui/consola/ (solo UI)
def mostrar_pregunta(pregunta):
    print("Pregunta:", pregunta)
    
# En data/ (solo persistencia)
def guardar_estadisticas(datos):
    guardar_json(archivo, datos)
```

---

### 2. Algoritmos Manuales (Sin Built-ins Prohibidos)

**¿Por qué?**
Demuestra comprensión profunda de cómo funcionan los algoritmos.

**Implementaciones manuales en el proyecto:**

#### Suma de lista (en `utils/algoritmos.py`)
```python
# ❌ Prohibido: sum()
def mi_sum(lista):
    total = 0
    for valor in lista:
        total = total + valor
    return total
```

#### Máximo de lista
```python
# ❌ Prohibido: max()
def mi_max(lista):
    if not lista:
        return 0
    maximo = lista[0]
    i = 1
    while i < len(lista):
        if lista[i] > maximo:
            maximo = lista[i]
        i = i + 1
    return maximo
```

#### Ordenamiento (Insertion Sort en `data/repositorio_usuarios.py`)
```python
# ❌ Prohibido: sorted() o .sort()
def ordenar_ranking(ranking):
    for i in range(1, len(ranking)):
        usuario_actual = ranking[i]
        j = i - 1
        while j >= 0 and ranking[j]["mejor_puntaje"] < usuario_actual["mejor_puntaje"]:
            ranking[j + 1] = ranking[j]
            j -= 1
        ranking[j + 1] = usuario_actual
    return ranking
```

#### Mezcla de opciones (Fisher-Yates en `data/repositorio_preguntas.py`)
```python
# ❌ Prohibido: random.shuffle()
def mezclar_opciones(opciones):
    mezcladas = opciones[:]
    i = len(mezcladas) - 1
    while i > 0:
        j = random.randint(0, i)
        # Intercambiar posiciones
        temp = mezcladas[i]
        mezcladas[i] = mezcladas[j]
        mezcladas[j] = temp
        i = i - 1
    return mezcladas
```

---

### 3. UN SOLO return por Función

**¿Por qué?**
Facilita debugging y seguimiento del flujo del programa.

**Estrategia usada:** Variables de control

**Ejemplo en `models/usuario.py`:**
```python
def obtener_mejor_puntaje(usuario):
    # Variable de control para el resultado
    resultado = 0
    
    # Verificar si existe la clave "puntajes"
    tiene_puntajes = False
    for clave in usuario:
        if clave == "puntajes":
            tiene_puntajes = True
            break
    
    if tiene_puntajes and len(usuario["puntajes"]) > 0:
        mejor = usuario["puntajes"][0]
        i = 1
        while i < len(usuario["puntajes"]):
            if usuario["puntajes"][i] > mejor:
                mejor = usuario["puntajes"][i]
            i = i + 1
        resultado = mejor
    
    return resultado  # UN SOLO return al final
```

---

### 4. Tipado de Funciones

**¿Por qué?**
Mejora legibilidad y ayuda a prevenir errores de tipo.

**Ejemplo en `core/logica_preguntas.py`:**
```python
def evaluar_respuesta(
    respuesta_usuario: str, 
    opciones: list, 
    respuesta_correcta: str, 
    nombre_usuario: str
) -> dict:
    """Evalúa una respuesta del usuario."""
    # Implementación...
    return resultado
```

**Tipos usados en el proyecto:**
- `str`: Cadenas de texto
- `int`: Números enteros
- `float`: Números decimales
- `bool`: Booleanos
- `list`: Listas
- `dict`: Diccionarios
- `-> tipo`: Tipo de retorno

---

### 5. Sin usar .get() para cumplir principios

**¿Por qué no usar .get()?**
Es un método built-in. El proyecto requiere acceso manual.

**Solución: Búsqueda manual**

```python
# ❌ Prohibido:
valor = diccionario.get("clave", default)

# ✅ Permitido (búsqueda manual):
valor = default
for clave in diccionario:
    if clave == "clave":
        valor = diccionario[clave]
        break
```

**Ejemplo en `models/usuario.py`:**
```python
def obtener_mejor_puntaje(usuario):
    # Buscar manualmente si existe "puntajes"
    tiene_puntajes = False
    for clave in usuario:
        if clave == "puntajes":
            tiene_puntajes = True
            break
    
    if not tiene_puntajes or len(usuario["puntajes"]) == 0:
        return 0
    # ...
```

---

## 🎮 Flujo de Ejecución del Juego

### Inicialización
```
1. Main.py ejecuta ui/consola/menu_consola.py
   - Muestra menú de opciones
   - Captura nombre de usuario

2. Usuario selecciona "Jugar"
   - Llama a ui/consola/juego_consola.py
   
3. juego_consola.py inicializa:
   - Carga preguntas desde CSV (data/repositorio_preguntas.py)
   - Inicializa estado de partida
```

### Gameplay Loop
```
Para cada nivel (1, 2, 3):
  Para cada pregunta del nivel:
    1. Obtener pregunta aleatoria (core/logica_juego.py)
       ↓
    2. Mostrar pregunta (UI)
       ↓
    3. Capturar respuesta usuario (UI)
       ↓
    4. Evaluar respuesta (core/logica_preguntas.py)
       ↓
    5. Calcular puntos base (core/logica_puntaje.py)
       ↓
    6. Calcular buffeo si aplica (core/logica_buffeos.py)
       ↓
    7. Usar objetos especiales si aplica
       ↓
    8. Actualizar racha (core/logica_preguntas.py)
       ↓
    9. Verificar condición de fin (core/logica_juego.py)
       ↓
   10. Mostrar resultado (UI)
```

### Finalización
```
1. Construir estadísticas finales (core/logica_juego.py)
   ↓
2. Guardar estadísticas (data/repositorio_usuarios.py)
   ↓
3. Verificar merecimiento de objeto (core/logica_buffeos.py)
   ↓
4. Si merece objeto → Minijuego
   ↓
5. Mostrar resumen final (UI)
```

---

## 🔧 Sistemas Especiales

### Sistema de Buffeos

**Rachas de respuestas correctas:**
- Racha > 3: +1 punto
- Racha > 5: +3 puntos
- Racha > 7: +5 puntos

**Implementación en `core/logica_buffeos.py`:**
```python
def calcular_puntos_buffeo(racha_actual, objeto):
    puntos_racha = 0
    
    if racha_actual > 7:
        puntos_racha = PUNTOS_BUFFEO_POR_RACHA[7]  # 5 puntos
    elif racha_actual > 5:
        puntos_racha = PUNTOS_BUFFEO_POR_RACHA[5]  # 3 puntos
    elif racha_actual > 3:
        puntos_racha = PUNTOS_BUFFEO_POR_RACHA[3]  # 1 punto
    
    puntos_objeto = 0
    if objeto == "espada":
        puntos_objeto = 2  # Espada da +2
    
    return {
        "puntos": puntos_racha + puntos_objeto,
        "por_racha": puntos_racha,
        "por_objeto": puntos_objeto
    }
```

### Objetos Especiales

#### 1. Espada de la Esfinge
- **Efecto**: +2 puntos por respuesta correcta
- **Bonus**: Permite un reintento especial
- **Consumible**: NO

#### 2. Armadura de la Esfinge
- **Efecto**: Protege contra UNA respuesta incorrecta
- **Consumible**: SÍ (se elimina al usarse)

#### 3. Raciones de la Esfinge
- **Efecto**: Recupera 3 puntos al fallar
- **Consumible**: SÍ

#### 4. Bolsa de Monedas
- **Efecto**: Duplica puntos de última respuesta correcta
- **Consumible**: SÍ

**Persistencia de objetos:**
Archivo `EstadoBuff.json`:
```json
{
  "Juan": {
    "objeto_excepcional": "espada",
    "vidas_extra": 2
  }
}
```

### Minijuego "Guardianes de Piedra"

**Objetivo**: Navegar matriz 5x5 desde (0,0) hasta (4,4)

**Regla**: Solo puedes moverte a casillas con valor MAYOR al actual

**Generación garantizada de solución** (en `core/logica_minijuego.py`):
```python
def generar_matriz_resoluble(tamano):
    # 1. Crear matriz vacía
    matriz = inicializar_matriz_vacia(tamano)
    
    # 2. Generar camino garantizado (recursivo)
    camino = generar_camino_garantizado(tamano)
    
    # 3. Asignar valores crecientes al camino
    asignar_valores_a_camino(matriz, camino)
    
    # 4. Rellenar resto con valores válidos
    rellenar_matriz_con_valores_seguro(matriz, camino)
    
    return matriz
```

---

## 📚 Patrones de Diseño Aplicados

### 1. Repository Pattern
**¿Dónde?** `data/repositorio_*.py`

**¿Para qué?**
Abstrae el acceso a datos. Si mañana cambiamos de JSON a SQL, solo modificamos repositorios.

### 2. Facade Pattern
**¿Dónde?** `core/logica_juego.py`

**¿Para qué?**
Simplifica la interacción con múltiples subsistemas (preguntas, buffeos, puntaje).

### 3. Model-View-Controller (MVC)
- **Model**: `models/` y `data/`
- **View**: `ui/consola/` y `ui/Pygame/`
- **Controller**: `core/`

---

## 🎓 Preguntas Frecuentes en la Defensa

### Q1: ¿Por qué separar consola y pygame?
**R:** Para demostrar que la lógica core es **reutilizable** e **independiente de la UI**. La misma lógica sirve para ambas interfaces.

### Q2: ¿Por qué no usar funciones built-in como sum(), max()?
**R:** Para demostrar **comprensión profunda** de los algoritmos. Implementar manualmente muestra que entendemos cómo funcionan internamente.

### Q3: ¿Por qué UN SOLO return?
**R:** Facilita el **debugging** y hace el flujo más **predecible**. Sabemos que siempre hay un único punto de salida.

### Q4: ¿Cómo garantizan que el minijuego tiene solución?
**R:** Usamos un **algoritmo recursivo** que primero genera un camino válido, luego asigna valores crecientes a ese camino, garantizando solución.

### Q5: ¿Por qué usar diccionarios en lugar de clases?
**R:** Para practicar **estructuras de datos fundamentales**. Los diccionarios son más flexibles y no requieren definir clases formales.

### Q6: ¿Cómo manejan la persistencia?
**R:** Usamos **JSON** para usuarios y buffs (estructurado), y **CSV** para preguntas (tabla simple). Cada uno tiene su repositorio.

---

## ✅ Checklist de Defensa

Antes de la defensa, verificar:

- [ ] Puedo explicar la arquitectura en capas
- [ ] Puedo mostrar separación core/UI
- [ ] Puedo explicar 3+ algoritmos manuales implementados
- [ ] Puedo mostrar ejemplos de UN SOLO return
- [ ] Puedo explicar el sistema de buffeos
- [ ] Puedo explicar cómo funciona el minijuego
- [ ] Puedo mostrar el flujo completo de una partida
- [ ] Puedo explicar los patrones de diseño usados
- [ ] Puedo demostrar el juego funcionando (consola Y pygame)
- [ ] Puedo explicar cómo se persisten los datos

---

## 🚀 Conclusión

Este proyecto demuestra:
1. **Arquitectura en capas** bien estructurada
2. **Separación de responsabilidades** clara
3. **Algoritmos fundamentales** implementados manualmente
4. **Reutilización de código** (misma lógica para 2 UIs)
5. **Persistencia de datos** con múltiples formatos
6. **Gameplay complejo** con buffeos y objetos
7. **Generación algorítmica** de minijuego resoluble

¡Buena suerte en la defensa! 🎓
