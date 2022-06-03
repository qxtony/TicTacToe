from os import system
from time import sleep
from typing import NoReturn

from rich.console import Console

from colors import GameColors
from src import TicTacToe

game = TicTacToe()
console = Console()
colors = GameColors()


def border(to_exit: bool = False) -> NoReturn:
    console.print(
        game.create_borders(),
        style=f"{colors.field} bold",
    )
    print("\n")

    if to_exit:
        exit()


def main() -> NoReturn:

    while True:
        system("clear")
        border()

        if game.bot_goes_first:
            console.print("Первый ход бота", style=colors.default)
            print("\n")

        winner = game.check_a_win()

        if winner:
            system("clear")

            console.print(f"Победил игрок {winner}!\n", style=colors.win)
            border(to_exit=True)

        elif game.check_a_tie():
            system("clear")

            console.print("Ничья!\n", style=colors.tie)
            border(to_exit=True)


        console.print(
            "Куда будете делать ход?\n"
            "Введите номер клетки от 1 до 9. ",
            style=colors.player_input,
        )
        field = input()

        answer = game.move(field)

        if answer:
            console.print(answer, style=colors.default)
            sleep(1.5)

        sleep(0.1)


if __name__ == "__main__":
    main()
