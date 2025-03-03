from ficha import Ficha
from partida import Partida

class Jugador:
    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color
        self.fichas = [Ficha(color) for _ in range(4)]
        self.ultima_ficha_movida = None

    def lanzar_dados(self, partida):
        """El jugador lanza los dados llamando a la función de partida."""
        return partida.lanzar_dados()

    def elegir_ficha(self, partida, movimientos):
        """Permite al jugador elegir qué ficha mover, o mueve automáticamente si solo hay una opción."""
        opciones = []

        # Identificar fichas que pueden moverse
        for i, ficha in enumerate(self.fichas):
            for movimiento in movimientos:
                if ficha.puede_moverse(partida.tablero, movimiento):
                    opciones.append((i, ficha, movimiento))

        # No hay fichas que puedan moverse
        if not opciones:
            print(f"⚠️ {self.nombre} no puede mover ninguna ficha.")
            return None, None

        # Solo hay una opción disponible, mover automáticamente
        if len(opciones) == 1:
            ficha, movimiento = opciones[0][1], opciones[0][2]
            self.ultima_ficha_movida = ficha
            print(f"✅ Movimiento automático: {self.nombre} mueve su ficha {movimiento} casilla(s).")
            return ficha, movimiento

        # Mostrar opciones y permitir elección
        print(f"\n🎯 {self.nombre}, elige una ficha para mover:")
        for idx, (i, ficha, movimiento) in enumerate(opciones):
            print(f"{idx + 1}. Ficha en posición {ficha.posicion}: Mover {movimiento} casilla(s)")

        while True:
            try:
                eleccion = int(input("Ingrese el número de la ficha a mover: ")) - 1
                if 0 <= eleccion < len(opciones):
                    self.ultima_ficha_movida = opciones[eleccion][1]
                    return opciones[eleccion][1], opciones[eleccion][2]
            except ValueError:
                pass
            print("❌ Selección inválida, intenta de nuevo.")


    ## 0: Exito, 1: Captura, 2: Bloqueo en la salida, -1: No hay fichas en la carcel 
    def sacar_ficha(self, partida):
        """Saca una ficha de la carcel si el juego lo permite"""
        
        mi_carcel = partida.tablero.carcel[self.color]
        pos_salida = partida.tablero.salidas[self.color]
        casilla_salida = partida.tablero.obtener_casilla(pos_salida)
        
        # No hay fichas en la carcel
        if not mi_carcel:
            return -1

        # Verificar si hay fichas para capturar en la salida
        if any(f.color != self.color for f in casilla_salida["fichas"]):
            for ficha in casilla_salida["fichas"]:
                if ficha.color != self.color:
                    partida.tablero.remover_ficha(ficha)
                    ficha.posicion = None
                    partida.tablero.carcel[ficha.color].append(ficha)
                    print(f"⚔️ {self.nombre} captura a una ficha {ficha.color} en la salida!")
            return 1

        elif len(casilla_salida["fichas"]) == 2:
            return 2
        else:
            return 0

