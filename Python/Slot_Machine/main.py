import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbols_count = {"A": 2, "B": 4, "C": 6, "D": 8}

symbols_value = {"A": 5, "B": 4, "C": 3, "D": 2}


def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")

        print()


def deposit():
    while True:
        try:
            amount = int(input("What would you like to deposit? $"))
            if amount > 0:
                return amount
            else:
                print("Enter a valid amount")
        except ValueError:
            print("Enter a valid amount")


def number_of_lines():
    while True:
        try:
            lines = int(
                input(
                    "Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? "
                )
            )
            if 1 <= lines <= MAX_LINES:
                return lines
            else:
                print("Enter a valid input")
        except ValueError:
            print("Enter a valid input")


def betting_amount():
    while True:
        try:
            bet = int(input("How much would you like to bet on? "))
            if MIN_BET <= bet <= MAX_BET:
                return bet
            else:
                print("Enter a valid input")
        except ValueError:
            print("Enter a valid input")


def slot_machine(balance):
    lines = number_of_lines()
    while True:
        bet = betting_amount()
        total_bet = bet * lines

        if total_bet > balance:
            print(
                f"You do not have enough to bet that amount, your current balance is: ${balance}"
            )
        else:
            break

    print(
        f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}"
    )

    slots = get_slot_machine_spin(ROWS, COLS, symbols_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbols_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", winning_lines)
    return winnings - total_bet


def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q" or balance == 0:
            break
        balance += slot_machine(balance)

    print(f"You left with ${balance}")


if __name__ == "__main__":
    main()
