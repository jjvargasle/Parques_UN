from dados import Dados
from tablero import Tablero

class Partida:
    def __init__(self, jugadores, dados):
        self.jugadores = jugadores
        self.dados = dados
        self.tablero = Tablero()
        self.movimientos_disponibles = []
        self.turno_actual = 0  # Índice del jugador que está jugando
        self.en_juego = True  # Indica si la partida sigue activa

        for jugador in self.jugadores:
            for ficha in jugador.fichas:
                self.tablero.carcel[jugador.color].append(ficha)

    def lanzar_dados(self):
        """Lanza los dados y almacena el resultado globalmente."""
        dado1, dado2 = self.dados.lanzar()
        self.movimientos_disponibles = [dado1, dado2]
        print(f"🎲 {self.jugadores[self.turno_actual].nombre} lanzó: {dado1}, {dado2}")
        return dado1, dado2
    
    def obtener_movimientos(self):
        """Devuelve los movimientos disponibles en el turno actual."""
        return self.movimientos_disponibles

    def turno_jugador(self):
        """Ejecuta el turno del jugador actual, asegurando que los movimientos disponibles se gestionen correctamente."""
        jugador = self.jugadores[self.turno_actual]
        print(f"\n Turno de {jugador.nombre} ({jugador.color})")

        while True:
            break_outer = False # Flag 
            # Lanzar los dados y generar los movimientos posibles
            self.lanzar_dados()

            # Verificar si el jugador sacó 3 dobles seguidos
            if self.dados.dobles_consecutivos == 3:
                print(f"⛔ {jugador.nombre} sacó 3 dobles seguidos. Su última ficha movida va a la cárcel.")
                if jugador.ultima_ficha_movida:
                    self.tablero.remover_ficha(jugador.ultima_ficha_movida)
                    jugador.ultima_ficha_movida.posicion = None  # Enviar a la cárcel
                self.dados.dobles_consecutivos = 0  # Resetear contador

            # Intentar sacar ficha de la cárcel si hay un 5 en los dados
            if 5 in self.movimientos_disponibles + [sum(self.movimientos_disponibles)]:
                resultado = jugador.sacar_ficha(self)
                if resultado == 0:
                    # Sacar ficha de la carcel
                    ficha = self.tablero.carcel[jugador.color].pop()
                    pos_salida = self.tablero.salidas[jugador.color]
                    self.tablero.colocar_ficha(ficha, pos_salida)
                    if sum(self.movimientos_disponibles) == 5:
                        self.movimientos_disponibles.clear()
                    else:
                        self.movimientos_disponibles.remove(5)

                    print(f"🎲 {jugador.nombre} sacó una ficha de la cárcel con un 5.")
                
                elif resultado == 1:
                    # Captura en la salida
                    ficha = self.tablero.carcel[jugador.color].pop()
                    pos_salida = self.tablero.salidas[jugador.color]
                    self.tablero.colocar_ficha(ficha, pos_salida)
                    if sum(self.movimientos_disponibles) == 5:
                        self.movimientos_disponibles.clear()
                    else:
                        self.movimientos_disponibles.remove(5)

                    captura = True
                    while captura:
                        ficha, mov = jugador.elegir_ficha(self, [20])
                        if ficha is None:
                            break_outer = True
                            break

                        _ , captura, en_meta = ficha.mover(self.tablero, mov)
                    
    
                elif resultado == 2:
                    # Bloqueo en la salida, mover una ficha para desocupar la salida
                    if sum(self.movimientos_disponibles) == 5:
                        print(f"⚠️ {jugador.nombre} no pudo sacar una ficha de la cárcel.")
                    else:
                        ficha, mov = jugador.elegir_ficha(self, [mov for mov in self.movimientos_disponibles if mov != 5])
                        if ficha and mov:

                            _, captura, en_meta = ficha.mover(self.tablero, mov)
                            while captura:
                                ficha, mov = jugador.elegir_ficha(self, [20])
                                if ficha is None:
                                    break_outer = True
                                    break

                                _ , captura, en_meta = ficha.mover(self.tablero, mov)

                            self.movimientos_disponibles.remove(mov)
                            print(f"✅ {jugador.nombre} movió una ficha {mov} casilla(s) para desocupar la salida.")
                            
                            # Intentar sacar ficha de la cárcel nuevamente
                            if jugador.sacar_ficha(self) == 0:
                                ficha = self.tablero.carcel[jugador.color].pop()
                                pos_salida = self.tablero.salidas[jugador.color]
                                self.tablero.colocar_ficha(ficha, pos_salida)
                                self.movimientos_disponibles.remove(5)
                                print(f"🎲 {jugador.nombre} sacó una ficha de la cárcel con un 5.")
                        else:
                            print(f"⚠️ {jugador.nombre} no pudo mover una ficha para desocupar la salida.")
                else:
                    print(f"⚠️ {jugador.nombre} no tiene fichas en la cárcel.")

            print(f"\n🎲 {jugador.nombre}, movimientos disponibles: {self.movimientos_disponibles}")


            while self.movimientos_disponibles:  # Mientras queden movimientos disponibles
                ficha, mov = jugador.elegir_ficha(self, self.movimientos_disponibles + [sum(self.movimientos_disponibles)])
                
                if ficha is None:
                    break  # No hay más fichas que puedan moverse

                # Si se usó la suma de los dados, eliminar ambos valores individuales
                if mov == sum(self.movimientos_disponibles):
                    self.movimientos_disponibles.clear()
                else: 
                    self.movimientos_disponibles.remove(mov)

                _ , captura, en_meta = ficha.mover(self.tablero, mov)

                while en_meta:
                    ficha, mov = jugador.elegir_ficha(self, [10])
                    if ficha is None:
                        break_outer = True
                        break

                    _ , captura, en_meta = ficha.mover(self.tablero, mov)

                while captura:
                    ficha, mov = jugador.elegir_ficha(self, [20])
                    if ficha is None:
                        break_outer = True
                        break

                    _ , captura, en_meta = ficha.mover(self.tablero, mov)
                
                if break_outer:
                    break

                print(f"📝 Movimientos restantes: {self.movimientos_disponibles}") if len(self.movimientos_disponibles) > 0 else None
            
            if self.verificar_ganador(jugador): # Si el jugador actual ha ganado, termina la partida
                return
            
            if self.dados.dobles_consecutivos == 0:
                break
        
        print("hola")
        self.siguiente_turno()


    def siguiente_turno(self):
        """Pasa al siguiente jugador en la partida."""
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)

    def verificar_ganador(self, jugador):
        """Verifica si algún jugador ha ganado la partida."""
        if all(ficha.en_meta for ficha in jugador.fichas):
            print(f"🏆 {jugador.nombre} ha ganado la partida!")
            self.en_juego = False
            return True
        return False
