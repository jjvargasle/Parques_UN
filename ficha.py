
from tablero import Tablero

class Ficha:
    def __init__(self, color):
        self.color = color
        self.posicion = None  # None indica que aún no ha salido
        self.en_llegada = None  # None significa que aún no ha entrado a la llegada
        self.en_meta = False  # Se vuelve True cuando llega a la meta

        # Casilla en la que cada equipo entra a su llegada
        self.inicio_llegada = {"rojo": 68, "azul": 17, "verde": 34, "amarillo": 51}[color]

    def puede_moverse(self, tablero, movimientos):
        """
        Determina si la ficha puede moverse y devuelve la posición final posible.
        Si la ficha está en la llegada, se verifica si el movimiento es exacto.
        """

        # 1. Si la ficha está en la cárcel, no puede moverse
        if self.posicion is None:
            return None  

        # 2. Si la ficha ya llegó a la meta, no se puede mover
        if self.en_meta:
            return None  

        nueva_pos = self.posicion + movimientos

        # 3. Si la ficha aún no ha entrado a la llegada
        if self.en_llegada is None:
            if self.posicion <= self.inicio_llegada < nueva_pos:  # Si entra a la llegada
                self.en_llegada = nueva_pos - self.inicio_llegada - 1
                tablero.remover_ficha(self)  # Se elimina del tablero normal
                return self.en_llegada  # Se mueve directamente a la casilla de llegada

            # Revisar bloqueos en el camino
            posiciones_a_revisar = list(range(self.posicion + 1, nueva_pos + 1))
            for pos in posiciones_a_revisar:
                casilla = tablero.obtener_casilla(pos)
                if len(casilla["fichas"]) == 2:  # Bloqueo detectado
                    return pos - self.posicion -1 if pos - self.posicion - 1 > 0 else None# Se detiene antes del bloqueo y devuelve movimientos permitidos

            return nueva_pos - self.posicion  # Si no hay bloqueos, devuelve los movimientos permitidos

        # 4. Si la ficha ya está en la llegada, verificar movimientos exactos
        nueva_llegada = self.en_llegada + movimientos
        if nueva_llegada > 7:
            return None  # No puede moverse si no es un número exacto para llegar a la meta

        return nueva_llegada  # Devuelve la nueva posición en la llegada


    def mover(self, tablero, movimientos):
        """Mueve la ficha según las reglas establecidas"""
        movimientos_validos = self.puede_moverse(tablero, movimientos)

        captura = False # Si se captura una ficha al mover, se devuelve True

        if movimientos_validos is None:
            print(f"⚠️ Movimiento inválido: la ficha {self.color} no puede moverse.")
            if self.en_meta:
                print(f"⚠️ Ya ha sido coronada.")
            return False, False, False

        # Si la ficha ya está en la llegada
        if self.en_llegada is not None:
            self.en_llegada = movimientos_validos
            casillas_restantes = 7 - self.en_llegada
            if casillas_restantes != 0:
                print(f"✅ {self.color} avanzó en la llegada. Le faltan {casillas_restantes} casilla(s) para coronar.")
            if self.en_llegada == 7:
                self.en_meta = True  # La ficha ha llegado a la meta
                print(f"🏆 {self.color} ha llegado a la meta con una ficha!")
                return True, False, True
            return True, False, False

        # Si la ficha está en el tablero normal, moverla
        if self.posicion is not None:
            tablero.remover_ficha(self)

        nueva_pos = self.posicion + movimientos_validos
        casilla_destino = tablero.obtener_casilla(nueva_pos)

        captura = len(casilla_destino["fichas"]) > 0 if casilla_destino["tipo"] == "normal" else False
        ficha_capturada = None

        if captura:
            ficha_capturada = casilla_destino["fichas"][0]
            tablero.remover_ficha(ficha_capturada)
            ficha_capturada.posicion = None
            tablero.carcel[ficha_capturada.color].append(ficha_capturada)

        tablero.colocar_ficha(self, nueva_pos)

        if self.posicion <= self.inicio_llegada:
            casillas_restantes = (self.inicio_llegada - self.posicion) + 8
        else:
            casillas_restantes = (68 - self.posicion) + self.inicio_llegada + 8

        if self.en_llegada is not None:
            casillas_restantes = (7 - self.en_llegada)
            
        mensaje_de_captura = f" Ha capturado una ficha de color {ficha_capturada.color} en la posición {self.posicion}." if ficha_capturada else ""
        print(f"✅ {self.color} se movió {movimientos_validos} casilla(s).{mensaje_de_captura} Le faltan {casillas_restantes} casilla(s) para coronar.")
        return True, captura, False
    
