import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def instantaneous_description(state, tape, head):
    left = ''.join(tape[:head])
    right = ''.join(tape[head:])
    return f"{left} q{state} {right}"


def turing_machine(tape_string, max_length=1000):
    if len(tape_string) > max_length:
        raise ValueError(
            f"Input exceeds maximum allowed length of {max_length}.")

    tape = list(tape_string)
    tape.append('B')

    head = 0
    state = '0'
    steps = []

    while True:
        symbol = tape[head]
        steps.append((state, tape.copy(), head))

        match (state, symbol):
            case ('0', '0'):
                tape[head] = 'X'
                head += 1
                state = '1'
            case ('0', 'Y'):
                head += 1
                state = '3'
            case ('1', '0') | ('1', 'Y'):
                head += 1
            case ('1', '1'):
                tape[head] = 'Y'
                head -= 1
                state = '2'
            case ('2', '0') | ('2', 'Y'):
                head -= 1
            case ('2', 'X'):
                head += 1
                state = '0'
            case ('3', 'Y'):
                head += 1
            case ('3', 'B'):
                steps.append(('ACCEPT', tape.copy(), head))
                return True, steps
            case _:
                steps.append(('REJECT', tape.copy(), head))
                return False, steps


def generate_random_string(max_length=1000):
    n = random.randint(1, min(10, max_length // 2))
    valid = random.choice([True, False])
    if valid:
        return '0' * n + '1' * n
    else:
        m = random.randint(0, max_length - n)
        return '0' * n + '1' * m


def write_steps_to_file(steps, filename='output.txt'):
    with open(filename, 'w') as f:
        for state, tape, head in steps:
            f.write(instantaneous_description(state, tape, head) + '\n')


def animate_steps(steps, accepted):
    tape_length = len(steps[0][1])
    fig, ax = plt.subplots(figsize=(max(8, tape_length), 3))
    ax.set_xlim(0, tape_length)
    ax.set_ylim(0, 3)
    ax.axis('off')

    boxes, symbols, arrows = [], [], []
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
            result_message.set_text(
                "STRING ACCEPTED" if accepted else "STRING REJECTED")

    anim = FuncAnimation(fig, update, frames=len(steps),
                         interval=800, repeat=False)
    plt.show()


def main():
    print("=== Turing Machine Simulator ===")
    print("1. Enter string manually")
    print("2. Generate random binary string")
    option = input("Choose an option (1 or 2): ")

    if option == '1':
        tape_input = input("Enter a binary string (max 1000 characters): ")
    elif option == '2':
        tape_input = generate_random_string()
        print(f"Generated string: {tape_input}")
    else:
        print("Invalid option.")
        return

    if len(tape_input) > 1000:
        print("Input too long.")
        return

    accepted, steps = turing_machine(tape_input)
    write_steps_to_file(steps)

    if len(tape_input) <= 10:
        animate_steps(steps, accepted)
    else:
        print("Animation skipped due to input length. See output.txt for full computation trace.")


if __name__ == "__main__":
    main()
