# =============================================================================
# INTERFACES ABSTRACTAS PARA UI
# =============================================================================
# Define qué métodos debe implementar cualquier interfaz (consola o pygame)
# =============================================================================

class InterfazJuego:
    """
    Interfaz base que debe implementar cualquier UI del juego.
    
    La versión consola y la versión pygame implementarán estos métodos.
    Esto permite cambiar la UI sin modificar la lógica del juego.
    """
    
    def mostrar_menu_principal(self) -> str:
        """
        Muestra el menú principal y retorna la opción elegida.
        
        En consola: Imprime opciones y lee input
        En pygame: Muestra panel con botones y espera clic
        
        Retorna:
            str: Opción seleccionada ('1', '2', '3', etc.)
        """
        pass
    
    def mostrar_pregunta(self, pregunta: dict) -> str:
        """
        Muestra una pregunta y retorna la respuesta del usuario.
        
        En consola: Imprime pregunta y opciones, lee respuesta
        En pygame: Muestra pregunta en panel gráfico, espera clic en opción
        
        Parámetros:
            pregunta (dict): Datos de la pregunta
        
        Retorna:
            str: Respuesta del usuario ('A', 'B', 'C', 'D')
        """
        pass
    
    def mostrar_resultado(self, resultado: dict) -> None:
        """
        Muestra el resultado de una respuesta.
        
        En consola: Imprime mensaje de resultado
        En pygame: Muestra animación o panel con el resultado
        
        Parámetros:
            resultado (dict): Datos del resultado
        """
        pass
    
    def pedir_nombre_usuario(self) -> str:
        """
        Solicita el nombre del usuario.
        
        En consola: Imprime prompt y lee input
        En pygame: Muestra cuadro de texto para ingresar nombre
        
        Retorna:
            str: Nombre del usuario
        """
        pass
    
    def mostrar_estadisticas(self, estadisticas: dict) -> None:
        """
        Muestra las estadísticas de un usuario.
        
        En consola: Imprime tabla de estadísticas
        En pygame: Muestra panel gráfico con estadísticas
        
        Parámetros:
            estadisticas (dict): Estadísticas del usuario
        """
        pass
    
    def mostrar_ranking(self, ranking: list) -> None:
        """
        Muestra el ranking de jugadores.
        
        En consola: Imprime lista ordenada
        En pygame: Muestra tabla gráfica
        
        Parámetros:
            ranking (list): Lista de jugadores ordenados
        """
        pass
    
    def mostrar_mensaje(self, mensaje: str) -> None:
        """
        Muestra un mensaje al usuario.
        
        En consola: Imprime el mensaje
        En pygame: Muestra diálogo o notificación
        
        Parámetros:
            mensaje (str): Mensaje a mostrar
        """
        pass
    
    def confirmar_accion(self, pregunta: str) -> bool:
        """
        Pide confirmación al usuario.
        
        En consola: Muestra pregunta y espera s/n
        En pygame: Muestra diálogo con botones Sí/No
        
        Parámetros:
            pregunta (str): Pregunta a confirmar
        
        Retorna:
            bool: True si confirma, False si cancela
        """
        pass
    
    def seleccionar_opcion(self, opciones: list, titulo: str = "") -> str:
        """
        Muestra opciones y retorna la seleccionada.
        
        En consola: Imprime lista numerada y lee selección
        En pygame: Muestra menú gráfico con opciones
        
        Parámetros:
            opciones (list): Lista de opciones
            titulo (str): Título opcional
        
        Retorna:
            str: Opción seleccionada
        """
        pass
