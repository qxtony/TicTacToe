from os import system
from time import sleep
from typing import NoReturn

from rich.console import Console

from colors import GameColors
from src import Controller

game = Controller()
console = Console()
colors = GameColors()


def border(to_exit: bool = False) -> NoReturn:
    console.print(
        game.view.create_borders(),
        style=f"{colors.field} bold",
    )
    print("\n")

    if to_exit:
        exit()


def main() -> NoReturn:

    while True:
        system("clear")
        border()

        if game.model.bot_goes_first:
            console.print("Первый ход бота", style=colors.default)
            game.bot.move()
            print("\n")

        console.print(
            "Куда будете делать ход?\n" "Введите номер клетки от 1 до 9. ",
            style=colors.player_input,
        )
        field = input()

        answer = game.user.move(field)
        winner = game.model.check_a_win()

        if winner:
            system("clear")

            console.print(f"Победил игрок {winner}!\n", style=colors.win)
            border(to_exit=True)

        elif game.model.check_a_tie():
            system("clear")

            console.print("Ничья!\n", style=colors.tie)
            border(to_exit=True)

        elif answer:
            console.print(answer, style=colors.default)
            sleep(1.5)

        sleep(0.1)


if __name__ == "__main__":
    main()
