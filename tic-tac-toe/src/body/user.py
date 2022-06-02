from typing import Any, Optional

from src.state import CellState


class User:
    def __init__(self, model, bot):
        self.model = model
        self.bot = bot

    def move(self, cell: str) -> Optional[Any]:

        if self.model.player == CellState.O:
            self.bot.move()

        elif self.model.check_a_tie():
            return "Ничья!"

        response = self.model.check_valid_type_cell(cell)

        if not response["status"]:
            return response["value"]

        value = response["value"]

        y, x = self.model.get_cell_coordinates(value - 1)
        field = self.model.rows[y][x]

        if field == self.model.player.value:
            return "Вы уже выполнили ход на эту клетку."

        elif field == self.model.get_opponent():
            return "В это место уже сходил БОТ."

        self.model.rows[y][x] = self.model.player.value
        self.model.count_human_movements += 1

        self.model.switch_player()
        return self.bot.move()
