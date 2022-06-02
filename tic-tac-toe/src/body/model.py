from random import choice
from typing import Any, Dict, List, NoReturn, Tuple, Union

from src.state import CellState


class Model:
    def __init__(self):
        self.size: int = 3
        self.player: CellState = self.get_random_first_player()
        self.rows: List[List[str]] = self.init_field()
        self.count_human_movements: int = 0
        self.bot_goes_first = False

        if self.player == CellState.O:
            self.bot_goes_first = True

    def get_random_first_player(self) -> CellState:
        return choice([CellState.X, CellState.O])

    def init_field(self) -> List[List[str]]:
        return [[CellState.EMPTY.value] * self.size for _ in range(self.size)]

    def check_valid_type_cell(self, cell: Any) -> Dict[str, Any]:

        if not cell.isdigit():
            return {"status": False, "value": "Вы не ввели номер клетки."}

        cell = int(cell)

        if cell > 9 or cell < 1:
            return {
                "status": False,
                "value": "Пожалуйста, выберите число в диапазоне от 1 до 9.",
            }

        return {"status": True, "value": cell}

    def get_cell_coordinates(self, cell_number: int) -> Tuple[int, int]:
        return divmod(cell_number, self.size)

    def switch_player(self) -> NoReturn:
        self.player = [CellState.X, CellState.O][self.player == CellState.X]

    def get_opponent(self) -> str:

        return [CellState.X.value, CellState.O.value][
            self.player.value == CellState.X.value
        ]

    def line_taken(self, plaing_field: List[List[str]]) -> Union[str, bool]:

        for line in plaing_field:
            player = "".join(set(line))

            if len(player) == 1 and player in [
                CellState.X.value,
                CellState.O.value,
            ]:
                return player

        return False

    def check_a_tie(self) -> bool:

        field_of_cells: List[str] = sum(self.rows.copy(), [])
        return not (CellState.EMPTY.value in field_of_cells)

    def check_a_win(self) -> Union[str, bool]:

        inverted_board = [
            [line[index] for line in self.rows] for index in range(3)
        ]

        diagonal_board = [
            [self.rows[0][0], self.rows[1][1], self.rows[2][2]],
            [self.rows[2][0], self.rows[1][1], self.rows[0][2]],
        ]

        for check_element in [self.rows, inverted_board, diagonal_board]:
            answer = self.line_taken(check_element)

            if answer:
                return answer

        return False
