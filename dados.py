import random
import re

class Dados:
    def __init__(self, dev=None): # dev = Modo desarrollador 
        self.dobles_consecutivos = 0  # Contador de dobles seguidos
        self.dev = dev

    def lanzar(self):
        """Lanza dos dados y devuelve sus valores."""
        
        if self.dev:
            while True:
                cin = input("🎲 Desea dados aleatorios? (1 Si / 0 No): ")
                try:
                    cin = int(cin)
                    break
                except ValueError:
                    print("Entrada inválida. Intente nuevamente")

            if cin:
                dado1 = random.randint(1, 6)
                dado2 = random.randint(1, 6)
                
            else:
                """Modo desarrollador: permite elegir los valores."""
                while True:
                    cin = input("🎲 Ingrese dos valores (1-6) separados por espacios: ")
                    
                    # Extraer Números
                    valores = re.findall(r'\d+', cin)
                    
                    # Convertir a int y evaluar
                    if len(valores) == 2:
                        dado1, dado2 = map(int, valores)
                        if 1 <= dado1 <= 6 and 1 <= dado2 <= 6:
                            break
                    else:

                        print("Entrada inválida. Ingrese dos números entre 1 y 6.")
        
        else:
            dado1 = random.randint(1, 6)
            dado2 = random.randint(1, 6)

        if dado1 == dado2:
            self.dobles_consecutivos += 1
        else:
            self.dobles_consecutivos = 0


        return dado1, dado2

    def lanzar_un_dado(self):
        """Lanza un solo dado (para desempates)."""
        return random.randint(1, 6)
