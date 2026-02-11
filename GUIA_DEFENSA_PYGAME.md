# 🎮 Guía de Defensa: Pygame

## 📋 Índice Rápido
1. [Arquitectura General](#arquitectura-general)
2. [Máquina de Estados](#máquina-de-estados)
3. [Game Loop](#game-loop)
4. [Componentes Reutilizables](#componentes-reutilizables)
5. [Separación UI/Lógica](#separación-uilógica)
6. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🏗️ Arquitectura General

### Principios de Diseño Aplicados

1. **Separación de Responsabilidades**
   - `core/`: Lógica pura del juego (sin Pygame)
   - `ui/Pygame/`: Interfaz gráfica (usa core/)
   - `data/`: Acceso a archivos y persistencia
   - `models/`: Estructuras de datos

2. **Patrón MVC Adaptado**
   - **Model**: `core/` + `data/` + `models/`
   - **View**: `ui/Pygame/Estados/` (estados visuales)
   - **Controller**: `ui/Pygame/Juego.py` (máquina de estados)

3. **Componentes Reutilizables**
   - `ui/Pygame/componentes/boton.py`: Botones con hover
   - `ui/Pygame/utils/renderizado.py`: Utilidades de dibujo
   - `ui/Pygame/utils/eventos.py`: Manejo de eventos

---

## 🎰 Máquina de Estados

### ¿Qué es una Máquina de Estados?

Un patrón de diseño donde el programa puede estar en **uno de varios estados** a la vez, y cada estado maneja sus propios eventos y renderizado.

### Estados del Juego

```
Menu → Historia → Gameplay → SeleccionObjeto → Gameover
  ↓                   ↓            ↓
Rankings         Minijuego    Gameover
```

### Archivo Clave: `ui/Pygame/Juego.py`

```python
class Juego:
    def __init__(self):
        self.estados = {
            "Menu": menu(),
            "Gameplay": gameplay(),
            "Rankings": rankings(),
            # ...
        }
        self.estado_actual = "Menu"
    
    def ejecutar(self):
        while self.corriendo:
            # Cambiar de estado si es necesario
            if self.estados[self.estado_actual].done:
                self.estado_actual = self.estados[self.estado_actual].sig_estado
            
            # Ejecutar estado actual
            self.estados[self.estado_actual].update(dt)
            self.estados[self.estado_actual].draw(pantalla)
```

### Beneficios de la Máquina de Estados

1. **Modularidad**: Cada estado es independiente
2. **Mantenibilidad**: Fácil agregar/modificar estados
3. **Testabilidad**: Se puede probar cada estado por separado
4. **Claridad**: El flujo del programa es evidente

---

## 🔄 Game Loop

### Concepto

El **game loop** (bucle del juego) es el corazón de cualquier juego. Se ejecuta ~60 veces por segundo y:

1. **Procesa eventos** (clicks, teclado, cerrar ventana)
2. **Actualiza lógica** (mover objetos, calcular colisiones)
3. **Renderiza** (dibuja todo en pantalla)
4. **Controla FPS** (mantiene 60 frames por segundo)

### Implementación en `ui/Pygame/main.py`

```python
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    reloj = pygame.time.Clock()
    juego = Juego()
    
    while juego.corriendo:
        # 1. PROCESAR EVENTOS
        eventos = pygame.event.get()
        for evento in eventos:
            juego.procesar_evento(evento)
        
        # 2. ACTUALIZAR LÓGICA
        dt = reloj.tick(FPS)  # Delta time
        juego.actualizar(dt)
        
        # 3. RENDERIZAR
        juego.renderizar(pantalla)
        pygame.display.flip()  # Actualizar pantalla
```

### Componentes del Game Loop

- **Delta Time (dt)**: Tiempo transcurrido desde el último frame
- **FPS**: Frames Por Segundo (60 en este proyecto)
- **eventos**: Cola de eventos de Pygame (clicks, teclado, etc.)

---

## 🧩 Componentes Reutilizables

### Componente: Boton

**Archivo**: `ui/Pygame/componentes/boton.py`

**Propósito**: Botón reutilizable con:
- Imágenes de estado (normal/hover)
- Detección de clicks
- Renderizado automático

**Uso**:
```python
from ui.Pygame.componentes import Boton

boton = Boton(x=300, y=200, ancho=200, alto=60, 
              texto="JUGAR", fuente=mi_fuente)

# En el game loop:
boton.actualizar(pygame.mouse.get_pos())  # Hover
if evento.type == pygame.MOUSEBUTTONDOWN:
    if boton.fue_clickeado(evento.pos):
        # Botón clickeado!
```

**Beneficio**: Evita duplicar código de botones en cada estado.

### Utilidades de Renderizado

**Archivo**: `ui/Pygame/utils/renderizado.py`

Funciones comunes:
- `renderizar_texto()`: Texto centrado
- `renderizar_rectangulo_con_borde()`: Paneles
- `limpiar_pantalla()`: Fondo sólido

**Beneficio**: Centraliza lógica de dibujo, evita repetición.

### Utilidades de Eventos

**Archivo**: `ui/Pygame/utils/eventos.py`

Funciones comunes:
- `detectar_click_en_botones()`: Qué botón fue clickeado
- `obtener_posicion_mouse()`: Wrapper de pygame.mouse.get_pos()

**Beneficio**: Simplifica detección de eventos.

---

## 🔀 Separación UI/Lógica

### Principio Fundamental

**Pygame SOLO se encarga de mostrar y detectar eventos.**
**La lógica del juego está en `core/`.**

### Flujo de Procesamiento de Respuesta

```
1. Usuario hace click en opción → Pygame detecta (Gameplay.py)
2. Gameplay llama a core/logica_juego.py
3. Core procesa respuesta (calcula puntos, racha, buffeo)
4. Core devuelve resultado a Gameplay
5. Gameplay actualiza visualización
```

### Ejemplo Concreto

**Archivo**: `ui/Pygame/Estados/Gameplay/gameplay.py` (línea ~231)

```python
# ❌ MAL: Pygame no debe calcular puntos
puntos = dificultad * 2 + racha  # NO

# ✅ BIEN: Delegar al core
resultado = procesar_pregunta_completa(
    pregunta,
    nombre_usuario,
    racha,
    letra_respuesta,
    intento_actual,
    intentos_maximos
)
puntos = resultado.get("puntos", 0)
```

### Beneficios de la Separación

1. **Testabilidad**: Core se puede probar sin Pygame
2. **Reutilización**: Misma lógica para UI consola y Pygame
3. **Mantenibilidad**: Cambiar cálculos sin tocar UI
4. **Portabilidad**: Fácil migrar a otra librería gráfica

---

## ❓ Preguntas Frecuentes en Defensa

### 1. "¿Cómo funciona la máquina de estados?"

**Respuesta**:
> La máquina de estados es un patrón de diseño donde el programa tiene varios estados (Menu, Gameplay, Rankings, etc.) y solo uno está activo a la vez. Cada estado maneja sus propios eventos y renderizado. Cuando un estado termina (done=True), indica el siguiente estado (sig_estado) y la máquina cambia automáticamente. Esto modulariza el código y hace que cada pantalla sea independiente.

**Archivo clave**: `ui/Pygame/Juego.py`

---

### 2. "¿Qué es el game loop?"

**Respuesta**:
> El game loop es el bucle principal que se ejecuta ~60 veces por segundo. En cada iteración: (1) procesa eventos del usuario (clicks, teclado), (2) actualiza la lógica del juego (mover objetos, calcular estado), (3) renderiza todo en pantalla, y (4) controla el framerate a 60 FPS usando pygame.time.Clock(). Es el corazón de cualquier videojuego.

**Archivo clave**: `ui/Pygame/main.py`

---

### 3. "¿Cómo separaste lógica de Pygame?"

**Respuesta**:
> Separé el código en dos capas: (1) `core/` contiene toda la lógica pura del juego (calcular puntos, procesar respuestas, determinar racha) sin ninguna dependencia de Pygame. (2) `ui/Pygame/` solo se encarga de mostrar información y detectar eventos del usuario. Cuando el usuario hace algo, Pygame llama a funciones de core/ para procesar, recibe el resultado, y lo muestra. Esto permite probar la lógica independientemente y reutilizar el mismo core para la versión de consola.

**Archivos clave**: 
- `core/logica_juego.py` (lógica pura)
- `ui/Pygame/Estados/Gameplay/gameplay.py` (llama a core)

---

### 4. "¿Por qué creaste componentes reutilizables?"

**Respuesta**:
> Para aplicar el principio DRY (Don't Repeat Yourself). Antes, cada estado duplicaba código de botones. Ahora tengo un componente Boton en `ui/Pygame/componentes/boton.py` que todos los estados pueden usar. Esto reduce duplicación, facilita mantenimiento (un bug se arregla en un solo lugar), y hace el código más profesional. También creé utilidades de renderizado para centralizar funciones comunes como dibujar texto centrado.

**Archivos clave**:
- `ui/Pygame/componentes/boton.py`
- `ui/Pygame/utils/renderizado.py`

---

### 5. "¿Qué patrones de diseño usaste?"

**Respuesta**:
> Usé varios patrones: (1) **State Pattern** para la máquina de estados. (2) **MVC adaptado** donde core/data/models son el Model, ui/Pygame son las Views, y Juego.py es el Controller. (3) **Composition** en Gameplay que delega responsabilidades a gestores especializados (gestor_preguntas, gestor_hud, gestor_respuestas). (4) **Strategy Pattern** en core/ donde diferentes estrategias de cálculo de puntos se pueden cambiar fácilmente.

---

### 6. "Explica el flujo de una pregunta"

**Respuesta**:
> 1. Gameplay carga pregunta llamando a `obtener_pregunta_para_nivel()` de core.
> 2. Se crean botones con las opciones.
> 3. Usuario hace click, Gameplay detecta el evento.
> 4. Se llama a `procesar_pregunta_completa()` de core con la respuesta.
> 5. Core calcula si es correcta, puntos base, buffeo, puntos de objeto.
> 6. Core devuelve diccionario con resultado.
> 7. Gameplay actualiza puntos, racha, errores.
> 8. Se muestra resultado en pantalla.
> 9. Después de 3 segundos o ESPACIO, se carga siguiente pregunta.

**Archivo clave**: `ui/Pygame/Estados/Gameplay/gameplay.py`

---

### 7. "¿Cómo manejas el buffeo?"

**Respuesta**:
> El buffeo (puntos extra por racha) se maneja en core/logica_buffeos.py. Gameplay solo lo visualiza. Cuando la racha alcanza ciertos umbrales (3, 5, 7), core calcula puntos extra. Gameplay llama a `calcular_datos_buffeo_para_ui()` que devuelve datos para mostrar (puntos de racha, puntos de objeto). Luego Gameplay renderiza un panel dorado indicando el buffeo activo. La lógica está en core, la visualización en UI.

**Archivos clave**:
- `core/logica_buffeos.py` (lógica)
- `ui/Pygame/Estados/Gameplay/gameplay.py` (visualización)

---

### 8. "¿Por qué usas un solo return por función?"

**Respuesta**:
> Es un principio de este proyecto para mantener claridad y evitar salidas múltiples que dificulten el seguimiento del código. Cada función calcula su resultado en una variable y lo retorna al final. Esto hace el código más predecible, fácil de debuggear, y evita olvidar liberar recursos o ejecutar código de limpieza.

**Ejemplo**: Todas las funciones en `core/` y `ui/Pygame/componentes/`

---

### 9. "¿Cómo gestionas los eventos en Pygame?"

**Respuesta**:
> Pygame genera eventos (clicks, teclado, cerrar ventana) que se obtienen con `pygame.event.get()`. En el main loop, cada evento se pasa al estado actual mediante `get_event()`. El estado verifica el tipo (MOUSEBUTTONDOWN, KEYDOWN, QUIT) y actúa en consecuencia. Por ejemplo, Gameplay detecta clicks en botones de opciones y procesa la respuesta. Centralicé helpers en `ui/Pygame/utils/eventos.py` para simplificar detección.

**Archivo clave**: `ui/Pygame/Estados/Gameplay/gameplay.py` método `get_event()`

---

### 10. "¿Qué mejoras harías al código?"

**Respuesta**:
> (1) Extraer más lógica de renderizado a gestores especializados para reducir tamaño de Gameplay.py. (2) Implementar sistema de animaciones para transiciones entre estados. (3) Agregar sistema de sonidos. (4) Crear un gestor de recursos para cachear fuentes/imágenes globalmente. (5) Implementar tests unitarios para core/ usando pytest. (6) Agregar internacionalización para soportar múltiples idiomas.

---

## 📚 Archivos Críticos para la Defensa

### Top 10 Archivos a Conocer

1. **ui/Pygame/main.py** - Punto de entrada, game loop
2. **ui/Pygame/Juego.py** - Máquina de estados
3. **ui/Pygame/Estados/Gameplay/gameplay.py** - Estado principal del juego
4. **core/logica_juego.py** - Lógica central de procesamiento
5. **core/logica_buffeos.py** - Sistema de buffeos y objetos
6. **ui/Pygame/componentes/boton.py** - Componente reutilizable
7. **data/repositorio_preguntas.py** - Carga de preguntas
8. **config/constantes.py** - Configuración centralizada
9. **ui/Pygame/Botones.py** - Botones existentes del proyecto
10. **ui/Pygame/recursos.py** - Carga de fuentes e imágenes

---

## 🎯 Frases Clave para Impresionar

1. **"Implementé el patrón State para modularizar los estados del juego"**
2. **"Separé la lógica de negocio de la interfaz usando arquitectura en capas"**
3. **"Creé componentes reutilizables para aplicar el principio DRY"**
4. **"El game loop se ejecuta a 60 FPS controlado con pygame.time.Clock()"**
5. **"Pygame solo maneja eventos y renderizado, toda la lógica está en core/"**
6. **"Usé composición con gestores especializados para separar responsabilidades"**
7. **"El código sigue principios SOLID, especialmente Single Responsibility"**
8. **"Implementé tipado explícito y un solo return por función para claridad"**

---

## ✅ Checklist de Defensa

Antes de la defensa, asegúrate de poder:

- [ ] Explicar qué es una máquina de estados
- [ ] Describir el flujo del game loop
- [ ] Mostrar cómo se separa UI de lógica
- [ ] Explicar el patrón de componentes reutilizables
- [ ] Describir el flujo de procesamiento de una pregunta
- [ ] Explicar cómo funciona el sistema de buffeo
- [ ] Mencionar patrones de diseño aplicados
- [ ] Explicar por qué un solo return por función
- [ ] Describir la estructura de archivos del proyecto
- [ ] Proponer mejoras al código actual

---

**¡Suerte en tu defensa! 🎮✨**
