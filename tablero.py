class Tablero:
    def __init__(self):
        self.casillas = [{"numero": i, "tipo": "normal", "fichas": []} for i in range(1, 69)]
        self.seguros = [12, 17, 29, 34, 46, 51, 63, 68]
        self.salidas = {"rojo": 5, "azul": 22, "verde": 39, "amarillo": 56}
        self.carcel = {color: [] for color in self.salidas.keys()}  # Fichas capturadas

        # Marcar casillas especiales
        for i in self.seguros:
            self.casillas[i - 1]["tipo"] = "seguro"
        for color, pos in self.salidas.items():
            self.casillas[pos - 1]["tipo"] = f"salida_{color}"

    def aplicar_circularidad(self, posicion):
        """Transforma una posición aplicando circularidad"""
        return (posicion - 1) % 68 + 1

    def colocar_ficha(self, ficha, posicion):
        """Coloca una ficha en una casilla específica aplicando circularidad"""
        posicion = self.aplicar_circularidad(posicion)
        self.casillas[posicion - 1]["fichas"].append(ficha)
        ficha.posicion = posicion

    def remover_ficha(self, ficha):
        """Elimina una ficha de su casilla actual"""
        self.casillas[ficha.posicion - 1]["fichas"].remove(ficha)

    def obtener_casilla(self, posicion):
        """Devuelve la casilla en una posición dada aplicando circularidad"""
        posicion = self.aplicar_circularidad(posicion)
        return self.casillas[posicion - 1]
