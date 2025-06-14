import random
import time
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def turing_machine(tape_string):
    tape = list(tape_string)
    tape.append('B')

    head = 0
    state = 'q0'

    steps = []

    while True:
        symbol = tape[head]
        steps.append((state, tape.copy(), head))

        match (state, symbol):
            case ('q0', '0'):
                tape[head] = 'X'
                head += 1
                state = 'q1'

            case ('q0', 'Y'):
                head += 1
                state = 'q3'

            case ('q1', '0') | ('q1', 'Y'):
                head += 1

            case ('q1', '1'):
                tape[head] = 'Y'
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
                return True, steps

            case _:
                return False, steps


def generate_random_string():
    n = random.randint(1, 5)
    valid = random.choice([True, False])
    if valid:
        return '0' * n + '1' * n
    else:
        m = random.randint(0, 5)
        return '0' * n + '1' * m


def animate_steps(steps, accepted):
    tape_length = len(steps[0][1])
    fig, ax = plt.subplots(figsize=(tape_length, 3))
    ax.set_xlim(0, tape_length)
    ax.set_ylim(0, 3)
    ax.axis('off')

    boxes = []
    symbols = []
    arrows = []
    state_box = plt.Rectangle(
        (tape_length // 2 - 1, 2.4), 2, 0.4, facecolor='#cce5ff', edgecolor='black')
    ax.add_patch(state_box)
    state_label = ax.text(tape_length // 2, 2.6, '',
                          ha='center', va='center', fontsize=16, weight='bold')

    result_message = ax.text(tape_length // 2, 0.2, '', ha='center', va='center',
                             fontsize=14, weight='bold',
                             bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen' if accepted else 'lightcoral'))

    for i in range(tape_length):
        box = plt.Rectangle((i, 1), 1, 1, edgecolor='black', facecolor='white')
        ax.add_patch(box)
        boxes.append(box)

        symbol_text = ax.text(i + 0.5, 1.5, '', ha='center',
                              va='center', fontsize=16)
        symbols.append(symbol_text)

        arrow = ax.text(i + 0.5, 0.7, '', ha='center',
                        va='center', fontsize=16, color='red')
        arrows.append(arrow)

    def update(frame):
        state, tape, head = steps[frame]
        state_label.set_text(f"State: {state}")

        for i in range(tape_length):
            symbols[i].set_text(tape[i])
            arrows[i].set_text('↑' if i == head else '')
            boxes[i].set_facecolor('#FFDDC1' if i == head else 'white')

        if frame == len(steps) - 1:
            if accepted:
                result_message.set_text("STRING ACCEPTED")
            else:
                result_message.set_text("STRING REJECTED")

    anim = FuncAnimation(fig, update, frames=len(steps),
                         interval=800, repeat=False)
    plt.show()


def main():
    print("=== Turing Machine Simulator ===")
    print("1. Enter string manually")
    print("2. Generate random binary string")
    option = input("Choose an option (1 or 2): ")

    if option == '1':
        tape_input = input("Enter a binary string (like 0011): ")
    elif option == '2':
        tape_input = generate_random_string()
        print(f"Generated string: {tape_input}")
    else:
        print("Invalid option.")
        return

    accepted, steps = turing_machine(tape_input)

    animate_steps(steps, accepted)


if __name__ == "__main__":
    main()
