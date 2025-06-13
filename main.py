import random


def turing_machine(string):
    string = list(string)
    string.append('B')

    head = 0
    state = 'q0'

    steps = []

    while True:
        symbol = string[head]
        match (state, symbol):
            case ('q0', '0'):
                string[head] = 'X'
                head += 1
                state = 'q1'

            case ('q0', 'Y'):
                head += 1
                state = 'q3'

            case ('q1', '0') | ('q1', 'Y'):
                head += 1

            case ('q1', '1'):
                string[head] = 'Y'
                head -= 1
                state = 'q2'

            case ('q2', '0') | ('q2', 'Y'):
                head -= 1

            case ('q2', 'X'):
                head += 1
                state = 'q0'

            case ('q3', 'Y'):
                head += 1

            case ('q3', 'B'):
                return True

            case _:
                return False


def generar_cadena_aleatoria():
    n = random.randint(1, 5)
    valid = random.choice([True, False])
    if valid:
        return '0' * n + '1' * n
    else:
        m = random.randint(0, 5)
        return '0' * n + '1' * m


def main():
    print("=== Máquina de Turing ===")
    print("1. Ingresar cadena manualmente")
    print("2. Generar cadena aleatoria válida (0^n1^n)")
    opcion = input("Selecciona una opción (1 o 2): ")

    if opcion == '1':
        cadena = input("Introduce una cadena binaria (como 0011): ")
    elif opcion == '2':
        cadena = generar_cadena_aleatoria()
        print(f"Cadena generada: {cadena}")
    else:
        print("❌ Opción inválida.")
        return

    aceptada = turing_machine(cadena)

    if aceptada:
        print("✅ La cadena fue aceptada.")
    else:
        print("❌ La cadena fue rechazada.")


if __name__ == "__main__":
    main()
