from partida import Partida
from jugador import Jugador
from dados import Dados

def configurar_partida():
    print("🔹 Configuración de la partida 🔹")

    # Configurar modo desarrollador
    while True:
        try:
            dev_mode = int(input("¿Desea activar el modo desarrollador? (1: Sí, 0: No): "))
            if dev_mode in [0, 1]:
                dev_mode = bool(dev_mode)
                break
        except ValueError:
            pass
        print("❌ Entrada inválida. Intente nuevamente.")

    # Configurar número de jugadores
    while True:
        try:
            num_jugadores = int(input("Ingrese el número de jugadores (2-4): "))
            if 1 < num_jugadores <= 4:
                break
        except ValueError:
            pass
        print("❌ Entrada inválida. Intente nuevamente.")

    # Configurar nombres y colores de los jugadores
    jugadores = []
    colores_disponibles = ["rojo", "azul", "verde", "amarillo"]
    for i in range(num_jugadores):
        nombre = input(f"Ingrese el nombre del jugador {i + 1}: ")
        while True:
            color = input(f"Ingrese el color del jugador {i + 1} ({', '.join(colores_disponibles)}): ").lower()
            if color in colores_disponibles:
                colores_disponibles.remove(color)
                break
            print("❌ Color inválido o ya elegido. Intente nuevamente.")
        jugadores.append(Jugador(nombre, color))

    # Crear dados y partida
    dados = Dados(dev=dev_mode)
    partida = Partida(jugadores, dados)

    return partida

def menu_principal():
    print("\n🔹 Menú Principal 🔹")
    opcion = None
    while not opcion:
        print("1. Iniciar nueva partida")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")

        try: 
            if 1 >= int(opcion) <= 2:
                break
        except ValueError:
            print("❌ Opción inválida. Intente nuevamente.")
            opcion = None    
        else:
            print("❌ Opción inválida. Intente nuevamente.")
            opcion = None

    if opcion == "1":
        partida = configurar_partida()
        while partida.en_juego:
            partida.turno_jugador()
    elif opcion == "2":
        print("👋 ¡Gracias por jugar! Hasta luego.")

if __name__ == "__main__":
    menu_principal()